"""Command-line interface for updating GitHub Action references."""

import logging
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import click
import yaml

from .actions import references, update_text
from .errors import UpdateError
from .files import discover, write_atomic
from .resolver import Resolver

logger = logging.getLogger("gh-updater")


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument(
    "repository",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=".",
)
@click.option("--dry-run", is_flag=True, help="Preview without writing.")
@click.option(
    "--exclude",
    multiple=True,
    metavar="OWNER/REPO[/PATH]",
    help="Leave a repository or exact action unchanged; repeat as needed.",
)
@click.option(
    "--log-level",
    type=click.Choice(
        ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False
    ),
    default="WARNING",
    show_default=True,
    help="Set diagnostic logging verbosity (progress is always shown).",
)
def cli(
    repository: Path, dry_run: bool, exclude: tuple[str, ...], log_level: str
) -> int:
    """Pin GitHub Actions to the latest stable numeric tag's commit.

    REPOSITORY defaults to the current directory.

    Returns 0 on success and 1 when an update cannot be completed safely.
    """
    logging.basicConfig(
        level=log_level.upper(),
        format="%(name)s: %(levelname)s: %(message)s",
        force=True,
    )
    root = repository.resolve()
    resolver = Resolver()
    pending = []
    excluded = set(exclude)
    try:
        click.echo(f"Scanning {root}...", err=True)
        files = discover(root)
        sources = []
        repos = set()
        for path in files:
            text = path.read_bytes().decode("utf-8")
            try:
                repos.update(
                    reference.repo
                    for reference in references(text)
                    if reference.repo not in excluded
                    and reference.action not in excluded
                )
            except (UpdateError, yaml.YAMLError) as exc:
                raise UpdateError(f"{path.relative_to(root)}: {exc}") from exc
            sources.append((path, text))
        click.echo(
            f"Found {len(files)} YAML file(s); resolving {len(repos)} upstream(s)...",
            err=True,
        )
        if repos:
            with ThreadPoolExecutor() as executor:
                futures = {
                    executor.submit(resolver.lookup, repo): repo
                    for repo in sorted(repos)
                }
                for completed, future in enumerate(as_completed(futures), 1):
                    repo = futures[future]
                    resolver.cache[repo] = future.result()
                    click.echo(f"Resolved [{completed}/{len(repos)}] {repo}", err=True)
        for completed, (path, text) in enumerate(sources, 1):
            try:
                updated, changes = update_text(text, resolver, excluded)
            except (UpdateError, yaml.YAMLError) as exc:
                raise UpdateError(f"{path.relative_to(root)}: {exc}") from exc
            if changes:
                pending.append((path, text, updated, changes))
            click.echo(
                f"Checked [{completed}/{len(files)}] {path.relative_to(root)}", err=True
            )
            logger.debug(
                "%s: %d reference update(s)", path.relative_to(root), len(changes)
            )
        # Resolve and validate every file before making any changes.
        for completed, (path, text, updated, _) in enumerate(pending, 1):
            if not dry_run:
                click.echo(
                    f"Writing [{completed}/{len(pending)}] {path.relative_to(root)}",
                    err=True,
                )
                write_atomic(path, text, updated)
        for path, _, _, changes in pending:
            for change in changes:
                click.echo(f"{path.relative_to(root)}:{change}")
    except (UpdateError, OSError, UnicodeError) as exc:
        click.echo(f"gh-updater: error: {exc}", err=True)
        logger.debug("Update failed", exc_info=True)
        return 1
    verb = "Would update" if dry_run else "Updated"
    click.echo(f"{verb} {len(pending)} of {len(files)} YAML file(s).")
    return 0


def main(argv: list[str] | None = None) -> int:
    """Run the command-line interface with ``argv`` and return its exit code."""
    try:
        return cli.main(args=argv, prog_name="gh-updater", standalone_mode=False)
    except click.ClickException as exc:
        exc.show(file=sys.stderr)
        return exc.exit_code
