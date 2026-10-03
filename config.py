"""Central configuration: sensor limits and alert thresholds (all editable)."""
# mode: 'high' = bad when value rises, 'low' = bad when value falls
SENSORS = {
 "temperature": dict(name="Temperature", unit="°C",   nominal=180, lo=0, hi=300, warn=210, crit=240, mode="high", noise=1.5, fault=255, icon="🌡️"),
 "pressure":    dict(name="Pressure",    unit="bar",  nominal=10,  lo=0, hi=20,  warn=13,  crit=15,  mode="high", noise=0.15, fault=16, icon="⏲️"),
 "vibration":   dict(name="Vibration",   unit="mm/s", nominal=2,   lo=0, hi=15,  warn=5,   crit=8,   mode="high", noise=0.15, fault=9, icon="📳"),
 "water_level": dict(name="Water Level", unit="%",    nominal=60,  lo=0, hi=100, warn=35,  crit=20,  mode="low",  noise=0.6, fault=15, icon="💧"),
 "flow":        dict(name="Flow",        unit="m³/h", nominal=50,  lo=0, hi=120, warn=25,  crit=10,  mode="low",  noise=1.0, fault=8, icon="🌀"),
 "efficiency":  dict(name="Energy Efficiency", unit="%", nominal=88, lo=0, hi=100, warn=75, crit=65, mode="low", noise=0.4, fault=60, icon="⚡"),
}
DB_PATH = "data/simguard.db"
COLORS = {"ok": "#16a34a", "warning": "#f59e0b", "critical": "#dc2626", "info": "#2563eb", "accent": "#7c3aed", "navy": "#0f172a"}
