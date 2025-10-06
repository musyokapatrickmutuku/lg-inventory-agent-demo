# init_db.py
"""
Initializes the SQLite database for the LG TV Inventory Demo Agent.
Creates both the inventory and emails tables (with 'explanation' column).
Populates sample inventory data from the provided LG list.
"""

import sqlite3
from datetime import datetime
import os

ROOT = os.path.dirname(__file__)
DB_PATH = os.path.join(ROOT, "demo.db")

# === Inventory seed data ===
inventory_rows = [
    ("MGT001", "32LR60006LA", "LED LCD TV 32 (O/S, FHD)", "TV-LED", 71.11, 4),
    ("MGT002", "32LQ63006LA", "LED LCD TV 32 (O/S, HD)", "TV-LED", 95.67, 1),
    ("MGT003", "43LQ60006LA", "LED LCD TV 43 (O/S, FHD)", "TV-LED", 120.24, 3),
    ("MGT004", "43NANO81A6A", "LED NanoCell 43 (Smart)", "TV-LED", 125.40, 1),
    ("MGT005", "43NANO81T6A", "LED NanoCell 43T (Smart)", "TV-LED", 177.12, 2),
    ("MGT006", "50NANO80A6B", "NanoCell 50 (Smart)", "TV-LED", 187.46, 1),
    ("MGT007", "50NANO90A6B", "NanoCell 50 (Higher spec)", "TV-LED", 157.73, 1),
    ("MGT008", "50UA73006LA", "LED 50 (UA Series)", "TV-LED", 187.46, 2),
    ("MGT009", "55UA73006LA", "LED 55 (UA Series)", "TV-LED", 199.09, 2),
    ("MGT010", "55QNED87A6B", "Qned 55 (High end)", "TV-LED", 266.32, 1),
    ("MGT011", "65UA73006LA", "LED 65 (UA Series)", "TV-LED", 255.98, 1),
    ("MGT012", "65UR78006LK", "LED 65 (UR Series)", "TV-LED", 249.52, 3),
    ("MGT013", "65QNED91T6A", "Qned 65 (Premium)", "TV-LED", 575.29, 1),
    ("MGT014", "75QNED93A6A", "Qned 75 (Flagship)", "TV-LED", 884.26, 1),
]

def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # === Create inventory table ===
    c.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        mgt_no TEXT PRIMARY KEY,
        model TEXT,
        model_name TEXT,
        division TEXT,
        resale_price REAL,
        total_qty INTEGER,
        last_updated TEXT
    )
    """)

    # === Create emails table with explanation ===
    c.execute("""
    CREATE TABLE IF NOT EXISTS emails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        subject TEXT,
        sender TEXT,
        body TEXT,
        label TEXT,
        confidence REAL,
        explanation TEXT,
        processed_at TEXT
    )
    """)

    now = datetime.utcnow().isoformat()
    for row in inventory_rows:
        c.execute("""
           INSERT OR REPLACE INTO inventory
           (mgt_no, model, model_name, division, resale_price, total_qty, last_updated)
           VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (*row, now))

    conn.commit()
    conn.close()
    print(f"✅ Database initialized successfully: {DB_PATH}")

if __name__ == "__main__":
    main()
