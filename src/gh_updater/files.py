"""Discover updater inputs and write changed files atomically."""

import os
import tempfile
from pathlib import Path

from .errors import UpdateError

IGNORED_DIRS = {".git", ".venv", ".tox", "venv", "node_modules", "__pycache__"}


def discover(root: Path) -> list[Path]:
    """Find GitHub workflow and action metadata YAML files below ``root``."""
    files = []
    for directory, dirs, names in os.walk(root, followlinks=False):
        dirs[:] = sorted(
            name
            for name in dirs
            if name not in IGNORED_DIRS and not (Path(directory) / name).is_symlink()
        )
        for name in sorted(names):
            path = Path(directory) / name
            relative = path.relative_to(root)
            if path.is_symlink():
                continue
            if name in ("action.yml", "action.yaml") or (
                relative.parts[0] == ".github" and path.suffix in (".yml", ".yaml")
            ):
                files.append(path)
    return files


def write_atomic(path: Path, original: str, updated: str) -> None:
    """Atomically replace ``path`` if its contents still match ``original``."""
    if path.read_bytes().decode("utf-8") != original:
        raise UpdateError(f"{path}: changed during lookup; rerun the command")
    temporary: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="", dir=path.parent, delete=False
        ) as stream:
            temporary = stream.name
            stream.write(updated)
        os.chmod(temporary, path.stat().st_mode)
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            Path(temporary).unlink(missing_ok=True)
