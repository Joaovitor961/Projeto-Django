import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / 'db.sqlite3'

if not DB_PATH.exists():
    print(f"Database not found at {DB_PATH}")
    raise SystemExit(1)

conn = sqlite3.connect(str(DB_PATH))
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Get tables
cur.execute("SELECT name, type, tbl_name, sql FROM sqlite_master WHERE type IN ('table','view') AND name NOT LIKE 'sqlite_%' ORDER BY name;")
objects = cur.fetchall()

result = {
    'db_path': str(DB_PATH),
    'objects': []
}

for obj in objects:
    name = obj['name']
    typ = obj['type']
    sql = obj['sql']
    info = {'name': name, 'type': typ, 'sql': sql, 'count': None, 'columns': [], 'sample_rows': []}

    # Try to get row count
    try:
        cur.execute(f"SELECT COUNT(*) as cnt FROM '{name}'")
        info['count'] = cur.fetchone()['cnt']
    except Exception as e:
        info['count'] = f"error: {e}"

    # columns
    try:
        cur.execute(f"PRAGMA table_info('{name}')")
        cols = [row['name'] for row in cur.fetchall()]
        info['columns'] = cols
    except Exception:
        info['columns'] = []

    # sample rows
    try:
        cur.execute(f"SELECT * FROM '{name}' LIMIT 10")
        rows = cur.fetchall()
        for r in rows:
            info['sample_rows'].append({k: (None if r[k] is None else (str(r[k]) if not isinstance(r[k], (int, float)) else r[k])) for k in r.keys()})
    except Exception as e:
        info['sample_rows'] = [f"error: {e}"]

    result['objects'].append(info)

print(json.dumps(result, indent=2, ensure_ascii=False))
conn.close()
