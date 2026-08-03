"""Deliberately-violating fixture: must FAIL the guardrails so a working CI
job can tell the difference from the clean fixture.

Two planted violations, each targeting a different guardrail in the Python
overlay:
  1. SQL-injection-shaped string concatenation -> ruff S608 (flake8-bandit).
  2. An untyped def                             -> mypy strict (disallow_untyped_defs).

No real-looking secret lives in this tree, so gitleaks passes on this file;
only ruff S608 and mypy strict should fail it.
"""

import sqlite3


def fetch_player_sql(conn, player_id):
    # implant: dynamic SQL built by string concatenation
    query = "SELECT * FROM players WHERE id = '" + player_id + "'"
    return conn.execute(query).fetchall()