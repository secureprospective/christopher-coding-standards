"""Observe an exact clean/intended-rejection result on declared fixture inputs."""

import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys


def fingerprints(names: list[str]) -> dict[str, str]:
    root = Path.cwd().resolve()
    result = {}
    for name in names:
        path = Path(name)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(f"input must be a workspace-relative file: {name}")
        if not path.resolve().is_relative_to(root) or not path.is_file():
            raise ValueError(f"input must resolve to a file inside the workspace: {name}")
        result[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def output_text(value: bytes | None) -> str:
    return (value or b"").decode("utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expect", choices=["pass", "reject"], required=True)
    parser.add_argument("--diagnostic", help="required literal tool diagnostic for rejection")
    parser.add_argument("--input", action="append", required=True, dest="inputs")
    parser.add_argument("--timeout", type=float, default=120, help="direct-command seconds")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.command[:1] == ["--"]:
        args.command = args.command[1:]
    if not args.command or not math.isfinite(args.timeout) or args.timeout <= 0:
        parser.error("command and finite positive timeout are required")
    if (
        (args.expect == "reject" and (not args.diagnostic or not args.diagnostic.strip()))
        or (args.expect == "pass" and args.diagnostic is not None)
    ):
        parser.error("reject requires a nonblank diagnostic; pass takes no diagnostic")

    record = {
        "command": args.command,
        "expectation": {"exit_code": 0 if args.expect == "pass" else 1, "diagnostic": args.diagnostic},
        "timeout_seconds": args.timeout,
        "inputs_before": None,
        "inputs_after": None,
        "exit_code": None,
        "stdout": "",
        "stderr": "",
        "error": None,
        "matched": False,
    }
    try:
        record["inputs_before"] = fingerprints(args.inputs)
        completed = subprocess.run(
            args.command, stdin=subprocess.DEVNULL, capture_output=True, timeout=args.timeout
        )
        record.update(
            exit_code=completed.returncode,
            stdout=output_text(completed.stdout),
            stderr=output_text(completed.stderr),
        )
        record["inputs_after"] = fingerprints(args.inputs)
        record["matched"] = (
            completed.returncode == record["expectation"]["exit_code"]
            and record["inputs_before"] == record["inputs_after"]
            and (args.diagnostic is None or args.diagnostic in record["stdout"] + "\n" + record["stderr"])
        )
        status = 0 if record["matched"] else 1
    except (OSError, ValueError, OverflowError, subprocess.TimeoutExpired) as error:
        record["error"] = str(error)
        if isinstance(error, subprocess.TimeoutExpired):
            record.update(stdout=output_text(error.stdout), stderr=output_text(error.stderr))
        status = 2
    print(json.dumps(record, indent=2))
    return status


if __name__ == "__main__":
    sys.exit(main())
