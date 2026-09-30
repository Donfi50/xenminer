"""
Initialize SQLite databases required by gpage.py with schema and sample data.
Run once before starting the Flask app. Idempotent — safe to re-run.
"""
import sqlite3
import os
import hashlib
import random
import string

DB_DIR = os.path.dirname(os.path.abspath(__file__))


def conn(name):
    path = os.path.join(DB_DIR, name)
    return sqlite3.connect(path)


def init_blocks_db():
    c = conn("blocks.db")
    cur = c.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS blocks (
        block_id INTEGER PRIMARY KEY AUTOINCREMENT,
        hash_to_verify TEXT,
        key TEXT UNIQUE,
        account TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS xuni (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        hash_to_verify TEXT,
        key TEXT,
        account TEXT,
        date DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS account_attempts (
        account TEXT,
        timestamp TEXT,
        attempts INTEGER
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS consensus (
        total_count INTEGER,
        my_ethereum_address TEXT,
        last_block_id INTEGER,
        last_block_hash TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS account_performance (
        account TEXT PRIMARY KEY,
        hashes_per_second REAL
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS super_blocks (
        account TEXT,
        super_block_count INTEGER
    )""")

    # Seed sample data if empty
    cur.execute("SELECT COUNT(*) FROM blocks")
    if cur.fetchone()[0] == 0:
        sample_accounts = [
            "0x0A6969ffF003B760c97005e03ff5a9741126167A",
            "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1",
            "0x1234567890abcdef1234567890abcdef12345678",
            "0xabcdef1234abcd1234abcd1234abcd1234abcd12",
            "0xdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef",
        ]
        for i in range(1, 201):
            acct = random.choice(sample_accounts)
            key = hashlib.sha256(str(random.random()).encode()).hexdigest()
            cur.execute(
                "INSERT OR IGNORE INTO blocks (hash_to_verify, key, account, created_at) VALUES (?, ?, ?, datetime('now', '-' || ? || ' minutes'))",
                (f"$argon2id$v=19$m=1500,t=1,p=1$WEVOMTAwODIwMjJYRU4${'a' * 64}", key, acct, random.randint(0, 1440)),
            )

    cur.execute("SELECT COUNT(*) FROM account_attempts")
    if cur.fetchone()[0] == 0:
        sample_accounts = [
            "0x0a6969fff003b760c97005e03ff5a9741126167a",
            "0x742d35cc6634c0532925a3b844bc9e7595f0beb1",
            "0x1234567890abcdef1234567890abcdef12345678",
        ]
        for i in range(100):
            acct = random.choice(sample_accounts)
            cur.execute(
                "INSERT INTO account_attempts (account, timestamp, attempts) VALUES (?, datetime('now', '-' || ? || ' minutes'), ?)",
                (acct, random.randint(0, 120), random.randint(1000, 50000)),
            )

    c.commit()
    c.close()


def init_difficulty_db():
    c = conn("difficulty.db")
    cur = c.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS difficulty (
        level INTEGER
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS difficulty_table (
        account TEXT,
        difficulty TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS blockrate (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATETIME DEFAULT CURRENT_TIMESTAMP,
        rate REAL
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS miners (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATETIME DEFAULT CURRENT_TIMESTAMP,
        total_miners INTEGER
    )""")

    cur.execute("SELECT COUNT(*) FROM difficulty")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO difficulty (level) VALUES (1500)")

    cur.execute("SELECT COUNT(*) FROM blockrate")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO blockrate (rate) VALUES (1.0)")

    cur.execute("SELECT COUNT(*) FROM miners")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO miners (total_miners) VALUES (42)")

    c.commit()
    c.close()


def init_cache_db():
    c = conn("cache.db")
    cur = c.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS cache_table (
        account TEXT,
        total_blocks INTEGER,
        hashes_per_second REAL,
        super_blocks INTEGER
    )""")

    cur.execute("SELECT COUNT(*) FROM cache_table")
    if cur.fetchone()[0] == 0:
        sample_miners = [
            ("0x0a6969fff003b760c97005e03ff5a9741126167a", 15234, 12500.5, 15),
            ("0x742d35cc6634c0532925a3b844bc9e7595f0beb1", 12087, 9800.3, 12),
            ("0x1234567890abcdef1234567890abcdef12345678", 9856, 8200.0, 9),
            ("0xabcdef1234abcd1234abcd1234abcd1234abcd12", 7234, 6500.7, 7),
            ("0xdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef", 5421, 4800.2, 5),
            ("0xcafecafecafecafecafecafecafecafecafecafe", 3890, 3100.0, 3),
            ("0x1111111111111111111111111111111111111111", 2100, 1800.5, 2),
            ("0x2222222222222222222222222222222222222222", 1500, 1200.0, 1),
        ]
        cur.executemany(
            "INSERT INTO cache_table (account, total_blocks, hashes_per_second, super_blocks) VALUES (?, ?, ?, ?)",
            sample_miners,
        )

    c.commit()
    c.close()


if __name__ == "__main__":
    print("Initializing blocks.db...")
    init_blocks_db()
    print("Initializing difficulty.db...")
    init_difficulty_db()
    print("Initializing cache.db...")
    init_cache_db()
    print("All databases initialized successfully.")
