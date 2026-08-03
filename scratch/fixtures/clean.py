"""Clean fixture: must pass ruff (E/F/I/UP/B/S/C4/PIE/SIM/RET/ARG/PTH), mypy
strict, and gitleaks. Exercise the overlay's expectations so a correct
configuration passes a correct file — no SQL injection, no untyped def,
no secrets.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path


def load_player(conn: sqlite3.Connection, player_id: str) -> tuple[int, str]:
    """Parameterized query — the S608-safe way to touch the database."""
    row = conn.execute(
        "SELECT id, name FROM players WHERE id = ?", (player_id,)
    ).fetchone()
    if row is None:
        raise ValueError(f"no player with id {player_id!r}")
    return int(row[0]), str(row[1])


def whitelist_path(raw: str) -> Path:
    """Example AWS key below is NOT present — this file carries no secrets."""
    candidate = Path(raw)
    return candidate.resolve()