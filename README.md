# SimGuard – Digital Twin AI for Industrial Boiler Monitoring
Streamlit + SQLite + scikit-learn + Plotly. **All data is simulated; nothing is connected to real IoT sensors.**
## Run
```
pip install -r requirements.txt
streamlit run app.py
```
## Structure
`app.py` (entry), `config.py` (thresholds), `database.py` (SQLite), `utils/` (simulation, alerts), `models/fault_model.py` (Isolation Forest + Random Forest trained on synthetic data), `modules/` (six pages).
## AI note
Models train at startup on synthetic data; held-out metrics do not establish real-world accuracy. The digital twin is simplified and not physics-validated.
## Deploy
Push to GitHub → share.streamlit.io → select `app.py`. SQLite on Community Cloud is ephemeral; use an external DB (e.g. Postgres/Supabase) for persistence.
## Screenshots
Add after running. ## Future work: real sensor ingestion (MQTT), auth, PNG boiler asset, Figma-matched styling.
