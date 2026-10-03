"""SimGuard – entry point. Run: streamlit run app.py"""
import numpy as np, streamlit as st
from datetime import datetime
import database as db, styles
from config import SENSORS
from utils import simulation as sim, alerts
from models import fault_model
from modules import dashboard, sensors, digital_twin, fault_detection, machine_status, analytics

st.set_page_config("SimGuard", "🛡️", layout="wide")
styles.inject()

@st.cache_resource
def get_model(): return fault_model.train()

ss = st.session_state
if "init" not in ss:
    db.init_db(); ss.update(init=True, state=sim.initial_state(), faults=set(), running=True, setpoint=180, load=1.0, rng=np.random.default_rng(), model=get_model())
    for _ in range(60): ss.state = sim.step(ss.state, set(), ss.rng); db.insert_reading(datetime.now().isoformat(), ss.state)  # seed history

def tick():
    ss.state = sim.step(ss.state, ss.faults, ss.rng, ss.setpoint, ss.load)
    ts = datetime.now().isoformat(); db.insert_reading(ts, ss.state); alerts.check(ts, ss.state)

PAGES = {"📊  Dashboard": dashboard, "📡  Sensors": sensors, "🧊  Digital Twin": digital_twin, "🧠  AI Fault Detection": fault_detection, "⚙️  Machine Status": machine_status, "📈  Analytics": analytics}
with st.sidebar:
    st.markdown("<div class='brand'><div class='logo'>🛡️</div><div><b>SimGuard</b><span>Digital Twin AI</span></div></div>", unsafe_allow_html=True)
    page = st.radio("Navigation", list(PAGES), label_visibility="collapsed")
    st.markdown("<div class='side-label'>Simulation</div>", unsafe_allow_html=True)
    ss.running = st.toggle("Run simulation", ss.running)
    interval = st.slider("Refresh (s)", 1, 10, 3)
    if st.button("Generate reading"): tick()
    n = int((db.read_alerts().acknowledged == 0).sum()); st.markdown(f"<div class='side-label'>Alerts</div>🔔 <b>{n}</b> open", unsafe_allow_html=True)
    if st.button("Acknowledge all"): db.acknowledge_all(); st.rerun()
    st.markdown("<div class='profile'><div class='av'>OP</div><div><b style='color:#fff'>Operator</b><br><span style='font-size:.75rem'>Demo profile · no login</span></div></div>", unsafe_allow_html=True)

def view():
    if ss.running: tick()
    df = db.read_readings(500); PAGES[page].render(df, ss.state)

if hasattr(st, "fragment"): st.fragment(run_every=interval if ss.running else None)(view)()
else: view()  # fallback: use "Generate reading"/rerun on older Streamlit
