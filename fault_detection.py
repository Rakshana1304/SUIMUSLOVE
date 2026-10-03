import streamlit as st, styles, plotly.express as px
from models import fault_model as fm

def render(df, latest):
    styles.header("AI Fault Detection", "Anomaly detection on live readings")
    st.info("Models are trained on synthetic data. Metrics below do NOT establish real-world industrial accuracy.")
    m = st.session_state.model
    res = fm.predict(m, df.tail(300))
    res["ts"] = df.tail(300)["ts"].values
    st.plotly_chart(px.scatter(res, x="ts", y="score", color="severity", title="Anomaly score (lower = more anomalous)"), use_container_width=True)
    bad = res[res.anomaly].tail(15).copy()
    bad["action"] = bad["fault"].map(lambda f: fm.ACTIONS.get(f.replace("_fault", ""), "Inspect equipment."))
    st.subheader("Detected anomalies"); st.dataframe(bad.iloc[::-1], use_container_width=True, hide_index=True)
    with st.expander("Held-out synthetic test metrics"):
        st.write("Isolation Forest (normal vs fault)"); st.json({k: v for k, v in m["iso_report"].items() if k in ("fault", "normal")})
        st.write("Random Forest accuracy", round(m["rf_report"]["accuracy"], 3))
