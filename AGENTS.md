# Base44 Dev Environment — XEN Miner

## Project Overview
Python/Flask proof-of-work mining infrastructure for the XEN blockchain (Argon2ID).
The main web component is `gpage.py` — a Flask app serving a miner leaderboard,
hash-rate stats, and mining API endpoints (`/verify`, `/validate`, `/difficulty`).

## Architecture
- **`gpage.py`** — Main Flask web app (port 3000). Routes: `/leaderboard`, `/hash_rate`,
  `/difficulty`, `/verify`, `/validate`, `/total_blocks`, `/get_xuni_counts`, etc.
  Uses Jinja2 templates in `templates/`.
- **`rpc_server.py`** — Separate Flask JSON-RPC server mimicking an Ethereum node (port 5555).
  Not started by default; has extra deps (`web3`, `ethereum`, `rlp`, `coincurve`) not in requirements.txt.
- **`miner.py`** — CLI mining script (not a server). Connects to remote `xenminer.mooo.com`.
- **`syncnode.py`** — CLI block sync script.
- **`indexing/`** — Background indexing/maintenance scripts.
- **`init_db.py`** — Creates and seeds the SQLite databases (`blocks.db`, `difficulty.db`, `cache.db`)
  with schema + sample data. Run before starting the app. Idempotent.

## Databases (SQLite, file-based)
- `blocks.db` — tables: `blocks`, `xuni`, `account_attempts`, `consensus`, `account_performance`, `super_blocks`
- `difficulty.db` — tables: `difficulty`, `difficulty_table`, `blockrate`, `miners`
- `cache.db` — table: `cache_table` (leaderboard cache)

## Running
```bash
docker compose -f docker-compose.base44.yml up -d
```
The `init-db` one-shot service creates/seeds databases first, then `web` starts Flask on port 3000
with `--reload` (live reload on file changes).

## Notes
- `gpage.py` defines `app = Flask(__name__)` twice; the second instance is the live one.
- `gpage.py` has no `app.run()` — started via `flask --app gpage run` CLI.
- `requirements.txt` originally omitted `flask` (added during setup).
- Templates `leaderboard4.html` and `hash_rate.html` were created during setup (referenced but missing).
- No external secrets or credentials required — all data is local SQLite.
