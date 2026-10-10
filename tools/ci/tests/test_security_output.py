"""Public summaries must not publish private scanner diagnostic streams."""

from contextlib import redirect_stderr, redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    "check_security", Path(__file__).resolve().parents[1] / "check-security.py"
)
assert SPEC is not None and SPEC.loader is not None
SECURITY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SECURITY)


class SecurityOutputTests(unittest.TestCase):
    def captured(self, status=0, matched=True):
        original = {"exit_code": status, "matched": matched, "stdout": "private diagnostic canary"}
        return original, subprocess.CompletedProcess(
            ["verifier"], 0 if matched else 1, json.dumps(original) + "\n", "private stderr canary"
        )

    def private_observation(self, status):
        original, result = self.captured(status)
        output, errors = io.StringIO(), io.StringIO()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "observation.json"
            with patch.object(SECURITY.subprocess, "run", return_value=result):
                with redirect_stdout(output), redirect_stderr(errors):
                    actual = SECURITY.observe(Path(directory), ["scanner"], [], private_record=path)
            self.assertEqual(actual, original)
            private = json.loads(path.read_text())
            self.assertEqual(private, {"checker_exit": 0, "stdout": result.stdout, "stderr": result.stderr})
            summary = json.loads(output.getvalue())
            self.assertEqual(summary["checker_exit"], 0)
            self.assertEqual(summary["sha256"], SECURITY.hashlib.sha256(path.read_bytes()).hexdigest())
            self.assertEqual(summary["private_observation"], str(path.resolve()))
        self.assertNotIn("canary", output.getvalue() + errors.getvalue())

    def test_private_clean_preserves_result(self):
        self.private_observation(0)

    def test_private_expected_rejection_preserves_status_one(self):
        self.private_observation(1)

    def test_failed_expectation_stays_failed_and_private(self):
        original, result = self.captured(2, False)
        output, errors = io.StringIO(), io.StringIO()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "observation.json"
            with patch.object(SECURITY.subprocess, "run", return_value=result):
                with redirect_stdout(output), redirect_stderr(errors):
                    with self.assertRaisesRegex(RuntimeError, "checker exit 1"):
                        SECURITY.observe(Path(directory), ["scanner"], [], private_record=path)
            private = json.loads(path.read_text())
            self.assertEqual(json.loads(private["stdout"]), original)
            self.assertEqual(private["checker_exit"], 1)
        self.assertNotIn("canary", output.getvalue() + errors.getvalue())

    def test_inside_checkout_rejected_before_command(self):
        with patch.object(SECURITY.subprocess, "run") as command:
            with self.assertRaisesRegex(ValueError, "outside the checkout"):
                SECURITY.observe(SECURITY.ROOT, ["scanner"], [], private_record=SECURITY.ROOT / "probe.json")
            command.assert_not_called()

    def test_existing_private_record_not_overwritten(self):
        _, result = self.captured()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "observation.json"
            path.write_text("keep original")
            with patch.object(SECURITY.subprocess, "run", return_value=result):
                with self.assertRaises(FileExistsError):
                    SECURITY.observe(Path(directory), ["scanner"], [], private_record=path)
            self.assertEqual(path.read_text(), "keep original")

    def test_default_public_output_contract_unchanged(self):
        original, result = self.captured()
        output, errors = io.StringIO(), io.StringIO()
        with patch.object(SECURITY.subprocess, "run", return_value=result):
            with redirect_stdout(output), redirect_stderr(errors):
                self.assertEqual(SECURITY.observe(SECURITY.ROOT, ["scanner"], []), original)
        self.assertEqual(output.getvalue(), result.stdout)
        self.assertEqual(errors.getvalue(), result.stderr)


if __name__ == "__main__":
    unittest.main()
