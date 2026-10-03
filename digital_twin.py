import streamlit as st, styles

def render(df, latest):
    styles.header("Digital Twin", "Simplified boiler simulation")
    st.warning("Simplified simulation — not physics-validated.")
    c1, c2 = st.columns([1, 1])
    with c1:
        st.session_state.setpoint = st.slider("Temperature setpoint (°C)", 120, 230, st.session_state.setpoint)
        st.session_state.load = st.slider("Load / inlet flow factor", 0.4, 1.5, st.session_state.load, 0.05)
    lvl = max(0, min(100, latest["water_level"])); h = 200 * lvl / 100
    c2.markdown(f"""<svg width="260" height="260" viewBox="0 0 260 260"><rect x="40" y="20" width="160" height="200" rx="30" fill="#e2e8f0" stroke="#0f172a" stroke-width="4"/>
    <rect x="44" y="{220-h}" width="152" height="{h}" rx="26" fill="#3b82f6" opacity=".7"/><text x="120" y="120" text-anchor="middle" font-size="14">{latest['temperature']:.0f}°C · {latest['pressure']:.1f} bar</text>
    <text x="120" y="245" text-anchor="middle" font-size="12">Steam {latest['steam']:.1f} t/h · Eff {latest['efficiency']:.0f}%</text></svg>""", unsafe_allow_html=True)
