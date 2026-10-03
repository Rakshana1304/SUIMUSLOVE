"""SQLite storage for readings and alerts."""
import sqlite3, pandas as pd
from config import DB_PATH, SENSORS

def _conn():
    c = sqlite3.connect(DB_PATH, check_same_thread=False)
    return c

def init_db():
    cols = ", ".join(f"{k} REAL" for k in SENSORS)
    with _conn() as c:
        c.execute(f"CREATE TABLE IF NOT EXISTS readings (ts TEXT, {cols}, steam REAL)")
        c.execute("CREATE TABLE IF NOT EXISTS alerts (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, sensor TEXT, severity TEXT, message TEXT, acknowledged INTEGER DEFAULT 0)")

def insert_reading(ts, r):
    keys = list(SENSORS) + ["steam"]
    with _conn() as c:
        c.execute(f"INSERT INTO readings VALUES (?,{','.join('?'*len(keys))})", [ts] + [float(r[k]) for k in keys])

def read_readings(limit=None):
    q = "SELECT * FROM readings ORDER BY ts DESC" + (f" LIMIT {int(limit)}" if limit else "")
    df = pd.read_sql(q, _conn()).sort_values("ts")
    df["ts"] = pd.to_datetime(df["ts"])
    return df.reset_index(drop=True)

def insert_alert(ts, sensor, severity, message):
    with _conn() as c:
        c.execute("INSERT INTO alerts (ts,sensor,severity,message) VALUES (?,?,?,?)", (ts, sensor, severity, message))

def read_alerts():
    return pd.read_sql("SELECT * FROM alerts ORDER BY id DESC", _conn())

def active_alert_exists(sensor, severity):
    with _conn() as c:
        return c.execute("SELECT 1 FROM alerts WHERE sensor=? AND severity=? AND acknowledged=0", (sensor, severity)).fetchone() is not None

def acknowledge_all():
    with _conn() as c:
        c.execute("UPDATE alerts SET acknowledged=1")
