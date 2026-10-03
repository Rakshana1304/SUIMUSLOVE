import streamlit as st, plotly.express as px
from config import SENSORS
from utils.alerts import status_of
import database as db, styles

def render(df, latest):
    styles.header("Dashboard", "Live overview of boiler operations")
    st.markdown("<span class='note'>Simulated data — not connected to real IoT sensors</span><br><br>", unsafe_allow_html=True)
    keys = ["temperature", "vibration", "pressure", "efficiency"]
    icons = {"temperature": "🌡️", "vibration": "📳", "pressure": "⏲️", "efficiency": "⚡"}
    for col, k in zip(st.columns(4), keys):
        c = SENSORS[k]
        col.markdown(styles.kpi(c["name"], f"{latest[k]:.1f}", c["unit"], icons[k], status_of(k, latest[k])), unsafe_allow_html=True)
    a, b = st.columns(2)
    d = df.tail(150)
    with a: styles.chart(px.line(d, x="ts", y="temperature", title="Temperature (°C)"), "d1")
    with b: styles.chart(px.line(d, x="ts", y="pressure", title="Pressure (bar)"), "d2")
    a, b = st.columns(2)
    with a: styles.chart(px.line(d, x="ts", y="vibration", title="Vibration (mm/s)"), "d3")
    with b: styles.chart(px.area(d, x="ts", y="steam", title="Steam output (t/h)"), "d4")
    l, r = st.columns([1, 1])
    sts = {k: status_of(k, latest[k]) for k in SENSORS}
    l.markdown("<div class='card'><b>Sensor summary</b>" + "".join(
        f"<div class='alert-row'>{SENSORS[k]['icon']} {SENSORS[k]['name']}<b style='margin-left:auto'>{latest[k]:.1f} {SENSORS[k]['unit']}</b>{styles.pill(s, 'Normal' if s=='ok' else None)}</div>" for k, s in sts.items()) + "</div>", unsafe_allow_html=True)
    al = db.read_alerts().head(6)
    rows = "".join(f"<div class='alert-row'>{styles.pill(x.severity)} {x.message}<small>{str(x.ts)[11:19]}</small></div>" for x in al.itertuples()) or "<div class='alert-row'>No alerts yet — all systems normal.</div>"
    r.markdown(f"<div class='card'><b>Recent alerts</b>{rows}</div>", unsafe_allow_html=True)
