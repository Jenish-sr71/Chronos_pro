from datetime import date, datetime

import streamlit as st

from . import config as cfg
from . import storage
from . import theme


def init_session_state():
    if "start_time" not in st.session_state:
        st.session_state.start_time = None
        st.session_state.active_category = None
        st.session_state.active_task = None


def render_sidebar_snapshot():
    """Renders the brand + always-visible 'today' snapshot in the sidebar.

    Call this once at the top of every page so the sidebar looks the same
    everywhere, and a session running from the Dashboard stays visible no
    matter which page the user navigates to.
    """
    init_session_state()
    settings = cfg.load_settings()
    goal = settings.get("daily_goal", 240)

    today_df = storage.load_for_date(date.today())
    today_total = int(today_df["Duration_Min"].sum()) if today_df is not None else 0

    is_tracking = st.session_state.start_time is not None
    active_label = st.session_state.active_task or st.session_state.active_category or ""

    theme.render_sidebar_shell(
        today_total=today_total,
        goal=goal,
        is_tracking=is_tracking,
        active_label=active_label,
    )
    return goal


def render_control_bar():
    """Renders the Start / currently-tracking / End session control.

    Category and task are locked in the moment "Start" is clicked, so
    changing the category control mid-session can never silently
    reassign an in-progress log.
    """
    init_session_state()
    categories = cfg.load_categories()

    st.markdown('<div class="control-bar">', unsafe_allow_html=True)

    if st.session_state.start_time is None:
        st.markdown('<div class="control-bar-label">Start a session</div>', unsafe_allow_html=True)
        category = st.radio(
            "Category", categories, key="category_select", horizontal=True, label_visibility="collapsed"
        )
        col1, col2 = st.columns([3, 1])
        with col1:
            task_name = st.text_input(
                "Task name (optional)",
                placeholder="What are you working on?",
                key="task_input",
                label_visibility="collapsed",
            )
        with col2:
            if st.button("▶  Start", key="start_btn"):
                st.session_state.start_time = datetime.now()
                st.session_state.active_category = category
                st.session_state.active_task = task_name
                st.rerun()
    else:
        theme.render_live_readout(
            st.session_state.start_time,
            st.session_state.active_task or st.session_state.active_category,
        )
        st.markdown('<div class="end-session">', unsafe_allow_html=True)
        if st.button("⏹  End & save session", key="end_btn"):
            end_time = datetime.now()
            storage.save_session(
                st.session_state.active_category,
                st.session_state.active_task,
                st.session_state.start_time,
                end_time,
            )
            st.session_state.start_time = None
            st.session_state.active_category = None
            st.session_state.active_task = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
