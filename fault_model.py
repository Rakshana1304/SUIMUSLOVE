"""Isolation Forest (anomaly) + Random Forest (fault type), trained on SYNTHETIC data."""
import numpy as np, pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from config import SENSORS

KEYS = list(SENSORS)
CLASSES = ["normal"] + [f"{k}_fault" for k in KEYS]
ACTIONS = {"temperature": "Inspect burner, fuel feed and cooling loop.", "pressure": "Check safety valve and pressure gauge.",
 "vibration": "Inspect pump/bearing alignment and mounts.", "water_level": "Check feed-water pump and level probe.",
 "flow": "Inspect valves and pipe for blockage or leaks.", "efficiency": "Check scale build-up and combustion tuning."}

def features(df):
    X = df[KEYS].copy()
    X["temp_pressure"] = df["temperature"] / df["pressure"].clip(lower=0.1)  # engineered ratio
    X["flow_eff"] = df["flow"] * df["efficiency"] / 100
    return X

def _synth(n, rng):
    rows, y = [], []
    for i, cls in enumerate(CLASSES):
        for _ in range(n):
            r = {k: rng.normal(c["nominal"], c["noise"] * 3) for k, c in SENSORS.items()}
            if i: k = KEYS[i - 1]; r[k] = rng.normal(SENSORS[k]["fault"], SENSORS[k]["noise"] * 4)
            rows.append(r); y.append(i)
    return pd.DataFrame(rows).clip(lower=0), np.array(y)

def train(seed=42):
    rng = np.random.default_rng(seed)
    df, y = _synth(400, rng)
    Xtr, Xte, ytr, yte = train_test_split(features(df), y, test_size=0.25, stratify=y, random_state=seed)
    sc = StandardScaler().fit(Xtr)
    iso = IsolationForest(n_estimators=200, contamination=0.05, random_state=seed).fit(sc.transform(Xtr[ytr == 0]))
    rf = RandomForestClassifier(n_estimators=150, random_state=seed).fit(sc.transform(Xtr), ytr)
    iso_pred = (iso.predict(sc.transform(Xte)) == -1).astype(int)
    rep = classification_report(yte, rf.predict(sc.transform(Xte)), target_names=CLASSES, output_dict=True, zero_division=0)
    iso_rep = classification_report((yte > 0).astype(int), iso_pred, target_names=["normal", "fault"], output_dict=True, zero_division=0)
    return dict(sc=sc, iso=iso, rf=rf, rf_report=rep, iso_report=iso_rep)

def predict(m, df):
    X = m["sc"].transform(features(df))
    out = df[["ts"]].copy() if "ts" in df else pd.DataFrame(index=df.index)
    out["score"] = m["iso"].decision_function(X)
    out["anomaly"] = m["iso"].predict(X) == -1
    out["fault"] = [CLASSES[i] for i in m["rf"].predict(X)]
    out["severity"] = np.where(~out["anomaly"], "none", np.where(out["score"] < -0.15, "critical", "warning"))
    return out
