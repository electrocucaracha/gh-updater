import contextlib
import io
import subprocess
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

from gh_updater.actions import references, update_text
from gh_updater.cli import main
from gh_updater.errors import UpdateError
from gh_updater.files import discover
from gh_updater.resolver import Resolver

OLD = "1" * 40
NEW = "2" * 40
TAG_OBJECT = "3" * 40


def remote_output():
    return subprocess.CompletedProcess(
        [],
        0,
        f"{OLD}\trefs/tags/v9\n"
        f"{TAG_OBJECT}\trefs/tags/v10.2.0\n"
        f"{NEW}\trefs/tags/v10.2.0^{{}}\n"
        f"{OLD}\trefs/tags/v11.0.0-beta\n",
        "",
    )


class UpdaterTests(unittest.TestCase):
    @patch("gh_updater.resolver.subprocess.run", return_value=remote_output())
    def test_latest_numeric_annotated_tag_and_cache(self, run):
        resolver = Resolver()
        self.assertEqual(resolver.resolve("owner/repo", "v9"), (NEW, "v10.2.0"))
        self.assertEqual(resolver.resolve("owner/repo", OLD), (NEW, "v10.2.0"))
        run.assert_called_once()
        self.assertIn("https://github.com/owner/repo.git", run.call_args.args[0])

    @patch("gh_updater.resolver.subprocess.run", return_value=remote_output())
    def test_yaml_preservation_subpaths_comments_and_idempotence(self, run):
        text = (
            "on: push\r\njobs:\r\n  build:\r\n    steps:\r\n"
            f"      - uses: 'owner/repo/sub@{OLD}' # v9 keep this\r\n"
            "      - uses: ./local\r\n"
            "      - uses: docker://alpine:3\r\n"
            "      - run: |\r\n          echo 'uses: owner/fake@v1'\r\n"
        )
        resolver = Resolver()
        updated, changes = update_text(text, resolver, set())
        self.assertEqual(len(changes), 1)
        self.assertEqual(updated, text.replace(f"{OLD}' # v9", f"{NEW}' # v10.2.0"))
        self.assertEqual(update_text(updated, resolver, set()), (updated, []))
        self.assertIn("on", yaml.load(updated, Loader=yaml.BaseLoader))
        run.assert_called_once()

    @patch("gh_updater.resolver.subprocess.run", return_value=remote_output())
    def test_reusable_workflows_composites_quotes_and_exclusions(self, run):
        for text in (
            'jobs:\n  call:\n    uses: "owner/repo/.github/workflows/ci.yaml@v9"\n',
            "runs:\n  using: composite\n  steps:\n    - uses: owner/repo@v9 # reason\n",
        ):
            with self.subTest(text=text):
                updated, changes = update_text(text, Resolver(), set())
                self.assertEqual(len(changes), 1)
                self.assertIn(NEW, updated)
                yaml.compose(updated)
                self.assertEqual(
                    update_text(text, Resolver(), {"owner/repo"}), (text, [])
                )
        self.assertEqual(run.call_count, 2)

    @patch("gh_updater.resolver.subprocess.run", return_value=remote_output())
    def test_flow_and_anchor_remain_valid(self, run):
        text = (
            "jobs:\n  build:\n    steps:\n"
            "      - uses: &action owner/repo@v9\n"
            "      - uses: *action\n"
            '      - {uses: "owner/repo@v9", name: example}\n'
        )
        updated, changes = update_text(text, Resolver(), set())
        self.assertEqual(len(changes), 2)
        self.assertIn(f"&action owner/repo@{NEW} # v10.2.0", updated)
        self.assertIn(f'{{uses: "owner/repo@{NEW}", name: example}}', updated)
        self.assertEqual(len(references(updated)), 2)
        yaml.compose(updated)

    @patch("gh_updater.resolver.subprocess.run")
    def test_no_tags_branch_hints_are_per_occurrence(self, run):
        run.return_value = subprocess.CompletedProcess(
            [], 0, f"{OLD}\trefs/heads/main\n{NEW}\trefs/heads/develop\n", ""
        )
        text = (
            "jobs:\n  first:\n"
            f"    uses: owner/repo/.github/workflows/ci.yml@{NEW} # main\n"
            "  second:\n"
            f"    uses: owner/repo/.github/workflows/ci.yml@{OLD} # develop\n"
        )
        updated, changes = update_text(text, Resolver(), set())
        self.assertIn(f"@{OLD} # main", updated)
        self.assertIn(f"@{NEW} # develop", updated)
        self.assertEqual(len(changes), 2)
        with self.assertRaisesRegex(UpdateError, "no branch/tag hint"):
            Resolver().resolve("owner/repo", OLD)

    def test_invalid_and_multiline_uses_fail(self):
        for value in (
            "owner/repo",
            "|\n          owner/repo@v1",
            "${{ inputs.action }}",
        ):
            with self.subTest(value=value), self.assertRaises(UpdateError):
                references(f"jobs:\n  build:\n    steps:\n      - uses: {value}\n")

    @patch("gh_updater.resolver.subprocess.run", return_value=remote_output())
    def test_cli_discovery_dry_run_write_and_no_partial_lookup_edits(self, run):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workflow = root / ".github/workflows/ci.yaml"
            workflow.parent.mkdir(parents=True)
            original = (
                b"jobs:\r\n  build:\r\n    steps:\r\n      - uses: owner/repo@v9\r\n"
            )
            workflow.write_bytes(original)
            workflow.chmod(0o640)
            composite = root / "local/action.yml"
            composite.parent.mkdir()
            composite.write_text("runs:\n  steps:\n    - uses: owner/repo/sub@v9\n")
            ignored = root / "node_modules/action.yml"
            ignored.parent.mkdir()
            ignored.write_text("invalid: [")
            tox_action = root / ".tox/test/action.yml"
            tox_action.parent.mkdir(parents=True)
            tox_action.write_text("invalid: [")
            link = root / "action.yaml"
            link.symlink_to(workflow)
            self.assertEqual(set(discover(root)), {workflow, composite})
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main([directory, "--dry-run"]), 0)
                self.assertEqual(workflow.read_bytes(), original)
                self.assertEqual(main([directory]), 0)
                self.assertEqual(main([directory]), 0)
            self.assertEqual(workflow.stat().st_mode & 0o777, 0o640)
            self.assertIn(f"@{NEW} # v10.2.0\r\n".encode(), workflow.read_bytes())
            workflow.write_bytes(original)
            composite.write_text("runs:\n  steps:\n    - uses: owner/missing@v1\n")

            def lookup(command, **kwargs):
                if command[-1] == "https://github.com/owner/missing.git":
                    raise subprocess.CalledProcessError(128, [], stderr="not found")
                return remote_output()

            run.side_effect = lookup
            with contextlib.redirect_stderr(io.StringIO()) as errors:
                self.assertEqual(main([directory]), 1)
            self.assertIn("not found", errors.getvalue())
            self.assertEqual(workflow.read_bytes(), original)

    @patch("gh_updater.resolver.subprocess.run")
    def test_timeout_and_missing_tags_are_errors(self, run):
        run.side_effect = subprocess.TimeoutExpired("git", 60)
        with self.assertRaisesRegex(UpdateError, "timed out"):
            Resolver().resolve("owner/repo", "v1")
        run.side_effect = None
        run.return_value = subprocess.CompletedProcess([], 0, "", "")
        with self.assertRaisesRegex(UpdateError, "cannot resolve"):
            Resolver().resolve("owner/repo", "v1")

    @patch("gh_updater.resolver.subprocess.run")
    def test_equal_versions_prefer_specific_tag_and_numeric_order(self, run):
        run.return_value = subprocess.CompletedProcess(
            [],
            0,
            f"{OLD}\trefs/tags/V10\n"
            f"{NEW}\trefs/tags/10.0.0\n"
            f"{OLD}\trefs/tags/v9.99.99\n"
            f"{OLD}\trefs/tags/nightly\n",
            "",
        )
        self.assertEqual(Resolver().resolve("owner/repo", "main"), (NEW, "10.0.0"))

    def test_yaml_error_leaves_files_unchanged(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "action.yml"
            path.write_text("runs: [")
            with contextlib.redirect_stderr(io.StringIO()) as errors:
                self.assertEqual(main([directory]), 1)
            self.assertIn("action.yml", errors.getvalue())
            self.assertEqual(path.read_text(), "runs: [")

    @patch("gh_updater.resolver.subprocess.run")
    def test_parallel_lookups_deduplicate_and_finish_before_writes(self, run):
        barrier = threading.Barrier(2)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "action.yml"
            original = (
                "runs:\n  steps:\n"
                "    - uses: owner/first@v9\n"
                "    - uses: owner/second@v9\n"
                "    - uses: owner/first/sub@v9\n"
                "    - uses: owner/excluded@v9\n"
            )
            path.write_text(original)

            def lookup(command, **kwargs):
                self.assertEqual(path.read_text(), original)
                barrier.wait(timeout=5)
                return remote_output()

            run.side_effect = lookup
            with (
                contextlib.redirect_stdout(io.StringIO()) as output,
                contextlib.redirect_stderr(io.StringIO()) as progress,
            ):
                self.assertEqual(main([directory, "--exclude", "owner/excluded"]), 0)
            self.assertEqual(run.call_count, 2)
            self.assertEqual(path.read_text().count(NEW), 3)
            self.assertIn("owner/excluded@v9", path.read_text())
            self.assertIn("Resolved [2/2]", progress.getvalue())
            self.assertIn("Checked [1/1] action.yml", progress.getvalue())
            self.assertIn("Writing [1/1] action.yml", progress.getvalue())
            self.assertNotIn("Resolved", output.getvalue())
            self.assertTrue(
                output.getvalue().endswith("Updated 1 of 1 YAML file(s).\n")
            )

    @patch("gh_updater.resolver.subprocess.run", return_value=remote_output())
    def test_log_levels_and_dry_run_progress(self, run):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "action.yml"
            original = "runs:\n  steps:\n    - uses: owner/repo@v9\n"
            path.write_text(original)
            for level in ("debug", "INFO", "WARNING", "ERROR", "CRITICAL"):
                with (
                    self.subTest(level=level),
                    contextlib.redirect_stdout(io.StringIO()) as output,
                    contextlib.redirect_stderr(io.StringIO()) as errors,
                ):
                    self.assertEqual(
                        main([directory, "--dry-run", "--log-level", level]), 0
                    )
                    self.assertEqual("DEBUG:" in errors.getvalue(), level == "debug")
                    self.assertIn("Resolved [1/1]", errors.getvalue())
                self.assertNotIn("Writing", errors.getvalue())
                self.assertIn("Would update 1 of 1", output.getvalue())
                self.assertEqual(path.read_text(), original)

    @patch("gh_updater.resolver.subprocess.run", return_value=remote_output())
    def test_workers_option_caps_at_upstream_count(self, run):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "action.yml"
            path.write_text(
                "runs:\n  steps:\n"
                "    - uses: owner/first@v9\n"
                "    - uses: owner/second@v9\n"
            )
            for workers, expected in (("1", 1), ("8", 2)):
                with (
                    self.subTest(workers=workers),
                    contextlib.redirect_stdout(io.StringIO()),
                    contextlib.redirect_stderr(io.StringIO()) as progress,
                ):
                    self.assertEqual(
                        main([directory, "--dry-run", "--workers", workers]), 0
                    )
                self.assertIn(f"with {expected} worker(s)", progress.getvalue())
                self.assertIn("Resolved [2/2]", progress.getvalue())
                self.assertIn(f"(worker {expected})", progress.getvalue())

    def test_click_help_invalid_options_and_empty_directory(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(main(["--help"]), 0)
            self.assertEqual(main(["-h"]), 0)
        self.assertIn("--log-level", output.getvalue())
        self.assertIn("--workers", output.getvalue())
        for args in (
            ["--log-level", "invalid"],
            ["--unknown"],
            [__file__],
            ["--workers", "0"],
        ):
            with (
                self.subTest(args=args),
                contextlib.redirect_stderr(io.StringIO()) as errors,
            ):
                self.assertEqual(main(args), 2)
            self.assertIn("Error:", errors.getvalue())
        with tempfile.TemporaryDirectory() as directory:
            with (
                contextlib.redirect_stdout(io.StringIO()) as output,
                contextlib.redirect_stderr(io.StringIO()) as progress,
            ):
                self.assertEqual(main([directory]), 0)
            self.assertIn("Updated 0 of 0", output.getvalue())
            self.assertIn("resolving 0 upstream(s)", progress.getvalue())

    @patch("gh_updater.resolver.subprocess.run")
    def test_resolution_failure_is_visible_at_critical_without_writes(self, run):
        def lookup(command, **kwargs):
            if command[-1] == "https://github.com/owner/branch.git":
                return subprocess.CompletedProcess(
                    [], 0, f"{NEW}\trefs/heads/main\n", ""
                )
            return remote_output()

        run.side_effect = lookup
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "action.yml"
            original = (
                "runs:\n  steps:\n"
                "    - uses: owner/repo@v9\n"
                f"    - uses: owner/branch@{OLD}\n"
            )
            path.write_text(original)
            with (
                contextlib.redirect_stdout(io.StringIO()) as output,
                contextlib.redirect_stderr(io.StringIO()) as errors,
            ):
                self.assertEqual(main([directory, "--log-level", "critical"]), 1)
            self.assertIn("gh-updater: error:", errors.getvalue())
            self.assertIn("no branch/tag hint", errors.getvalue())
            self.assertNotIn("Writing", errors.getvalue())
            self.assertEqual(output.getvalue(), "")
            self.assertEqual(path.read_text(), original)


if __name__ == "__main__":
    unittest.main()
