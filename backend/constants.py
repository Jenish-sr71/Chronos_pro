import os

# Project root = one level up from this backend/ folder, so paths work
# no matter what directory Streamlit is launched from.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")
DATA_FILE = os.path.join(BASE_DIR, "time_logs.csv")

# Instrument-panel palette, shared across every chart and category chip
# so a given category always reads as the same color everywhere in the app.
PALETTE = ["#46C2A0", "#5AA9E6", "#E2735C", "#9B8CFF", "#E3B23C", "#E667A0", "#7C8AA3"]
