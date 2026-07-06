import plotly.express as px
import streamlit as st

from backend import controls, journal, storage, theme
from backend.constants import PALETTE

st.set_page_config(page_title="Chronos · Analytics", page_icon="⏳", layout="wide")
theme.inject_css()

controls.render_sidebar_snapshot()

theme.page_header("Analytics", "Trends and patterns across your logged time.")

all_df = storage.load_all()

if all_df is None:
    theme.empty_state(
        "📊",
        "No data yet",
        "Log a few sessions from the Dashboard and your trends will show up here.",
    )
else:
    extremes = journal.session_extremes(all_df)
    streak = journal.current_streak(all_df)
    total_all = int(all_df["Duration_Min"].sum())

    st.markdown('<div class="stat-row">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        theme.stat_tile("Current streak", f"{streak}d")
    with c2:
        theme.stat_tile("Longest session", f"{extremes['longest']}m")
    with c3:
        theme.stat_tile("Average session", f"{extremes['average']}m")
    with c4:
        theme.stat_tile("All-time total", f"{total_all // 60}h {total_all % 60}m")
    st.markdown("</div>", unsafe_allow_html=True)

    theme.section_title("Trend")
    range_label = st.radio(
        "Range", ["7 Days", "30 Days"], key="trend_range", horizontal=True, label_visibility="collapsed"
    )
    days = 7 if range_label == "7 Days" else 30

    trend_df = journal.weekly_trend(all_df, days=days)
    fig_bar = px.bar(trend_df, x="Day", y="Minutes", color_discrete_sequence=[PALETTE[0]])
    theme.plotly_dark_layout(fig_bar, showlegend=False)
    fig_bar.update_traces(marker_line_width=0)
    fig_bar.update_xaxes(showgrid=False)
    fig_bar.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.05)")
    st.plotly_chart(fig_bar, use_container_width=True)

    theme.section_title("Where the time goes")
    cat_range_label = st.radio(
        "Category range",
        ["7 Days", "30 Days", "All time"],
        key="cat_range",
        horizontal=True,
        label_visibility="collapsed",
    )
    cat_days = {"7 Days": 7, "30 Days": 30, "All time": None}[cat_range_label]
    cat_df = journal.category_totals(all_df, days=cat_days)

    if cat_df.empty:
        theme.empty_state("🗂️", "Nothing in this range", "Try a wider time range.")
    else:
        col_chart, col_table = st.columns([1.3, 1])
        with col_chart:
            fig_donut = px.pie(
                cat_df, values="Minutes", names="Category", hole=0.55, color_discrete_sequence=PALETTE
            )
            theme.plotly_dark_layout(fig_donut, legend=dict(orientation="v"))
            st.plotly_chart(fig_donut, use_container_width=True)
        with col_table:
            st.dataframe(cat_df, use_container_width=True, hide_index=True)
