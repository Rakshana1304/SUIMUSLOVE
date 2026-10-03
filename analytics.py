import streamlit as st, styles, plotly.express as px
import database as db
from config import SENSORS

def render(df, latest):
    styles.header("Analytics", "Trends, statistics and export")
    full = db.read_readings()
    d = st.date_input("Date range", (full.ts.min().date(), full.ts.max().date()))
    params = st.multiselect("Parameters", list(SENSORS) + ["steam"], default=["temperature", "pressure"])
    if len(d) == 2 and params:
        f = full[(full.ts.dt.date >= d[0]) & (full.ts.dt.date <= d[1])]
        st.plotly_chart(px.line(f, x="ts", y=params), use_container_width=True)
        st.dataframe(f[params].describe().T, use_container_width=True)
        st.download_button("Download CSV", f.to_csv(index=False), "simguard_readings.csv", "text/csv")
    a = db.read_alerts()
    if len(a): st.plotly_chart(px.histogram(a, x="sensor", color="severity", title="Fault frequency"), use_container_width=True)
