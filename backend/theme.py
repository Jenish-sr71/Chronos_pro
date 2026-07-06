import math

import streamlit as st


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

        html, body, [data-testid="stAppViewContainer"]{
            background-color: var(--bg) !important;
            color: var(--text);
            font-family: 'Inter', sans-serif;
        }
        [data-testid="stAppViewContainer"]{
            background-image:
                radial-gradient(1000px circle at 0% -10%, rgba(70,194,160,0.38), transparent 45%),
                radial-gradient(900px circle at 105% 10%, rgba(90,169,230,0.32), transparent 50%),
                radial-gradient(1100px circle at 40% 115%, rgba(155,90,255,0.28), transparent 55%),
                radial-gradient(700px circle at 85% 90%, rgba(226,115,92,0.16), transparent 55%) !important;
            background-attachment: fixed !important;
        }
        [data-testid="stHeader"]{ background-color: transparent; }
        .block-container{ padding-top: 2rem; max-width: 1100px; }

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
            width: 100%;
            border-radius: 8px;
            border: 1px solid var(--border);
            background-color: var(--accent);
            color: #06110D;
            font-weight: 600;
            padding: 0.55rem 0;
            transition: all 0.15s ease;
        }
        .stButton > button:hover{
            background-color: var(--accent-deep);
            border-color: var(--accent-deep);
            color: #fff;
        }
        .stButton > button:active{ transform: scale(0.98); }

        .end-session .stButton > button{
            background-color: transparent;
            color: var(--danger);
            border: 1px solid var(--danger);
        }
        .end-session .stButton > button:hover{ background-color: var(--danger); color: #fff; }

        .ghost-btn .stButton > button{
            background-color: transparent;
            color: var(--text-muted);
            border: 1px solid var(--border);
        }
        .ghost-btn .stButton > button:hover{ border-color: var(--text-muted); color: var(--text); }

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
        .mascot-avatar{ width:46px; height:46px; flex-shrink:0; }
        .mascot-bubble{
            position:relative;
            background-color: var(--surface-2);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 0.6rem 1rem;
            font-size: 0.88rem;
            color: var(--text);
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

def render_mascot(message):
    """Original mascot — a small hourglass spirit that reacts to your sessions."""
    st.markdown(
        f"""
        <div class="mascot-row">
            <svg class="mascot-avatar" viewBox="0 0 64 64">
                <circle cx="32" cy="32" r="30" fill="var(--accent-soft)"/>
                <path d="M20 14 h24 a3 3 0 0 1 0 6 L34 32 l10 12 a3 3 0 0 1 0 6 H20
                         a3 3 0 0 1 0-6 l10-12 -10-12 a3 3 0 0 1 0-6 Z"
                      fill="var(--accent)"/>
                <circle cx="27" cy="24" r="2.4" fill="#06110D"/>
                <circle cx="37" cy="24" r="2.4" fill="#06110D"/>
                <path d="M26 42 q6 5 12 0" stroke="#06110D" stroke-width="2" fill="none" stroke-linecap="round"/>
            </svg>
            <div class="mascot-bubble">{message}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_live_readout(start_time, task_label):
    start_ts_ms = int(start_time.timestamp() * 1000)
    start_label = start_time.strftime("%H:%M")

    st.markdown(
        f"""
        <div class="active-session-row">
            <div class="sweep-ring" id="chronos-sweep-ring"></div>
            <div>
                <div class="timer-meta">Tracking <b>{task_label}</b> · started at {start_label}</div>
                <div id="chronos-live-timer" class="timer-readout">00:00:00</div>
            </div>
        </div>
        <script>
        (function() {{
            const startTs = {start_ts_ms};
            const el = document.getElementById('chronos-live-timer');
            const ring = document.getElementById('chronos-sweep-ring');
            function tick() {{
                if (!el) return;
                const diff = Math.max(0, Date.now() - startTs);
                const h = String(Math.floor(diff / 3600000)).padStart(2, '0');
                const m = String(Math.floor((diff % 3600000) / 60000)).padStart(2, '0');
                const s = String(Math.floor((diff % 60000) / 1000)).padStart(2, '0');
                el.textContent = h + ':' + m + ':' + s;
                if (ring) {{
                    const secondsIntoMinute = Math.floor(diff / 1000) % 60;
                    ring.style.setProperty('--sweep', (secondsIntoMinute / 60 * 100).toFixed(2));
                }}
            }}
            tick();
            setInterval(tick, 1000);
        }})();
        </script>
        """,
        unsafe_allow_html=True,
    )
