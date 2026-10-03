"""Shared look & feel: CSS, HTML card helpers, Plotly styling."""
import streamlit as st
from config import COLORS

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"], .stApp {font-family:'Inter',sans-serif;}
.stApp {background:#f6f7fb;}
#MainMenu, footer {visibility:hidden;} header[data-testid=stHeader] {background:transparent;}
.block-container {padding:1.6rem 2.4rem 3rem; max-width:1500px;}
h1 {font-size:1.7rem!important; font-weight:700!important; color:#0f172a!important; margin-bottom:.1rem!important;}
h2,h3 {color:#0f172a!important; font-weight:600!important;}
/* sidebar */
[data-testid=stSidebar] {background:#0f172a; border-right:none;}
[data-testid=stSidebar] * {color:#cbd5e1;}
[data-testid=stSidebar] [role=radiogroup] {gap:.25rem;}
[data-testid=stSidebar] [role=radiogroup] label {padding:.65rem .9rem; border-radius:12px; width:100%; cursor:pointer; transition:background .15s;}
[data-testid=stSidebar] [role=radiogroup] label:hover {background:#1e293b;}
[data-testid=stSidebar] [role=radiogroup] label > div:first-child {display:none;}
[data-testid=stSidebar] [role=radiogroup] label:has(input:checked) {background:#7c3aed;}
[data-testid=stSidebar] [role=radiogroup] label:has(input:checked) * {color:#fff!important; font-weight:600;}
.brand {display:flex; align-items:center; gap:.7rem; margin:.4rem 0 1.4rem;}
.brand .logo {width:42px;height:42px;border-radius:12px;background:linear-gradient(135deg,#7c3aed,#4f46e5);display:flex;align-items:center;justify-content:center;font-size:1.3rem;}
.brand b {color:#fff!important; font-size:1.15rem; display:block; line-height:1.1;}
.brand span {font-size:.75rem; color:#94a3b8!important;}
.side-label {font-size:.72rem; color:#64748b!important; margin:1.2rem 0 .3rem; font-weight:600;}
.profile {display:flex; align-items:center; gap:.7rem; padding:.8rem; border-radius:12px; background:#1e293b; margin-top:1rem;}
.profile .av {width:36px;height:36px;border-radius:50%;background:#7c3aed;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;}
/* cards */
.card, .kpi {background:#fff; border:1px solid #e5e7eb; border-radius:16px; padding:1.1rem 1.2rem; box-shadow:0 1px 2px rgba(15,23,42,.04); margin-bottom:1rem; color:#0f172a;}
.kpi {display:flex; justify-content:space-between; align-items:flex-start;}
.kpi .lbl {font-size:.85rem; color:#64748b;} .kpi .val {font-size:1.75rem; font-weight:700; margin:.15rem 0;} .kpi .unit {font-size:.9rem; color:#64748b; font-weight:500;}
.kpi .ico {width:44px;height:44px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:1.3rem;}
.pill {display:inline-block; padding:.15rem .65rem; border-radius:999px; font-size:.75rem; font-weight:600;}
.p-ok {background:#dcfce7;color:#15803d;} .p-warning {background:#fef3c7;color:#b45309;} .p-critical {background:#fee2e2;color:#b91c1c;} .p-maint {background:#dbeafe;color:#1d4ed8;}
.live {display:inline-flex;align-items:center;gap:.4rem;background:#fff;border:1px solid #e5e7eb;border-radius:999px;padding:.3rem .8rem;font-size:.8rem;font-weight:600;color:#0f172a;}
.dot {width:8px;height:8px;border-radius:50%;background:#16a34a;} .dot.off{background:#94a3b8;}
.bar {height:6px;background:#eef0f4;border-radius:99px;overflow:hidden;margin-top:.4rem;} .bar i {display:block;height:100%;background:#7c3aed;border-radius:99px;}
.alert-row {display:flex;gap:.8rem;align-items:center;padding:.6rem 0;border-bottom:1px solid #f1f5f9;font-size:.88rem;color:#0f172a;} .alert-row small{color:#94a3b8;margin-left:auto;white-space:nowrap;}
.note {background:#f5f3ff;border:1px solid #ddd6fe;color:#5b21b6;padding:.5rem .8rem;border-radius:10px;font-size:.82rem;display:inline-block;}
[data-testid=stSidebar] .stButton button {background:#1e293b;border:1px solid #334155;color:#e2e8f0;border-radius:10px;width:100%;}
div[data-testid=stPlotlyChart] {background:#fff;border:1px solid #e5e7eb;border-radius:16px;padding:.4rem;}
</style>"""

def inject(): st.markdown(CSS, unsafe_allow_html=True)

def pill(status, text=None):
    cls = {"ok": "p-ok", "warning": "p-warning", "critical": "p-critical", "maint": "p-maint"}[status]
    return f"<span class='pill {cls}'>{text or status.title()}</span>"

def kpi(label, value, unit, icon, status="ok"):
    tint = {"ok": "#eff6ff", "warning": "#fef3c7", "critical": "#fee2e2"}[status]
    return f"<div class='kpi'><div><div class='lbl'>{label}</div><div class='val'>{value} <span class='unit'>{unit}</span></div>{pill(status, 'Normal' if status=='ok' else status.title())}</div><div class='ico' style='background:{tint}'>{icon}</div></div>"

def header(title, subtitle):
    run = st.session_state.get("running", False)
    st.markdown(f"<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem'><div><h1>{title}</h1><span style='color:#64748b'>{subtitle}</span></div><div class='live'><span class='dot {'' if run else 'off'}'></span>{'Simulation running' if run else 'Simulation paused'}</div></div>", unsafe_allow_html=True)

def chart(fig, key, h=320):
    fig.update_layout(template="plotly_white", height=h, margin=dict(l=10, r=10, t=45, b=10), font=dict(family="Inter"),
        colorway=["#7c3aed", "#2563eb", "#f59e0b", "#16a34a", "#dc2626"], legend=dict(orientation="h", y=-0.2, title=None),
        title=dict(font=dict(size=14)), xaxis_title=None)
    st.plotly_chart(fig, use_container_width=True, key=key)
