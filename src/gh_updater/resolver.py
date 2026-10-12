"""Resolve GitHub Action refs to stable commits."""

import logging
import os
import re
import subprocess

from .errors import UpdateError

VERSION = re.compile(r"[vV]?(\d+(?:\.\d+)*)")
SHA = re.compile(r"[0-9a-fA-F]{40}")
logger = logging.getLogger("gh-updater")


class Resolver:
    """Cache GitHub refs and resolve action references to stable commits."""

    def __init__(self) -> None:
        """Initialize an empty per-repository ref cache."""
        self.cache: dict[str, dict[str, str]] = {}

    def lookup(self, repo: str) -> dict[str, str]:
        """Fetch and validate the tags and branches advertised for ``repo``."""
        logger.debug("Looking up upstream %s", repo)
        env = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
        try:
            result = subprocess.run(
                [
                    "git",
                    "ls-remote",
                    "--tags",
                    "--heads",
                    f"https://github.com/{repo}.git",
                ],
                check=True,
                capture_output=True,
                text=True,
                timeout=60,
                env=env,
            )
        except subprocess.CalledProcessError as exc:
            raise UpdateError(
                f"{repo}: git lookup failed: {exc.stderr.strip()}"
            ) from exc
        except subprocess.TimeoutExpired as exc:
            raise UpdateError(f"{repo}: git lookup timed out after 60 seconds") from exc
        refs: dict[str, str] = {}
        for line in result.stdout.splitlines():
            parts = line.split()
            if len(parts) != 2 or not SHA.fullmatch(parts[0]):
                raise UpdateError(f"{repo}: invalid git ls-remote response")
            refs[parts[1]] = parts[0]
        logger.debug("Loaded %d refs for %s", len(refs), repo)
        return refs

    def resolve(self, repo: str, ref: str) -> tuple[str, str]:
        """Return the resolved commit SHA and display version for ``repo``."""
        if repo not in self.cache:
            self.cache[repo] = self.lookup(repo)
        refs = self.cache[repo]
        versions = []
        for name in refs:
            if not name.startswith("refs/tags/"):
                continue
            tag = name.removeprefix("refs/tags/")
            match = VERSION.fullmatch(tag)
            if match:
                numbers = tuple(int(part) for part in match[1].split("."))
                versions.append((numbers, tag))
        if versions:
            width = max(len(numbers) for numbers, _ in versions)
            _, tag = max(
                versions,
                key=lambda item: (
                    item[0] + (0,) * (width - len(item[0])),
                    len(item[0]),
                    item[1],
                ),
            )
            name = f"refs/tags/{tag}"
            return refs.get(name + "^{}", refs[name]), tag
        if SHA.fullmatch(ref):
            raise UpdateError(
                f"{repo}: no stable numeric tags and no branch/tag hint for pinned SHA; "
                "add a '# main' style comment or use --exclude"
            )
        tag = f"refs/tags/{ref}"
        for name in (tag + "^{}", tag, f"refs/heads/{ref}"):
            if name in refs:
                return refs[name], ref
        raise UpdateError(f"{repo}: no stable numeric tags and cannot resolve {ref!r}")
