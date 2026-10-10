"""Model runner per-line prepend semantics, not hosted execution itself."""

import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    "install_tools", Path(__file__).resolve().parents[1] / "install-tools.py"
)
assert SPEC is not None and SPEC.loader is not None
INSTALL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INSTALL)


class GithubEnvironmentTests(unittest.TestCase):
    def test_path_priority_matches_selected_environment(self):
        with tempfile.TemporaryDirectory() as directory:
            paths, environment = Path(directory) / "path", Path(directory) / "env"
            wanted = ["/owned/go with spaces/bin", "/owned/tools/bin", "/runner/older/go/bin", "/usr/bin"]
            selected = {"PATH": os.pathsep.join(wanted), "GOROOT": "/owned/go with spaces", "GOTOOLCHAIN": "local"}
            with patch.dict(os.environ, {"GITHUB_PATH": str(paths), "GITHUB_ENV": str(environment)}):
                INSTALL.github_environment(selected)
            actual = []
            for entry in paths.read_text().splitlines():
                actual.insert(0, entry)
            self.assertEqual(actual, wanted)
            self.assertEqual(environment.read_text(), "GOROOT=/owned/go with spaces\nGOTOOLCHAIN=local\n")
            # Original forward emission would select the inherited paths first.
            self.assertNotEqual(list(reversed(wanted))[0], wanted[0])

    def test_without_github_files_does_not_publish_environment(self):
        with patch.dict(os.environ, {}, clear=True):
            INSTALL.github_environment({"PATH": "/owned/bin:/usr/bin", "GOROOT": "/owned/go"})


if __name__ == "__main__":
    unittest.main()
