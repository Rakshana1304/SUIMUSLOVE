"""Threshold status + de-duplicated alert generation."""
from config import SENSORS
import database as db

def status_of(key, v):
    c = SENSORS[key]
    bad = (lambda t: v >= t) if c["mode"] == "high" else (lambda t: v <= t)
    return "critical" if bad(c["crit"]) else "warning" if bad(c["warn"]) else "ok"

def check(ts, reading):
    for k, v in reading.items():
        if k not in SENSORS: continue
        s = status_of(k, v)
        if s != "ok" and not db.active_alert_exists(k, s):  # one open alert per sensor+severity
            db.insert_alert(ts, k, s, f"{SENSORS[k]['name']} {v:.1f} {SENSORS[k]['unit']} crossed {s} threshold")
