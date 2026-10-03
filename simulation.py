"""Bounded simulated boiler sensors (NOT real IoT data). Simplified coupling, not validated physics."""
import numpy as np
from config import SENSORS

def initial_state():
    s = {k: float(c["nominal"]) for k, c in SENSORS.items()}
    s["steam"] = steam_output(s)
    return s

def steam_output(r):
    # Simplified: steam ~ inflow * efficiency * water-availability factor
    return float(r["flow"] * r["efficiency"] / 100 * 0.55 * min(1, r["water_level"] / 40))

def step(prev, faults, rng, setpoint_temp=180, load=1.0):
    new = {}
    for k, c in SENSORS.items():
        target = c["fault"] if k in faults else c["nominal"]
        if k == "temperature" and k not in faults: target = setpoint_temp
        if k == "flow" and k not in faults: target = c["nominal"] * load
        if k == "pressure" and k not in faults:  # pressure follows temperature
            target = c["nominal"] + 0.04 * (new["temperature"] - 180)
        v = prev[k] + 0.25 * (target - prev[k]) + rng.normal(0, c["noise"])
        new[k] = float(np.clip(v, c["lo"], c["hi"]))  # no impossible values
    new["steam"] = steam_output(new)
    return new
