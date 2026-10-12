"""Per-worker progress reporting for parallel upstream lookups."""

import sys
import threading
from collections.abc import Sequence
from typing import TextIO, TypeVar

T = TypeVar("T")


def partition(items: Sequence[T], workers: int) -> list[list[T]]:
    """Assign ``items`` round-robin to ``workers`` buckets."""
    return [list(items[worker::workers]) for worker in range(workers)]


class WorkerProgress:
    """Render one progress bar per worker, redrawn in place on a terminal.

    Non-interactive streams receive one line per completed item instead,
    so logs and captured output stay readable.
    """

    def __init__(
        self, totals: Sequence[int], stream: TextIO | None = None, width: int = 20
    ) -> None:
        """Track ``totals[worker]`` items for each worker and write to ``stream``."""
        self.totals = list(totals)
        self.done = [0] * len(self.totals)
        self.current = [""] * len(self.totals)
        self.completed = 0
        self.width = width
        self.stream = stream or sys.stderr
        self.interactive = self.stream.isatty()
        self.lock = threading.Lock()
        self.drawn = 0

    def render(self) -> list[str]:
        """Return the header and one bar line per worker."""
        lines = [f"Resolving upstreams [{self.completed}/{sum(self.totals)}]:"]
        for worker, (done, total) in enumerate(zip(self.done, self.totals)):
            filled = self.width * done // total if total else self.width
            bar = "#" * filled + "-" * (self.width - filled)
            lines.append(
                f"  Worker {worker + 1:>2}: [{bar}] {done}/{total} "
                f"{self.current[worker]}".rstrip()
            )
        return lines

    def start(self) -> None:
        """Draw the initial, empty bars on an interactive stream."""
        if self.interactive:
            with self.lock:
                self._draw()

    def advance(self, worker: int, item: str) -> None:
        """Record that ``worker`` finished ``item`` and refresh the display."""
        with self.lock:
            self.done[worker] += 1
            self.completed += 1
            self.current[worker] = item
            if self.interactive:
                self._draw()
            else:
                self.stream.write(
                    f"Resolved [{self.completed}/{sum(self.totals)}] {item} "
                    f"(worker {worker + 1})\n"
                )
                self.stream.flush()

    def _draw(self) -> None:
        lines = self.render()
        if self.drawn:
            self.stream.write(f"\x1b[{self.drawn}A")
        self.stream.write("".join(f"\r\x1b[2K{line}\n" for line in lines))
        self.stream.flush()
        self.drawn = len(lines)
