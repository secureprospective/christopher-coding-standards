"""Own synthetic normalization controls, not vendor rules or Semgrep execution."""

import json
from pathlib import Path
import tempfile
import unittest

from rules_identity import identity


class RulesIdentityTests(unittest.TestCase):
    def observe(self, value):
        with tempfile.TemporaryDirectory(prefix="bee-rule-identity-") as directory:
            path = Path(directory) / "own-config.yml"
            path.write_text(json.dumps(value))  # JSON is a YAML subset.
            return identity(path)

    def test_rule_and_dictionary_order_only(self):
        a = {"rules": [{"id": "a", "pattern": "own-a"}, {"id": "b", "pattern": "own-b"}]}
        b = {"rules": [{"pattern": "own-b", "id": "b"}, {"pattern": "own-a", "id": "a"}]}
        x, y = self.observe(a), self.observe(b)
        self.assertNotEqual(x["raw_sha256"], y["raw_sha256"])
        self.assertEqual(x["rule_map_sha256"], y["rule_map_sha256"])
        self.assertEqual(x["rules"], 2)

    def test_pattern_change_is_not_normalized(self):
        a = self.observe({"rules": [{"id": "a", "pattern": "own-a"}]})
        b = self.observe({"rules": [{"id": "a", "pattern": "own-b"}]})
        self.assertNotEqual(a["rule_map_sha256"], b["rule_map_sha256"])

    def test_notice_change_is_not_normalized(self):
        a = self.observe({"rules": [{"id": "a", "metadata": {"license": "own-notice-a"}}]})
        b = self.observe({"rules": [{"id": "a", "metadata": {"license": "own-notice-b"}}]})
        self.assertNotEqual(a["rule_map_sha256"], b["rule_map_sha256"])

    def test_nested_list_order_is_not_normalized(self):
        a = self.observe({"rules": [{"id": "a", "patterns": ["own-a", "own-b"]}]})
        b = self.observe({"rules": [{"id": "a", "patterns": ["own-b", "own-a"]}]})
        self.assertNotEqual(a["rule_map_sha256"], b["rule_map_sha256"])

    def test_duplicate_ids_fail(self):
        with self.assertRaisesRegex(ValueError, "duplicate vendor rule ID"):
            self.observe({"rules": [{"id": "a"}, {"id": "a"}]})

    def test_missing_empty_or_extra_configuration_fails(self):
        for value in [{}, {"rules": []}, {"rules": [{"id": "a"}], "extra": True}]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.observe(value)

    def test_observed_zero_miss_wrapper_preserves_complete_rule_identity(self):
        rules = [{"id": "a", "metadata": {"license": "own-notice"}, "patterns": ["x", "y"]}]
        plain = self.observe({"rules": rules})
        wrapped = self.observe({"rules": rules, "missed": 0})
        self.assertEqual(plain["rule_map_sha256"], wrapped["rule_map_sha256"])
        self.assertNotEqual(plain["raw_sha256"], wrapped["raw_sha256"])
        self.assertIsNone(plain["registry_missed"])
        self.assertEqual(wrapped["registry_missed"], 0)

    def test_nonzero_or_untyped_registry_misses_fail(self):
        for value in [1, -1, False, True, 0.0, None, "0", [], {}]:
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "zero registry misses"):
                self.observe({"rules": [{"id": "a"}], "missed": value})

    def test_non_string_id_fails(self):
        with self.assertRaisesRegex(ValueError, "named vendor rule objects"):
            self.observe({"rules": [{"id": 1}]})


if __name__ == "__main__":
    unittest.main()
