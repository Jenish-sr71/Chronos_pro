import streamlit as st

from backend import auth
from backend import config as cfg
from backend import controls, storage, theme

st.set_page_config(page_title="Chronos · Settings", page_icon="⏳", layout="wide")
theme.inject_css()
auth.require_login()
theme.render_background()

controls.render_sidebar_snapshot()
user = auth.current_user()

theme.page_header("Settings", "Configure your goal, categories, and stored data.")

settings = cfg.load_settings(user)
categories = cfg.load_categories(user)

# ---------------------------------------------------------------------------
# Daily goal
# ---------------------------------------------------------------------------
theme.section_title("Daily goal")
new_goal = st.number_input(
    "Daily goal (minutes)",
    min_value=10,
    value=settings.get("daily_goal", 240),
    step=15,
    label_visibility="collapsed",
)
if new_goal != settings.get("daily_goal"):
    settings["daily_goal"] = new_goal
    cfg.save_settings(settings, user)
    st.toast("Daily goal updated.")

# ---------------------------------------------------------------------------
# Categories
# ---------------------------------------------------------------------------
theme.section_title("Categories")

chip_html = '<div class="chip-list">'
for c in categories:
    chip_html += f'<div class="chip">{c}</div>'
chip_html += "</div>"
st.markdown(chip_html, unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 1.3, 1])
with col1:
    new_cat = st.text_input("Add a category", placeholder="e.g., Cooking", label_visibility="collapsed")
with col2:
    remove_cat = st.selectbox("Remove a category", ["—"] + categories, label_visibility="collapsed")
with col3:
    if st.button("Add"):
        if new_cat and new_cat not in categories:
            categories.append(new_cat)
            cfg.save_categories(categories, user)
            st.rerun()

if remove_cat != "—":
    st.markdown('<div class="ghost-btn">', unsafe_allow_html=True)
    if st.button(f"Remove '{remove_cat}'"):
        categories = [c for c in categories if c != remove_cat]
        if not categories:
            categories = ["Work"]
        cfg.save_categories(categories, user)
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Danger zone
# ---------------------------------------------------------------------------
theme.section_title("Danger zone")
st.markdown('<div class="danger-zone">', unsafe_allow_html=True)
st.write("This permanently deletes every logged session. This cannot be undone.")
confirm = st.checkbox("I understand this will delete all my data")
st.markdown('<div class="end-session">', unsafe_allow_html=True)
if st.button("🗑  Clear all data", disabled=not confirm):
    storage.clear_all(user)
    st.toast("All session data cleared.")
    st.rerun()
st.markdown("</div></div>", unsafe_allow_html=True)
