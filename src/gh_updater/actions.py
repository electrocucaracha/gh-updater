"""Parse and update GitHub Action references in YAML text."""

import re
from dataclasses import dataclass

import yaml
from yaml.nodes import MappingNode, Node, ScalarNode, SequenceNode
from yaml.tokens import ScalarToken

from .errors import UpdateError
from .resolver import SHA, VERSION, Resolver

ACTION = re.compile(
    r"(?P<repo>[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)"
    r"(?P<path>(?:/[A-Za-z0-9_.-]+)*)@(?P<ref>[^\s@]+)"
)


@dataclass(frozen=True)
class Reference:
    """A GitHub Action reference and its source location in YAML text."""

    action: str
    repo: str
    ref: str
    start: int
    end: int
    line: int
    quote: str
    flow: bool


def mapping(node: Node | None) -> dict[str, Node]:
    """Return a YAML mapping's scalar-keyed values, or an empty mapping."""
    if not isinstance(node, MappingNode):
        return {}
    return {
        key.value: value for key, value in node.value if isinstance(key, ScalarNode)
    }


def steps(node: Node | None) -> list[Node]:
    """Return the items in a YAML sequence, or an empty list."""
    return list(node.value) if isinstance(node, SequenceNode) else []


def references(text: str) -> list[Reference]:
    """Extract remote ``uses`` references from workflow and composite-action YAML.

    >>> refs = references("jobs:\\n  build:\\n    steps:\\n      - uses: owner/repo/sub@v1\\n")
    >>> [(ref.action, ref.ref, ref.line) for ref in refs]
    [('owner/repo/sub', 'v1', 4)]
    """
    root = mapping(yaml.compose(text, Loader=yaml.BaseLoader))
    containers: list[Node] = []
    for job in mapping(root.get("jobs")).values():
        containers.append(job)
        containers.extend(steps(mapping(job).get("steps")))
    containers.extend(steps(mapping(root.get("runs")).get("steps")))
    tokens = [token for token in yaml.scan(text) if isinstance(token, ScalarToken)]
    found: dict[int, Reference] = {}
    for container in containers:
        node = mapping(container).get("uses")
        if not isinstance(node, ScalarNode):
            if node is not None:
                raise UpdateError("'uses' must be a string")
            continue
        if node.value.startswith(("./", "docker://")):
            continue
        match = ACTION.fullmatch(node.value)
        if not match:
            raise UpdateError(
                f"line {node.start_mark.line + 1}: invalid uses: {node.value}"
            )
        token = next(
            token
            for token in tokens
            if node.start_mark.index <= token.start_mark.index < node.end_mark.index
        )
        if token.style in ("|", ">") or token.start_mark.line != token.end_mark.line:
            raise UpdateError(
                f"line {token.start_mark.line + 1}: multiline 'uses' is unsupported; "
                "use a single-line scalar"
            )
        found[token.start_mark.index] = Reference(
            action=match["repo"] + match["path"],
            repo=match["repo"],
            ref=match["ref"],
            start=token.start_mark.index,
            end=token.end_mark.index,
            line=token.start_mark.line + 1,
            quote=token.style or "",
            flow=isinstance(container, MappingNode) and bool(container.flow_style),
        )
    return list(found.values())


def update_text(
    text: str, resolver: Resolver, excluded: set[str]
) -> tuple[str, list[str]]:
    """Pin eligible action refs in ``text`` and return the edits made.

    The input is not modified. Excluded repositories and exact action paths are
    left unchanged.
    """
    edits = []
    changes = []
    for reference in references(text):
        if reference.action in excluded or reference.repo in excluded:
            continue
        line_end = text.find("\n", reference.end)
        if line_end == -1:
            line_end = len(text)
        if line_end > reference.end and text[line_end - 1] == "\r":
            line_end -= 1
        tail = text[reference.end : line_end]
        comment = re.fullmatch(r"[ \t]*#[ \t]*(.*)", tail)
        hint = reference.ref
        if SHA.fullmatch(hint) and comment and comment[1].split():
            hint = comment[1].split()[0]
        sha, version = resolver.resolve(reference.repo, hint)
        value = f"{reference.action}@{sha}"
        replacement = reference.quote + value + reference.quote
        end = reference.end
        if not reference.flow:
            if tail.strip() and not comment:
                raise UpdateError(f"line {reference.line}: unsupported uses suffix")
            if comment:
                body = comment[1]
                parts = body.split(maxsplit=1)
                # Replace updater hints, but keep human commentary.
                if parts and (
                    VERSION.fullmatch(parts[0])
                    or parts[0] in (hint, version)
                    or SHA.fullmatch(parts[0])
                ):
                    body = parts[1] if len(parts) > 1 else ""
                replacement += f" # {version}" + (f" {body}" if body else "")
            else:
                replacement += f" # {version}"
            end = line_end
        if text[reference.start : end] != replacement:
            edits.append((reference.start, end, replacement))
            changes.append(
                f"{reference.line}: {reference.action}@{reference.ref} -> {sha} # {version}"
            )
    for start, end, replacement in sorted(edits, reverse=True):
        text = text[:start] + replacement + text[end:]
    return text, changes
