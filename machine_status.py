import streamlit as st
from config import SENSORS
from utils.alerts import status_of
import styles

NAMES = ["Boiler 1", "Boiler 2", "Pump 1", "Pump 2", "Generator 1", "Generator 2"]
ICON = {"Boiler": "🔥", "Pump": "🌀", "Generator": "⚡"}

def render(df, latest):
    styles.header("Machine Status", "Equipment health at a glance")
    st.caption("Demo: all machines share one simulated feed with small offsets; Pump 2 is shown as Maintenance.")
    sts = [status_of(k, latest[k]) for k in SENSORS]
    n_alerts = sts.count("warning") + sts.count("critical")
    base = "critical" if "critical" in sts else "warning" if "warning" in sts else "ok"
    for i, n in enumerate(NAMES):
        if i % 3 == 0: cols = st.columns(3)
        s, label = ("maint", "Maintenance") if n == "Pump 2" else (base, {"ok": "Running", "warning": "Warning", "critical": "Fault"}[base])
        eff = latest["efficiency"] * (1 - 0.03 * i)
        cols[i % 3].markdown(f"""<div class='card'><div style='display:flex;justify-content:space-between'><b>{ICON[n.split()[0]]} {n}</b>{styles.pill(s, label)}</div>
        <div style='margin-top:.8rem;font-size:.85rem;color:#64748b'>Efficiency <b style='color:#0f172a'>{eff:.1f}%</b></div><div class='bar'><i style='width:{eff:.0f}%'></i></div>
        <div style='margin-top:.8rem;font-size:.85rem;color:#64748b'>Temp {latest['temperature']*(1-0.03*i):.0f} °C · Pressure {latest['pressure']:.1f} bar · Vibration {latest['vibration']:.1f} mm/s</div>
        <div style='margin-top:.6rem;font-size:.8rem'>Active alerts: <b>{0 if n=='Pump 2' else n_alerts}</b></div></div>""", unsafe_allow_html=True)
