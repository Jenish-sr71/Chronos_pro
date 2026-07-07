from datetime import date

import plotly.express as px
import streamlit as st

from backend import auth
from backend import config as cfg
from backend import controls, journal, storage, theme
from backend.constants import PALETTE

st.set_page_config(page_title="Chronos", page_icon="⏳", layout="wide")
theme.inject_css()
auth.require_login()
theme.render_background()

goal = controls.render_sidebar_snapshot()
user = auth.current_user()

all_df = storage.load_all(user)
streak = journal.current_streak(all_df)
chip = f"🔥 {streak} day streak" if streak > 0 else None

theme.page_header(
    "Dashboard",
    f"{date.today().strftime('%A, %B %d')}",
    chip=chip,
    chip_hot=True,
)

controls.render_control_bar()

today_df = storage.load_for_date(date.today(), user)

if today_df is None:
    theme.empty_state(
        "⏳",
        "Nothing logged yet today",
        "Start your first session above to see today's breakdown here.",
    )
else:
    total_mins = int(today_df["Duration_Min"].sum())
    progress = min(total_mins / goal, 1.0) if goal > 0 else 0
    session_count = len(today_df)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col1:
        theme.metric_card("Total time today", f"{total_mins}m")
    with col2:
        theme.goal_ring(progress, sub_label=f"of {goal}m")
    with col3:
        theme.metric_card("Sessions logged", str(session_count))

    st.write("")
    tab1, tab2, tab3 = st.tabs(["📊 Breakdown", "📑 History", "📝 Journal"])

    with tab1:
        fig_pie = px.pie(
            today_df,
            values="Duration_Min",
            names="Category",
            hole=0.55,
            color_discrete_sequence=PALETTE,
        )
        theme.plotly_dark_layout(fig_pie, legend=dict(orientation="h", yanchor="bottom", y=-0.2))
        st.plotly_chart(fig_pie, use_container_width=True)

    with tab2:
        st.dataframe(
            today_df[["Category", "Task", "Start", "End", "Duration_Min"]],
            use_container_width=True,
            hide_index=True,
        )

    with tab3:
        st.caption("Generates a written summary of today. For a past day, use the Journal page.")
        if st.button("✨ Generate summary"):
            md, html = journal.build_journal(today_df, date.today(), goal)
            st.markdown(html, unsafe_allow_html=True)
            st.text_area("Copy this into your notes:", value=md, height=200)
