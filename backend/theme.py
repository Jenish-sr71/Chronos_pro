import math

import streamlit as st
import streamlit.components.v1 as components


def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

        :root{
            --bg: #0B1220;
            --surface: #111A2B;
            --surface-2: #17233A;
            --surface-3: #1D2B45;
            --border: rgba(255,255,255,0.07);
            --text: #E7ECF5;
            --text-muted: #7C8AA3;
            --accent: #46C2A0;
            --accent-soft: rgba(70,194,160,0.14);
            --accent-deep: #2E9C7E;
            --danger: #E2735C;
            --danger-soft: rgba(226,115,92,0.14);
        }

        html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"],
        .main, section.main, [data-testid="stAppViewContainer"] > .main{
            background: transparent !important;
            color: var(--text);
            font-family: 'Inter', sans-serif;
        }
        /* The gradient lives directly on html/body — a real background-color
           can't be "lost" mid-session the way a separate position:fixed div
           can if a Streamlit rerun ever puts a transform on an ancestor
           (which breaks position:fixed, since a transformed ancestor becomes
           the new containing block instead of the viewport). This is always
           there, guaranteed, no matter what Streamlit does around it. */
        html, body{
            background: linear-gradient(180deg, #1B1140 0%, #1A2B52 35%, #14273E 65%, #0B1220 100%) !important;
            background-attachment: fixed !important;
        }
        [data-testid="stHeader"]{ background-color: transparent; }
        .block-container{ padding-top: 2rem; max-width: 1100px; }

        /* ---------- Animated scene (decorative overlay, scrolls with the page) ---------- */
        .bg-scene{
            position: absolute; top: 0; left: 0; right: 0; min-height: 100vh;
            z-index: -1; overflow: hidden; pointer-events: none;
        }
        .bg-glow{
            position:absolute; top:-140px; right:-100px; width:480px; height:480px; border-radius:50%;
            background:
                radial-gradient(circle at 32% 32%, rgba(70,194,160,0.35), rgba(70,194,160,0) 60%),
                radial-gradient(circle at 62% 55%, rgba(155,140,255,0.32), rgba(155,140,255,0) 60%),
                radial-gradient(circle at 45% 72%, rgba(90,169,230,0.28), rgba(90,169,230,0) 60%);
            filter: blur(6px);
        }
        .bg-star{
            position:absolute; width:2px; height:2px; background:#fff; border-radius:50%;
            animation: twinkle 3.2s ease-in-out infinite;
        }
        @keyframes twinkle{ 0%,100%{opacity:0.15;} 50%{opacity:0.9;} }
        .bg-cloud{
            position:absolute; opacity:0.5; filter: blur(0.5px);
            animation: drift linear infinite;
        }
        @keyframes drift{ from{ transform: translateX(-10vw); } to{ transform: translateX(110vw); } }
        .bg-mtn{ position:absolute; bottom:0; left:0; width:100%; }
        .bg-mtn.far{ opacity:0.55; }
        .bg-mtn.near{ opacity:0.88; }

        h1, h2, h3, .chronos-display{
            font-family: 'Space Grotesk', sans-serif;
            color: var(--text);
            letter-spacing: -0.01em;
        }

        /* ---------- Sidebar ---------- */
        [data-testid="stSidebar"]{
            background-color: var(--surface);
            border-right: 1px solid var(--border);
        }
        [data-testid="stSidebar"] .block-container{ padding-top: 1rem; }
        [data-testid="stSidebarNav"]{
            padding-top: 0.6rem;
            border-bottom: 1px solid var(--border);
            padding-bottom: 0.8rem;
            margin-bottom: 1rem;
        }
        [data-testid="stSidebarNav"] a{
            border-radius: 8px;
            margin: 0 0.6rem;
        }
        [data-testid="stSidebarNav"] a span{ color: var(--text-muted); font-family: 'Inter', sans-serif; font-size: 0.92rem; }
        [data-testid="stSidebarNav"] a[aria-current="page"]{ background-color: var(--accent-soft); }
        [data-testid="stSidebarNav"] a[aria-current="page"] span{ color: var(--accent); font-weight: 600; }

        .brand-row{
            display:flex;
            align-items:center;
            gap: 0.55rem;
            padding: 0 0.2rem;
            margin-bottom: 1.3rem;
        }
        .brand-glyph{
            width: 34px; height: 34px;
            border-radius: 9px;
            background: linear-gradient(155deg, var(--accent), var(--accent-deep));
            display:flex; align-items:center; justify-content:center;
            font-size: 1.05rem;
            flex-shrink: 0;
        }
        .brand-name{
            font-family:'Space Grotesk', sans-serif;
            font-size: 1.15rem;
            font-weight: 700;
            color: var(--text);
            line-height: 1.1;
        }
        .brand-sub{
            font-family:'JetBrains Mono', monospace;
            font-size: 0.65rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--text-muted);
        }

        .snapshot-card{
            background-color: var(--surface-2);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 0.9rem 1rem;
            margin-top: 0.4rem;
        }
        .snapshot-label{
            font-family:'JetBrains Mono', monospace;
            font-size: 0.65rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--text-muted);
            margin-bottom: 0.5rem;
        }
        .snapshot-row{
            display:flex; justify-content:space-between; align-items:baseline;
            margin-bottom: 0.4rem;
        }
        .snapshot-value{ font-family:'Space Grotesk', sans-serif; font-weight:600; color: var(--text); }
        .snapshot-bar-track{
            width:100%; height:6px; border-radius:99px;
            background-color: var(--surface-3);
            overflow:hidden;
        }
        .snapshot-bar-fill{
            height:100%; border-radius:99px;
            background-color: var(--accent);
        }
        .snapshot-live{
            display:flex; align-items:center; gap:0.4rem;
            margin-top: 0.7rem;
            font-size: 0.78rem;
            color: var(--accent);
        }
        .pulse-dot{
            width: 7px; height: 7px; border-radius: 50%;
            background-color: var(--accent);
            box-shadow: 0 0 0 rgba(70,194,160, 0.6);
            animation: pulse 1.6s infinite;
        }
        @keyframes pulse{
            0%{ box-shadow: 0 0 0 0 rgba(70,194,160, 0.5); }
            70%{ box-shadow: 0 0 0 6px rgba(70,194,160, 0); }
            100%{ box-shadow: 0 0 0 0 rgba(70,194,160, 0); }
        }

        [data-testid="stSidebar"] label{ color: var(--text-muted) !important; font-size: 0.8rem; }
        [data-testid="stSidebar"] input{
            background-color: var(--surface-2) !important;
            border: 1px solid var(--border) !important;
            color: var(--text) !important;
            border-radius: 8px !important;
        }

        /* ---------- Page header ---------- */
        .page-header{
            display:flex;
            justify-content:space-between;
            align-items:flex-end;
            margin-bottom: 1.6rem;
            gap: 1rem;
            flex-wrap: wrap;
        }
        .page-title{
            font-family:'Space Grotesk', sans-serif;
            font-size: 1.9rem;
            font-weight: 700;
            color: var(--text);
            margin: 0;
        }
        .page-subtitle{ color: var(--text-muted); font-size: 0.92rem; margin-top: 0.2rem; }
        .page-chip{
            font-family:'JetBrains Mono', monospace;
            font-size: 0.75rem;
            color: var(--text-muted);
            background-color: var(--surface);
            border: 1px solid var(--border);
            border-radius: 999px;
            padding: 0.35rem 0.85rem;
            white-space: nowrap;
        }
        .page-chip.hot{ color: var(--accent); border-color: rgba(70,194,160,0.35); background-color: var(--accent-soft); }

        .section-title{
            font-family:'Space Grotesk', sans-serif;
            font-size: 1.05rem;
            font-weight: 600;
            color: var(--text);
            margin: 1.6rem 0 0.7rem;
        }

        /* ---------- Segmented pill control (category + range filters) ---------- */
        [data-testid="stRadio"] > div[role="radiogroup"]{
            display: flex;
            flex-wrap: wrap;
            gap: 0.4rem;
        }
        [data-testid="stRadio"] label{
            border: 1px solid var(--border);
            border-radius: 999px;
            padding: 0.35rem 0.9rem;
            background-color: var(--surface-2);
            cursor: pointer;
            transition: all 0.12s ease;
            margin: 0 !important;
        }
        [data-testid="stRadio"] label > div:first-child{ display: none; }
        [data-testid="stRadio"] label p{
            color: var(--text-muted);
            font-family: 'Inter', sans-serif;
            font-size: 0.85rem;
            margin: 0;
        }
        [data-testid="stRadio"] label:hover{ border-color: var(--accent); }
        [data-testid="stRadio"] label:has(input:checked){
            background-color: var(--accent);
            border-color: var(--accent-deep);
        }
        [data-testid="stRadio"] label:has(input:checked) p{ color: #0B1220; font-weight: 600; }

        /* ---------- Buttons ---------- */
        .stButton > button{
            position: relative;
            overflow: hidden;
            isolation: isolate;
            border-radius: 999px;
            border: 1px solid var(--border);
            background-color: var(--accent);
            color: #06110D;
            font-weight: 600;
            padding: 0.6rem 1.5rem;
            min-height: 2.6rem;
            min-width: 4.5rem;
            white-space: nowrap;
            box-shadow: 0 2px 10px -5px rgba(0,0,0,0.6);
            transition: transform 0.1s ease, box-shadow 0.15s ease;
        }
        /* Full-width CTAs only where we actually want a wide bar — the sidebar
           (Start/End session, Sync, Log out) — not small inline buttons like
           Settings' "Add"/"Remove", which should size to their own label. */
        [data-testid="stSidebar"] .stButton > button{
            width: 100%;
        }
        .stButton > button::before{
            content: "";
            position: absolute;
            top: 50%; left: 50%;
            width: 90px; height: 90px;
            background: linear-gradient(90deg, #46C2A0 0%, #9B8CFF 50%, #5AA9E6 100%);
            filter: blur(16px);
            opacity: 0.55;
            border-radius: 50%;
            transform: translate(-50%, -50%) rotate(0deg);
            animation: chronos-btn-spin 3s linear infinite;
            z-index: -1;
        }
        .stButton > button:hover{
            color: #fff;
            box-shadow: 0 4px 16px -4px rgba(70,194,160,0.5);
        }
        .stButton > button:hover::before{
            width: 70px; height: 70px;
            opacity: 0.8;
        }
        .stButton > button:active{ transform: scale(0.97); }

        @keyframes chronos-btn-spin{
            0%   { transform: translate(-50%, -50%) rotate(0deg); }
            100% { transform: translate(-50%, -50%) rotate(360deg); }
        }

        .end-session .stButton > button{
            background-color: var(--surface-2);
            color: var(--danger);
            border: 1px solid var(--danger);
        }
        .end-session .stButton > button::before{
            background: linear-gradient(90deg, var(--danger) 0%, #E667A0 100%);
        }
        .end-session .stButton > button:hover{
            color: #fff;
            box-shadow: 0 4px 16px -4px rgba(226,115,92,0.5);
        }

        .ghost-btn .stButton > button{
            background-color: transparent;
            color: var(--text-muted);
            border: 1px solid var(--border);
            box-shadow: none;
        }
        .ghost-btn .stButton > button::before{ display: none; }
        .ghost-btn .stButton > button:hover{ border-color: var(--text-muted); color: var(--text); box-shadow: none; }

        hr, [data-testid="stSidebar"] hr{ border-color: var(--border); }

        /* ---------- Cards ---------- */
        .chronos-card{
            background-color: var(--surface);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 1.4rem 1.6rem;
            height: 100%;
        }
        .card-label{
            font-family:'JetBrains Mono', monospace;
            font-size: 0.7rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--text-muted);
            margin-bottom: 0.4rem;
        }
        .card-number{
            font-family: 'Space Grotesk', sans-serif;
            font-size: 2.4rem;
            font-weight: 600;
            color: var(--text);
            line-height: 1.1;
        }
        .card-sub{ color: var(--text-muted); font-size: 0.85rem; margin-top: 0.3rem;}

        /* ---------- Control bar (start/stop session) ---------- */
        .control-bar{
            background-color: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.3rem 1.6rem 0.6rem;
            margin-bottom: 1.7rem;
        }
        [data-testid="stVerticalBlockBorderWrapper"]:has(.mascot-row){
            background-color: var(--surface);
            border-color: var(--border) !important;
            border-radius: 16px !important;
        }

        .control-bar-label{
            font-family:'JetBrains Mono', monospace;
            font-size: 0.7rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--text-muted);
            margin-bottom: 0.7rem;
        }
        .active-session-row{
            display:flex; align-items:center; gap: 1.2rem;
            background: linear-gradient(180deg, var(--accent-soft), transparent);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1rem 1.3rem;
            margin-bottom: 0.9rem;
        }
        .sweep-ring{
            --sweep: 0;
            width: 52px; height: 52px;
            border-radius: 50%;
            flex-shrink: 0;
            background: conic-gradient(var(--accent) calc(var(--sweep) * 1%), var(--surface-2) 0);
            -webkit-mask: radial-gradient(farthest-side, transparent calc(100% - 7px), #000 calc(100% - 7px));
            mask: radial-gradient(farthest-side, transparent calc(100% - 7px), #000 calc(100% - 7px));
        }
        .timer-readout{
            font-family:'JetBrains Mono', monospace;
            font-size: 1.75rem;
            color: var(--text);
            letter-spacing: 0.02em;
        }
        .timer-meta{ color: var(--text-muted); font-size: 0.85rem; }
        .timer-meta b{ color: var(--text); }

        /* ---------- Stat tiles ---------- */
        .stat-row{ display:flex; gap: 1rem; margin-bottom: 1.6rem; flex-wrap: wrap; }
        .stat-tile{
            flex: 1 1 160px;
            background-color: var(--surface);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 1.1rem 1.3rem;
        }
        .stat-tile .card-number{ font-size: 1.9rem; }

        /* ---------- Radial gauge ---------- */
        .gauge-wrap{ position: relative; width: 140px; height: 140px; margin: 0.2rem auto 0.4rem; }
        .gauge-wrap svg{ width: 100%; height: 100%; transform: rotate(-90deg); }
        .gauge-track{ fill: none; stroke: var(--surface-2); stroke-width: 10; }
        .gauge-fill{
            fill: none; stroke: var(--accent); stroke-width: 10;
            stroke-linecap: round; transition: stroke-dashoffset 0.6s ease;
        }
        .gauge-center{
            position: absolute; inset: 0;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
        }
        .gauge-pct{ font-family: 'Space Grotesk', sans-serif; font-size: 1.6rem; font-weight: 700; color: var(--text); }
        .gauge-sub{ font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: var(--text-muted); margin-top: 2px; }

        /* ---------- Journal ---------- */
        .journal-card{
            background-color: var(--surface);
            border: 1px solid var(--border);
            border-left: 3px solid var(--accent);
            border-radius: 10px;
            padding: 1.5rem 1.9rem;
            font-family: 'Inter', sans-serif;
            font-size: 1rem;
            line-height: 1.7;
            color: var(--text);
        }
        .journal-card .line-item{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.86rem;
            color: var(--text-muted);
            margin: 0.15rem 0;
        }
        .journal-card .line-item b{ color: var(--text); }

        [data-testid="stDataFrame"]{ border: 1px solid var(--border); border-radius: 10px; overflow: hidden; }

        button[data-baseweb="tab"]{ font-family: 'Inter', sans-serif; color: var(--text-muted); }
        button[data-baseweb="tab"][aria-selected="true"]{ color: var(--accent); }

        .empty-state{
            text-align:center;
            padding: 3.4rem 1rem;
            color: var(--text-muted);
            background-color: var(--surface);
            border: 1px dashed var(--border);
            border-radius: 14px;
        }
        .empty-state .glyph{ font-size: 2.2rem; margin-bottom: 0.6rem; }
        .empty-state .headline{
            font-family:'Space Grotesk', sans-serif;
            font-size: 1.2rem;
            font-weight: 600;
            color: var(--text);
            margin-bottom: 0.3rem;
        }

        /* ---------- Category chips (settings) ---------- */
        .chip-list{ display:flex; flex-wrap:wrap; gap:0.5rem; margin: 0.5rem 0 1rem; }
        .chip{
            display:flex; align-items:center; gap:0.4rem;
            background-color: var(--surface-2);
            border: 1px solid var(--border);
            border-radius: 999px;
            padding: 0.3rem 0.6rem 0.3rem 0.85rem;
            font-size: 0.85rem;
            color: var(--text);
        }
        .mascot-row{ display:flex; align-items:center; gap:0.8rem; margin-bottom:1rem; }
        .mascot-avatar-circle{
            width:44px; height:44px; flex-shrink:0; border-radius:50%;
            background: linear-gradient(155deg, var(--accent), var(--accent-deep));
            display:flex; align-items:center; justify-content:center;
            font-size:1.3rem;
        }
        .mascot-bubble{
            position:relative;
            background-color: var(--surface-2);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 0.6rem 1rem;
            font-size: 0.9rem;
            font-weight: 500;
            color: var(--text) !important;
        }
        .mascot-bubble:before{
            content:"";
            position:absolute; left:-6px; top:16px;
            width:12px; height:12px;
            background-color: var(--surface-2);
            border-left:1px solid var(--border);
            border-bottom:1px solid var(--border);
            transform: rotate(45deg);
        }

        .danger-zone{
            border: 1px solid rgba(226,115,92,0.3);
            background-color: var(--danger-soft);
            border-radius: 14px;
            padding: 1.2rem 1.4rem;
        }

        /* ---------- Mobile ---------- */
        @media (max-width: 640px){
            .block-container{ padding: 1rem 0.9rem !important; }
            .page-title{ font-size: 1.4rem; }
            .page-header{ align-items:flex-start; }
            .card-number{ font-size: 1.7rem; }
            .stat-tile{ flex: 1 1 42%; padding: 0.9rem 1rem; }
            .gauge-wrap{ width: 112px; height: 112px; }
            .gauge-pct{ font-size: 1.3rem; }
            .mascot-bubble{ font-size: 0.82rem; padding: 0.5rem 0.8rem; }
            .active-session-row{ flex-direction: column; align-items:flex-start; gap: 0.6rem; }
            .timer-readout{ font-size: 1.5rem; }
            .brand-name{ font-size: 1.05rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Layout primitives
# ---------------------------------------------------------------------------

def page_header(title, subtitle="", chip=None, chip_hot=False):
    chip_html = ""
    if chip:
        chip_html = f'<div class="page-chip{" hot" if chip_hot else ""}">{chip}</div>'
    st.markdown(
        f"""
        <div class="page-header">
            <div>
                <div class="page-title">{title}</div>
                <div class="page-subtitle">{subtitle}</div>
            </div>
            {chip_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(text):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Cards / tiles
# ---------------------------------------------------------------------------

def metric_card(label, value, sub_html=""):
    st.markdown(
        f"""
        <div class="chronos-card">
            <div class="card-label">{label}</div>
            <div class="card-number">{value}</div>
            {sub_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def stat_tile(label, value, sub=""):
    sub_html = f'<div class="card-sub">{sub}</div>' if sub else ""
    st.markdown(
        f"""
        <div class="stat-tile">
            <div class="card-label">{label}</div>
            <div class="card-number">{value}</div>
            {sub_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def goal_ring(pct, sub_label, label="Goal progress"):
    """Radial gauge showing progress toward the daily goal (0-1)."""
    radius = 52
    circumference = 2 * math.pi * radius
    offset = circumference * (1 - max(0.0, min(pct, 1.0)))

    st.markdown(
        f"""
        <div class="chronos-card">
            <div class="card-label" style="text-align:center;">{label}</div>
            <div class="gauge-wrap">
                <svg viewBox="0 0 120 120">
                    <circle class="gauge-track" cx="60" cy="60" r="{radius}"></circle>
                    <circle class="gauge-fill" cx="60" cy="60" r="{radius}"
                        style="stroke-dasharray:{circumference:.1f}; stroke-dashoffset:{offset:.1f};">
                    </circle>
                </svg>
                <div class="gauge-center">
                    <div class="gauge-pct">{int(pct * 100)}%</div>
                    <div class="gauge-sub">{sub_label}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def empty_state(glyph, headline, body):
    st.markdown(
        f"""
        <div class="empty-state">
            <div class="glyph">{glyph}</div>
            <div class="headline">{headline}</div>
            <div>{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def plotly_dark_layout(fig, **extra):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E7ECF5", family="Inter"),
        margin=dict(t=10, b=10, l=10, r=10),
        **extra,
    )
    return fig


# ---------------------------------------------------------------------------
# Sidebar shell — brand + always-visible "today" snapshot, on every page
# ---------------------------------------------------------------------------

def render_sidebar_shell(today_total=0, goal=1, is_tracking=False, active_label=""):
    with st.sidebar:
        st.markdown(
            """
            <div class="brand-row">
                <div class="brand-glyph">⏳</div>
                <div>
                    <div class="brand-name">Chronos</div>
                    <div class="brand-sub">Life log</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        pct = min(today_total / goal, 1.0) if goal > 0 else 0
        live_html = ""
        if is_tracking:
            live_html = f"""
            <div class="snapshot-live">
                <div class="pulse-dot"></div> Tracking {active_label}
            </div>
            """
        st.markdown(
            f"""
            <div class="snapshot-card">
                <div class="snapshot-label">Today</div>
                <div class="snapshot-row">
                    <div class="snapshot-value">{today_total}m</div>
                    <div style="color:var(--text-muted); font-size:0.75rem;">of {goal}m</div>
                </div>
                <div class="snapshot-bar-track">
                    <div class="snapshot-bar-fill" style="width:{pct*100:.0f}%;"></div>
                </div>
                {live_html}
            </div>
            """,
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# Live timer readout used inside the control bar
# ---------------------------------------------------------------------------

def render_background():
    """Fixed animated parallax backdrop — sky glow, drifting clouds, layered hills.
    Call once near the top of each page, right after inject_css()."""
    st.markdown(
        """
        <div class="bg-scene">
            <div class="bg-glow"></div>
            <div class="bg-star" style="top:12%; left:15%; animation-delay:0s;"></div>
            <div class="bg-star" style="top:20%; left:70%; animation-delay:0.6s;"></div>
            <div class="bg-star" style="top:8%;  left:45%; animation-delay:1.2s;"></div>
            <div class="bg-star" style="top:30%; left:85%; animation-delay:1.8s;"></div>
            <div class="bg-star" style="top:15%; left:30%; animation-delay:2.4s;"></div>
            <div class="bg-star" style="top:24%; left:10%; width:3px; height:3px; background:#9B8CFF; animation-delay:0.9s;"></div>
            <div class="bg-star" style="top:18%; left:55%; width:3px; height:3px; background:#46C2A0; animation-delay:1.6s;"></div>
            <svg class="bg-cloud" style="top:10%; width:140px; animation-duration:70s;" viewBox="0 0 100 40">
                <ellipse cx="30" cy="25" rx="30" ry="12" fill="#ffffff"/>
                <ellipse cx="55" cy="18" rx="22" ry="14" fill="#ffffff"/>
            </svg>
            <svg class="bg-cloud" style="top:22%; width:100px; animation-duration:95s; animation-delay:-30s;" viewBox="0 0 100 40">
                <ellipse cx="30" cy="25" rx="26" ry="10" fill="#ffffff"/>
                <ellipse cx="55" cy="20" rx="18" ry="11" fill="#ffffff"/>
            </svg>
            <svg class="bg-mtn far" viewBox="0 0 1200 260" preserveAspectRatio="none">
                <polygon points="0,260 0,150 200,60 420,170 650,40 900,160 1200,90 1200,260" fill="#39366E"/>
            </svg>
            <svg class="bg-mtn near" viewBox="0 0 1200 220" preserveAspectRatio="none">
                <polygon points="0,220 0,120 250,190 480,70 760,180 1000,60 1200,140 1200,220" fill="#103A38"/>
            </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_mascot(message):
    """Original mascot — a small hourglass spirit that reacts to your sessions."""
    st.markdown(
        f"""
        <div class="mascot-row">
            <div class="mascot-avatar-circle">⏳</div>
            <div class="mascot-bubble">{message}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_live_readout(start_time, task_label):
    start_ts_ms = int(start_time.timestamp() * 1000)
    start_label = start_time.strftime("%H:%M")

    # Rendered via components.html (a real iframe) instead of st.markdown, because
    # browsers never execute <script> tags inserted through innerHTML — which is
    # how st.markdown(unsafe_allow_html=True) injects HTML. That silently killed
    # the ticking timer. CSS vars from the main page aren't visible inside the
    # iframe, so the palette is duplicated here.
    components.html(
        f"""
        <style>
            body {{ margin:0; background:transparent; font-family:'Inter',sans-serif; }}
            .active-session-row{{
                display:flex; align-items:center; gap:1.2rem;
                background: linear-gradient(180deg, rgba(70,194,160,0.14), transparent);
                border: 1px solid rgba(255,255,255,0.07);
                border-radius: 12px;
                padding: 1rem 1.3rem;
                box-sizing: border-box;
            }}
            .sweep-ring{{
                --sweep: 0;
                width: 52px; height: 52px; border-radius: 50%; flex-shrink: 0;
                background: conic-gradient(#46C2A0 calc(var(--sweep) * 1%), #17233A 0);
                -webkit-mask: radial-gradient(farthest-side, transparent calc(100% - 7px), #000 calc(100% - 7px));
                mask: radial-gradient(farthest-side, transparent calc(100% - 7px), #000 calc(100% - 7px));
            }}
            .timer-readout{{
                font-family:'JetBrains Mono', monospace; font-size: 1.75rem;
                color: #E7ECF5; letter-spacing: 0.02em;
            }}
            .timer-meta{{ color: #7C8AA3; font-size: 0.85rem; }}
            .timer-meta b{{ color: #E7ECF5; }}
        </style>
        <div class="active-session-row">
            <div class="sweep-ring" id="chronos-sweep-ring"></div>
            <div>
                <div class="timer-meta">Tracking <b>{task_label}</b> · started at {start_label}</div>
                <div id="chronos-live-timer" class="timer-readout">00:00:00</div>
            </div>
        </div>
        <script>
            const startTs = {start_ts_ms};
            const el = document.getElementById('chronos-live-timer');
            const ring = document.getElementById('chronos-sweep-ring');
            function tick() {{
                const diff = Math.max(0, Date.now() - startTs);
                const h = String(Math.floor(diff / 3600000)).padStart(2, '0');
                const m = String(Math.floor((diff % 3600000) / 60000)).padStart(2, '0');
                const s = String(Math.floor((diff % 60000) / 1000)).padStart(2, '0');
                el.textContent = h + ':' + m + ':' + s;
                const secondsIntoMinute = Math.floor(diff / 1000) % 60;
                ring.style.setProperty('--sweep', (secondsIntoMinute / 60 * 100).toFixed(2));
            }}
            tick();
            setInterval(tick, 1000);
        </script>
        """,
        height=90,
    )
