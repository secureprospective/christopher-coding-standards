"""Checker contract tests; simulated tool results are not real linter evidence."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


CHECKER = Path(__file__).resolve().parents[1] / "verify_fixture.py"


class VerifyFixtureTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory(prefix="fixture-checker-test-")
        self.addCleanup(self.workspace.cleanup)
        self.root = Path(self.workspace.name)
        self.source = self.root / "fixture.txt"
        self.source.write_text("public fixture\n")

    def invoke(self, code="", expect="pass", diagnostic=None, inputs=None, timeout="5"):
        args = [sys.executable, str(CHECKER), "--expect", expect, "--timeout", timeout]
        for name in inputs if inputs is not None else ["fixture.txt"]:
            args += ["--input", name]
        if diagnostic is not None:
            args += ["--diagnostic", diagnostic]
        args += ["--", sys.executable, "-c", code]
        completed = subprocess.run(args, cwd=self.root, capture_output=True, text=True, timeout=10)
        return completed, json.loads(completed.stdout) if completed.stdout else None

    def test_clean_exit_and_input_identity(self):
        completed, record = self.invoke("print('observed output')")
        self.assertEqual(completed.returncode, 0)
        self.assertTrue(record["matched"])
        self.assertEqual(record["stdout"], "observed output\n")
        expected = {"fixture.txt": hashlib.sha256(self.source.read_bytes()).hexdigest()}
        self.assertEqual(record["inputs_before"], expected)
        self.assertEqual(record["inputs_after"], expected)

    def test_intended_rejection(self):
        completed, record = self.invoke("print('SC2086 (info):'); raise SystemExit(1)", "reject", "SC2086 (info):")
        self.assertEqual(completed.returncode, 0)
        self.assertTrue(record["matched"])
        self.assertEqual(record["exit_code"], 1)

    def test_rejection_diagnostic_can_be_on_stderr(self):
        completed, record = self.invoke("import sys; print('SC2086 (info):', file=sys.stderr); sys.exit(1)", "reject", "SC2086 (info):")
        self.assertEqual(completed.returncode, 0)
        self.assertIn("SC2086 (info):", record["stderr"])

    def test_wrong_exit_or_missing_diagnostic_is_not_rejection(self):
        cases = [("print('SC2086 (info):')", 0),
                 ("print('SC2086 (info):'); raise SystemExit(2)", 2),
                 ("print('configuration error'); raise SystemExit(1)", 1)]
        for code, exit_code in cases:
            with self.subTest(code=code):
                completed, record = self.invoke(code, "reject", "SC2086 (info):")
                self.assertEqual(completed.returncode, 1)
                self.assertFalse(record["matched"])
                self.assertEqual(record["exit_code"], exit_code)

    def test_clean_nonzero_is_failure(self):
        completed, record = self.invoke("raise SystemExit(1)")
        self.assertEqual(completed.returncode, 1)
        self.assertFalse(record["matched"])

    def test_missing_executable_is_setup_failure_not_rejection(self):
        completed = subprocess.run(
            [sys.executable, str(CHECKER), "--expect", "reject", "--diagnostic", "SC2086",
             "--input", "fixture.txt", "--", str(self.root / "missing-tool")],
            cwd=self.root, capture_output=True, text=True, timeout=10,
        )
        record = json.loads(completed.stdout)
        self.assertEqual(completed.returncode, 2)
        self.assertFalse(record["matched"])
        self.assertIsNone(record["exit_code"])
        self.assertIsNotNone(record["error"])

    def test_missing_directory_absolute_and_parent_inputs_rejected(self):
        for name in ["absent.txt", ".", str(self.source), "../fixture.txt"]:
            with self.subTest(name=name):
                completed, record = self.invoke(inputs=[name])
                self.assertEqual(completed.returncode, 2)
                self.assertFalse(record["matched"])
                self.assertIsNone(record["exit_code"])

    def test_symlink_escape_rejected(self):
        with tempfile.TemporaryDirectory(prefix="outside-fixture-test-") as outside:
            target = Path(outside) / "public.txt"
            target.write_text("another owned test fixture\n")
            (self.root / "escape.txt").symlink_to(target)
            completed, record = self.invoke(inputs=["escape.txt"])
            self.assertEqual(completed.returncode, 2)
            self.assertFalse(record["matched"])

    def test_mutation_invalidates_either_expected_result(self):
        mutation = "from pathlib import Path; Path('fixture.txt').write_text('changed')"
        for expect, suffix, diagnostic in [("pass", "", None),
                                           ("reject", "; print('SC2086'); raise SystemExit(1)", "SC2086")]:
            with self.subTest(expect=expect):
                self.source.write_text("public fixture\n")
                completed, record = self.invoke(mutation + suffix, expect, diagnostic)
                self.assertEqual(completed.returncode, 1)
                self.assertFalse(record["matched"])
                self.assertNotEqual(record["inputs_before"], record["inputs_after"])

    def test_deleted_input_is_setup_failure(self):
        completed, record = self.invoke("from pathlib import Path; Path('fixture.txt').unlink()")
        self.assertEqual(completed.returncode, 2)
        self.assertFalse(record["matched"])
        self.assertIsNotNone(record["error"])

    def test_timeout_preserves_partial_output_and_cannot_pass(self):
        completed, record = self.invoke("import time; print('SC2086', flush=True); time.sleep(2)", "reject", "SC2086", timeout="0.3")
        self.assertEqual(completed.returncode, 2)
        self.assertFalse(record["matched"])
        self.assertIsNone(record["exit_code"])
        self.assertIn("SC2086", record["stdout"])
        self.assertIsNotNone(record["error"])

    def test_non_utf8_output_is_replaced_not_silently_dropped(self):
        completed, record = self.invoke("import sys; sys.stdout.buffer.write(b'\\xff')")
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(record["stdout"], "\ufffd")

    def test_closed_stdin(self):
        completed, record = self.invoke("import sys; print(repr(sys.stdin.read()))")
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(record["stdout"], "''\n")

    def test_invalid_timeout_and_diagnostic_options_are_usage_errors(self):
        for timeout in ["0", "-1", "nan", "inf"]:
            with self.subTest(timeout=timeout):
                completed, record = self.invoke(timeout=timeout)
                self.assertEqual(completed.returncode, 2)
                self.assertIsNone(record)
        for expect, diagnostic in [("reject", None), ("reject", " "), ("pass", "unexpected")]:
            with self.subTest(expect=expect, diagnostic=diagnostic):
                completed, record = self.invoke(expect=expect, diagnostic=diagnostic)
                self.assertEqual(completed.returncode, 2)
                self.assertIsNone(record)


if __name__ == "__main__":
    unittest.main()
