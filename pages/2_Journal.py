from datetime import date

import streamlit as st

from backend import config as cfg
from backend import controls, journal, storage, theme

st.set_page_config(page_title="Chronos · Journal", page_icon="⏳", layout="wide")
theme.inject_css()

goal = controls.render_sidebar_snapshot()
settings = cfg.load_settings()

theme.page_header("Journal", "Look back on any day and export a written summary.")

selected_date = st.date_input("Pick a date", value=date.today(), max_value=date.today())

day_df = storage.load_for_date(selected_date)

if day_df is None:
    theme.empty_state(
        "📭",
        "Nothing logged that day",
        "Pick a different date, or start a session from the Dashboard.",
    )
else:
    stats = journal.day_stats(day_df, goal)

    st.markdown('<div class="stat-row">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        theme.stat_tile("Total time", f"{stats['total']}m")
    with c2:
        theme.stat_tile("Sessions", str(stats["sessions"]))
    with c3:
        theme.stat_tile("Goal reached", f"{int(stats['progress'] * 100)}%")
    st.markdown("</div>", unsafe_allow_html=True)

    theme.section_title("Summary")
    md, html = journal.build_journal(day_df, selected_date, goal)
    st.markdown(html, unsafe_allow_html=True)

    st.write("")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.download_button(
            "⬇  Download as Markdown",
            data=md,
            file_name=f"chronos-journal-{selected_date.isoformat()}.md",
            mime="text/markdown",
        )

    theme.section_title("Raw log")
    st.dataframe(
        day_df[["Category", "Task", "Start", "End", "Duration_Min"]],
        use_container_width=True,
        hide_index=True,
    )
