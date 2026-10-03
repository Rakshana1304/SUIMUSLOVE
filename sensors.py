import streamlit as st, plotly.express as px
from config import SENSORS
from utils.alerts import status_of
import styles

def render(df, latest):
    styles.header("Sensor Monitoring", "Readings, thresholds and test controls")
    for i, (k, c) in enumerate(SENSORS.items()):
        if i % 3 == 0: cols = st.columns(3)
        s = status_of(k, latest[k])
        cols[i % 3].markdown(styles.kpi(c["name"], f"{latest[k]:.1f}", c["unit"], c["icon"], s) + f"<div style='margin:-.6rem 0 1rem 1.2rem;font-size:.75rem;color:#94a3b8'>Updated {df['ts'].iloc[-1]:%H:%M:%S} · simulated</div>", unsafe_allow_html=True)
    k = st.selectbox("Sensor history", list(SENSORS), format_func=lambda x: SENSORS[x]["name"])
    c = SENSORS[k]
    fig = px.line(df.tail(300), x="ts", y=k, title=f"{c['name']} ({c['unit']})")
    fig.add_hline(y=c["warn"], line_dash="dash", line_color="#f59e0b", annotation_text="Warning")
    fig.add_hline(y=c["crit"], line_dash="dash", line_color="#dc2626", annotation_text="Critical")
    styles.chart(fig, "s1", 360)
    st.markdown("**Fault injection** — push a sensor into an abnormal state to test alerts and AI detection.")
    for col, key in zip(st.columns(len(SENSORS)), SENSORS):
        on = key in st.session_state.faults
        if col.button(("Clear " if on else "Inject ") + SENSORS[key]["name"], key=f"f_{key}"):
            st.session_state.faults.symmetric_difference_update({key}); st.rerun()
