"""Identify complete private Semgrep rule maps despite observed registry ordering."""

import argparse
import hashlib
import json
from pathlib import Path

from ruamel.yaml import YAML


def identity(path):
    raw = path.read_bytes()
    payload = YAML(typ="safe").load(raw)
    if not isinstance(payload, dict) or set(payload) != {"rules"}:
        raise ValueError("expected rules-only vendor configuration")
    if not isinstance(payload["rules"], list) or not payload["rules"]:
        raise ValueError("expected nonempty vendor rules")
    rules = {}
    for rule in payload["rules"]:
        if not isinstance(rule, dict) or not isinstance(rule.get("id"), str) or not rule["id"]:
            raise ValueError("expected named vendor rule objects")
        if rule["id"] in rules:
            raise ValueError("duplicate vendor rule ID")
        rules[rule["id"]] = rule
    # All record fields/notices and nested list ordering remain bound. Only the
    # observed unordered unique-ID rule collection / dictionary key order differs.
    encoded = json.dumps(rules, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return {
        "raw_sha256": hashlib.sha256(raw).hexdigest(),
        "rule_map_sha256": hashlib.sha256(encoded).hexdigest(),
        "rules": len(rules),
        "bytes": len(raw),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    print(json.dumps(identity(args.path)))
