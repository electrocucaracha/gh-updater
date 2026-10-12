import io
import unittest

from gh_updater.progress import WorkerProgress, partition


class TerminalStream(io.StringIO):
    def isatty(self):
        return True


class ProgressTests(unittest.TestCase):
    def test_partition_round_robin(self):
        self.assertEqual(
            partition(["a", "b", "c", "d", "e"], 2), [["a", "c", "e"], ["b", "d"]]
        )
        self.assertEqual(partition(["a"], 1), [["a"]])

    def test_non_interactive_prints_one_line_per_item(self):
        stream = io.StringIO()
        progress = WorkerProgress([1, 1], stream)
        progress.start()
        progress.advance(1, "owner/b")
        progress.advance(0, "owner/a")
        self.assertEqual(
            stream.getvalue(),
            "Resolved [1/2] owner/b (worker 2)\nResolved [2/2] owner/a (worker 1)\n",
        )

    def test_interactive_redraws_bars_in_place(self):
        stream = TerminalStream()
        progress = WorkerProgress([2, 1], stream, width=4)
        progress.start()
        self.assertNotIn("\x1b[3A", stream.getvalue())
        progress.advance(0, "owner/a")
        output = stream.getvalue()
        self.assertIn("\x1b[3A", output)
        self.assertIn("\r\x1b[2K", output)
        self.assertEqual(
            progress.render(),
            [
                "Resolving upstreams [1/3]:",
                "  Worker  1: [##--] 1/2 owner/a",
                "  Worker  2: [----] 0/1",
            ],
        )
        self.assertNotIn("Resolved [", output)


if __name__ == "__main__":
    unittest.main()
