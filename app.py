"""
Multimodal Construction Intelligence Platform
Skill Wallet Capstone Project 1
=============================================
A production-ready Streamlit application leveraging Google Gemini's multimodal
capabilities for construction site safety, structural analysis, project valuation,
and intelligent site assistance.
"""

import streamlit as st
import google.generativeai as genai
import json
import base64
import io
import time
import random
import math
import requests
from PIL import Image
from datetime import datetime

# ─────────────────────────────────────────────
# PAGE CONFIGURATION
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Construction Intelligence Platform",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL CSS STYLING
# ─────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ── Root Variables ── */
    :root {
        --primary:      #FF6B00;
        --primary-dark: #CC5500;
        --accent:       #FFB347;
        --bg-base:      #0D0F14;
        --bg-card:      #161A22;
        --bg-card2:     #1E232E;
        --border:       rgba(255,107,0,0.18);
        --border-soft:  rgba(255,255,255,0.07);
        --text-main:    #F0F2F5;
        --text-muted:   #8892A0;
        --success:      #22C55E;
        --warning:      #F59E0B;
        --danger:       #EF4444;
        --critical:     #DC2626;
        --info:         #3B82F6;
        --radius:       12px;
        --shadow:       0 4px 24px rgba(0,0,0,0.4);
    }

    /* ── Global Reset ── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: var(--text-main);
    }
    .stApp {
        background: var(--bg-base);
    }

    /* ── Hide Streamlit defaults ── */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0A0C12 0%, #111520 100%);
        border-right: 1px solid var(--border);
    }
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: var(--primary) !important;
    }

    /* ── Hero Banner ── */
    .hero-banner {
        background: linear-gradient(135deg, #FF6B00 0%, #FF8C38 40%, #CC5500 100%);
        border-radius: var(--radius);
        padding: 2rem 2.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(255,107,0,0.3);
        position: relative;
        overflow: hidden;
    }
    .hero-banner::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 300px;
        height: 300px;
        background: rgba(255,255,255,0.05);
        border-radius: 50%;
    }
    .hero-banner h1 {
        font-size: 1.9rem;
        font-weight: 800;
        color: white;
        margin: 0 0 0.5rem;
        line-height: 1.2;
    }
    .hero-banner p {
        color: rgba(255,255,255,0.85);
        font-size: 0.95rem;
        margin: 0;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        color: white;
        font-size: 0.72rem;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 20px;
        margin-bottom: 0.75rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    /* ── Tab Styling ── */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-card);
        border-radius: var(--radius);
        padding: 4px;
        gap: 2px;
        border: 1px solid var(--border-soft);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: var(--text-muted);
        font-weight: 500;
        font-size: 0.88rem;
        padding: 0.55rem 1.1rem;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: var(--primary) !important;
        color: white !important;
    }

    /* ── Cards ── */
    .card {
        background: var(--bg-card);
        border: 1px solid var(--border-soft);
        border-radius: var(--radius);
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: var(--shadow);
        transition: border-color 0.2s ease, transform 0.15s ease;
    }
    .card:hover {
        border-color: var(--border);
        transform: translateY(-1px);
    }
    .card-title {
        font-size: 0.78rem;
        font-weight: 600;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.5rem;
    }
    .card-value {
        font-size: 2rem;
        font-weight: 800;
        color: var(--text-main);
        line-height: 1;
    }
    .card-sub {
        font-size: 0.8rem;
        color: var(--text-muted);
        margin-top: 0.35rem;
    }

    /* ── Status Pills ── */
    .pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }
    .pill-safe    { background: rgba(34,197,94,0.15);  color: #22C55E; border: 1px solid rgba(34,197,94,0.3); }
    .pill-warning { background: rgba(245,158,11,0.15); color: #F59E0B; border: 1px solid rgba(245,158,11,0.3); }
    .pill-danger  { background: rgba(239,68,68,0.15);  color: #EF4444; border: 1px solid rgba(239,68,68,0.3); }
    .pill-critical{ background: rgba(220,38,38,0.2);   color: #DC2626; border: 1px solid rgba(220,38,38,0.4); }
    .pill-info    { background: rgba(59,130,246,0.15); color: #3B82F6; border: 1px solid rgba(59,130,246,0.3); }

    /* ── Section Headers ── */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin: 1.5rem 0 1rem;
        padding-bottom: 0.6rem;
        border-bottom: 1px solid var(--border-soft);
    }
    .section-icon {
        width: 36px;
        height: 36px;
        background: linear-gradient(135deg, var(--primary), var(--accent));
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        flex-shrink: 0;
    }
    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--text-main);
    }
    .section-sub {
        font-size: 0.78rem;
        color: var(--text-muted);
    }

    /* ── PPE Checklist Table ── */
    .ppe-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.88rem;
    }
    .ppe-table th {
        text-align: left;
        padding: 10px 14px;
        background: var(--bg-card2);
        color: var(--text-muted);
        font-size: 0.74rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        border-bottom: 1px solid var(--border-soft);
    }
    .ppe-table td {
        padding: 10px 14px;
        border-bottom: 1px solid var(--border-soft);
        color: var(--text-main);
    }
    .ppe-table tr:last-child td { border-bottom: none; }
    .ppe-table tr:hover td { background: rgba(255,107,0,0.04); }

    /* ── Hazard Cards ── */
    .hazard-card {
        background: var(--bg-card2);
        border-left: 4px solid var(--danger);
        border-radius: 8px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
    }
    .hazard-card.low      { border-color: var(--success); }
    .hazard-card.medium   { border-color: var(--warning); }
    .hazard-card.high     { border-color: var(--danger); }
    .hazard-card.critical { border-color: var(--critical); }
    .hazard-title {
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 0.35rem;
    }
    .hazard-remedy {
        font-size: 0.83rem;
        color: var(--text-muted);
        line-height: 1.5;
    }

    /* ── Metric Score Ring ── */
    .score-ring-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 1.5rem;
    }
    .score-ring-label {
        font-size: 0.78rem;
        font-weight: 600;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 0.75rem;
    }

    /* ── Progress Bar ── */
    .progress-container {
        background: var(--bg-card2);
        border-radius: 20px;
        height: 10px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    .progress-bar {
        height: 100%;
        border-radius: 20px;
        background: linear-gradient(90deg, var(--primary), var(--accent));
        transition: width 0.6s ease;
    }

    /* ── Chatbot ── */
    .chat-container {
        max-height: 420px;
        overflow-y: auto;
        padding: 1rem;
        background: var(--bg-card2);
        border-radius: var(--radius);
        border: 1px solid var(--border-soft);
        margin-bottom: 1rem;
    }
    .chat-msg {
        margin-bottom: 1rem;
        display: flex;
        gap: 0.75rem;
    }
    .chat-msg.user { flex-direction: row-reverse; }
    .chat-avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        flex-shrink: 0;
    }
    .chat-avatar.bot  { background: linear-gradient(135deg, var(--primary), var(--accent)); }
    .chat-avatar.user { background: var(--info); }
    .chat-bubble {
        max-width: 75%;
        padding: 0.75rem 1rem;
        border-radius: 14px;
        font-size: 0.88rem;
        line-height: 1.55;
    }
    .chat-bubble.bot  {
        background: var(--bg-card);
        border: 1px solid var(--border-soft);
        color: var(--text-main);
        border-radius: 4px 14px 14px 14px;
    }
    .chat-bubble.user {
        background: var(--primary);
        color: white;
        border-radius: 14px 4px 14px 14px;
    }

    /* ── Weather Alert ── */
    .weather-alert {
        border-radius: var(--radius);
        padding: 1.25rem 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid;
    }
    .weather-alert.extreme {
        background: rgba(220,38,38,0.1);
        border-color: rgba(220,38,38,0.3);
    }
    .weather-alert.warning {
        background: rgba(245,158,11,0.1);
        border-color: rgba(245,158,11,0.3);
    }
    .weather-alert.normal {
        background: rgba(34,197,94,0.08);
        border-color: rgba(34,197,94,0.25);
    }
    .weather-alert-title {
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .weather-alert-body {
        font-size: 0.85rem;
        line-height: 1.6;
        color: var(--text-muted);
    }

    /* ── Demo Mode Banner ── */
    .demo-banner {
        background: rgba(245,158,11,0.12);
        border: 1px solid rgba(245,158,11,0.35);
        border-radius: 8px;
        padding: 0.75rem 1rem;
        font-size: 0.82rem;
        color: #F59E0B;
        margin-bottom: 1.25rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* ── Upload Area ── */
    [data-testid="stFileUploader"] {
        background: var(--bg-card2) !important;
        border: 2px dashed var(--border) !important;
        border-radius: var(--radius) !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.9rem;
        padding: 0.6rem 1.5rem;
        transition: all 0.2s ease;
        box-shadow: 0 4px 12px rgba(255,107,0,0.25);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255,107,0,0.4);
    }
    .stButton > button:active { transform: translateY(0); }

    /* ── Divider ── */
    .custom-divider {
        border: none;
        border-top: 1px solid var(--border-soft);
        margin: 1.5rem 0;
    }

    /* ── Code blocks ── */
    .stCodeBlock {
        background: #0A0C10 !important;
        border: 1px solid var(--border-soft) !important;
    }

    /* ── Sidebar nav items ── */
    .nav-item {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        padding: 0.6rem 0.8rem;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 500;
        color: var(--text-muted);
        margin-bottom: 2px;
        cursor: default;
        transition: background 0.15s ease;
    }
    .nav-item:hover { background: rgba(255,107,0,0.08); color: var(--text-main); }
    .nav-item .nav-icon { font-size: 1rem; }

    /* ── Rendering image placeholder ── */
    .render-placeholder {
        background: linear-gradient(135deg, var(--bg-card2), #1a1f2e);
        border: 1px dashed var(--border);
        border-radius: var(--radius);
        padding: 3rem 2rem;
        text-align: center;
        color: var(--text-muted);
    }

    /* ── Tooltip ── */
    .tooltip-text {
        font-size: 0.78rem;
        color: var(--text-muted);
        font-style: italic;
        margin-top: 0.25rem;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-base); }
    ::-webkit-scrollbar-thumb { background: rgba(255,107,0,0.35); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(255,107,0,0.55); }
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# UTILITY HELPERS
# ─────────────────────────────────────────────
def is_demo_mode():
    return not bool(st.session_state.get("gemini_api_key", "").strip())


def get_model():
    """Return a configured Gemini model or None in demo mode."""
    if is_demo_mode():
        return None
    try:
        genai.configure(api_key=st.session_state["gemini_api_key"].strip())
        return genai.GenerativeModel("gemini-1.5-flash")
    except Exception:
        return None


def image_to_bytes(pil_img):
    buf = io.BytesIO()
    pil_img.save(buf, format="JPEG", quality=92)
    return buf.getvalue()


def render_demo_notice():
    st.markdown(
        '<div class="demo-banner">⚡ <strong>Demo Mode</strong> — Enter your Gemini API key in the sidebar to unlock live AI analysis.</div>',
        unsafe_allow_html=True,
    )


def section_header(icon, title, subtitle=""):
    sub_html = f'<div class="section-sub">{subtitle}</div>' if subtitle else ""
    st.markdown(f"""
    <div class="section-header">
        <div class="section-icon">{icon}</div>
        <div>
            <div class="section-title">{title}</div>
            {sub_html}
        </div>
    </div>
    """, unsafe_allow_html=True)


def pill(text, style="info"):
    icons = {"safe": "✅", "warning": "⚠️", "danger": "🔴", "critical": "🚨", "info": "ℹ️"}
    st.markdown(f'<span class="pill pill-{style}">{icons.get(style,"•")} {text}</span>',
                unsafe_allow_html=True)


def metric_card(title, value, sub="", col=None):
    html = f"""
    <div class="card">
        <div class="card-title">{title}</div>
        <div class="card-value">{value}</div>
        {'<div class="card-sub">' + sub + '</div>' if sub else ''}
    </div>"""
    if col:
        col.markdown(html, unsafe_allow_html=True)
    else:
        st.markdown(html, unsafe_allow_html=True)


def progress_bar_html(pct, label=""):
    return f"""
    <div style="margin-bottom:0.5rem;">
        {'<div style="font-size:0.82rem;color:var(--text-muted);margin-bottom:4px;">' + label + '</div>' if label else ''}
        <div class="progress-container">
            <div class="progress-bar" style="width:{pct}%"></div>
        </div>
        <div style="font-size:0.78rem;color:var(--text-muted);text-align:right;">{pct:.0f}%</div>
    </div>"""


def score_svg(score, color="#FF6B00"):
    """Render an SVG donut ring for a 0–100 score."""
    r = 54
    c = 2 * math.pi * r
    filled = c * score / 100
    gap = c - filled
    text_color = color
    return f"""
    <div class="score-ring-wrapper">
        <svg width="140" height="140" viewBox="0 0 140 140">
            <circle cx="70" cy="70" r="{r}" fill="none" stroke="#1E232E" stroke-width="14"/>
            <circle cx="70" cy="70" r="{r}" fill="none" stroke="{color}" stroke-width="14"
                stroke-dasharray="{filled:.1f} {gap:.1f}"
                stroke-dashoffset="{c*0.25:.1f}"
                stroke-linecap="round"/>
            <text x="70" y="66" text-anchor="middle" font-size="24" font-weight="800"
                fill="{text_color}" font-family="Inter,sans-serif">{score}</text>
            <text x="70" y="84" text-anchor="middle" font-size="11" fill="#8892A0"
                font-family="Inter,sans-serif">/100</text>
        </svg>
        <div class="score-ring-label">Safety Score</div>
    </div>"""


# ─────────────────────────────────────────────
# DEMO DATA GENERATORS
# ─────────────────────────────────────────────
DEMO_SAFETY_RESULT = {
    "safety_score": 72,
    "overall_status": "Moderate Risk",
    "ppe_detection": [
        {"item": "Safety Helmet / Hard Hat", "compliant": True,  "coverage_pct": 90, "notes": "Majority wearing helmets; 1 worker without"},
        {"item": "High-Visibility Vest",     "compliant": True,  "coverage_pct": 85, "notes": "Most workers equipped"},
        {"item": "Steel-Toe Boots",          "compliant": False, "coverage_pct": 60, "notes": "Several workers in non-compliant footwear"},
        {"item": "Safety Harness",           "compliant": False, "coverage_pct": 40, "notes": "Elevation work detected without harness"},
        {"item": "Safety Goggles",           "compliant": True,  "coverage_pct": 75, "notes": "Adequate near grinding zones"},
        {"item": "Gloves",                   "compliant": True,  "coverage_pct": 80, "notes": "Present in material-handling areas"},
    ],
    "site_hazards": [
        {"hazard": "Unsecured Scaffolding",  "severity": "Critical", "remedy": "Immediately halt work; re-inspect all scaffold clamps and bracing per IS 3696. Install toe-boards and mid-rails."},
        {"hazard": "Open Excavation Pit",    "severity": "High",     "remedy": "Install perimeter barriers ≥1 m from edge. Place reflective signage per OSHA 29 CFR 1926.652."},
        {"hazard": "Electrical Cable Exposure","severity": "High",   "remedy": "De-energize circuit, apply insulation tape, route cables through conduit overhead."},
        {"hazard": "Housekeeping — Debris",  "severity": "Medium",   "remedy": "Clear walkways, implement daily 5S routine. Designate skip bins within 15 m radius."},
        {"hazard": "Insufficient Lighting",  "severity": "Low",      "remedy": "Add temporary floodlights (min 50 lux) per IS 3646. Replace burnt-out units immediately."},
    ],
    "compliance_standards": ["OSHA 29 CFR 1926", "IS 456:2000", "IS 3696:1966"],
    "generated_at": datetime.now().isoformat(),
}

DEMO_CRACK_RESULT = {
    "defect_type": "Settlement Crack",
    "confidence": 82,
    "crack_width_mm": 3.2,
    "severity": "High",
    "root_causes": [
        "Differential foundation settlement due to varying subsoil bearing capacity",
        "Inadequate soil compaction during site preparation",
        "Possible water ingress causing soil liquefaction below foundation",
    ],
    "affected_zone": "South-west corner column-beam junction, extending 1.2 m vertically",
    "repairs": [
        {"method": "Epoxy Injection",       "description": "Inject low-viscosity epoxy resin (LPL grade) under 0.3–0.5 MPa pressure into sealed crack ports at 200 mm spacing. Structural strength recovery ~95%."},
        {"method": "Structural Re-grouting","description": "High-pressure cementitious grout injection to fill voids beneath foundation slab, followed by underpinning with micro-piles."},
        {"method": "Surface Sealing",       "description": "Apply elastomeric polyurethane sealant for waterproofing after primary structural repair to prevent further water ingress."},
    ],
    "urgency": "Urgent — Structural Assessment Required Within 72 Hours",
    "standards": ["IS 456:2000 Clause 8", "IS 13920:1993"],
    "generated_at": datetime.now().isoformat(),
}


def generate_demo_valuation(struct_type, sqft, tier, completion):
    """Produce deterministic valuation figures for demo mode."""
    base_cost_psf = {"Residential Apartment": 2800, "Commercial Complex": 3800, "Industrial Shed": 1800,
                     "Villa / Bungalow": 4200, "Mixed-Use Township": 3400}
    market_mult = {"Tier 1 (Metro)": 1.65, "Tier 2 (Urban)": 1.25, "Tier 3 (Semi-Urban)": 0.9}
    steel_psf = 4.5     # kg per sqft
    cement_psf = 0.22   # bags per sqft

    base = base_cost_psf.get(struct_type, 3000)
    mult = market_mult.get(tier, 1.0)
    total_budget   = round(base * sqft, 0)
    capex_incurred = round(total_budget * completion / 100, 0)
    market_val     = round(total_budget * mult * (0.7 + 0.3 * completion / 100), 0)
    steel_req      = round(steel_psf * sqft, 0)
    cement_req     = round(cement_psf * sqft, 0)

    def to_lakh_crore(val):
        if val >= 1e7:
            return f"₹ {val/1e7:.2f} Cr"
        return f"₹ {val/1e5:.2f} L"

    return {
        "total_budget":   to_lakh_crore(total_budget),
        "capex_incurred": to_lakh_crore(capex_incurred),
        "market_value":   to_lakh_crore(market_val),
        "steel_kg":       f"{steel_req:,.0f} kg",
        "cement_bags":    f"{cement_req:,.0f} bags",
        "raw_budget":     total_budget,
        "raw_capex":      capex_incurred,
        "raw_market":     market_val,
    }


WEATHER_ADVISORIES = {
    "High Wind (>60 km/h)": {
        "level": "extreme",
        "icon": "💨",
        "alerts": [
            ("🚫 Crane Operations SUSPENDED",      "extreme", "All crane and lifting operations must be halted immediately. Wind speed exceeds AS 4991 safe operating limit of 48 km/h."),
            ("⚠️  Scaffolding Inspection",          "warning", "Conduct emergency scaffold tie inspection. Ensure all ties are at ≤4 m horizontal and ≤3.5 m vertical intervals per IS 3696."),
            ("🚧 Material Securing",               "warning", "Tarp all loose aggregate, plywood, and sheet materials. Remove objects from elevation zones. Risk of projectile debris injury."),
            ("🔌 Temporary Structures",            "warning", "Verify all temporary electrical hookups are rated for exposed-site use. Secure cable runs with additional fasteners."),
            ("📢 Worker Advisory",                 "warning", "Restrict work above 3 m elevation. Issue high-wind personal safety briefing. Buddy-system mandatory on all elevated zones."),
        ],
    },
    "Heavy Rain": {
        "level": "warning",
        "icon": "🌧️",
        "alerts": [
            ("⚡ Electrical Hazard Protocol",      "danger",  "De-energize all non-weatherproof temporary power panels. Ground all generators. Insulate exposed cable terminations."),
            ("🏗️  Concrete Curing Advisory",        "warning", "Suspend fresh concrete pours. Cover all green concrete with polyethylene sheeting. Delay curing compounds — rain washout likely."),
            ("🕳️  Excavation Monitoring",           "warning", "Pump standing water from all open excavations immediately. Check trench shoring integrity every 30 minutes during rainfall."),
            ("🦺 Slip-Fall Prevention",            "warning", "Issue anti-slip footwear directive. Place temporary matting at access ramps. Increase housekeeping frequency on working platforms."),
            ("📐 Soil Stability Check",            "warning", "Commission geotechnical inspection if rainfall exceeds 50 mm/hr. Monitor settlement survey benchmarks after storm."),
        ],
    },
    "Extreme Heat (>42°C)": {
        "level": "extreme",
        "icon": "🌡️",
        "alerts": [
            ("🧊 Heat-Stroke Prevention",          "extreme", "Mandatory 15-min rest every 45 min of outdoor work. Provide 250 ml water/hr per worker. Set up shaded rest zones ≥4 m × 4 m."),
            ("🏗️  Concrete & Mortar Adaptation",    "warning", "Reduce w/c ratio, use chilled mixing water, and add retarding admixtures to extend workability (IS 9103:1999). Avoid midday pours (11 am–4 pm)."),
            ("🚑 Medical Readiness",               "warning", "First-aid station must stock oral rehydration salts, cool packs, and shade canopy. Identify and brief nearest hospital emergency contacts."),
            ("⚙️  Equipment Cooling",               "warning", "Inspect engine coolant levels for all heavy machinery. Reduce generator load factors to 70%. Monitor hydraulic fluid temps."),
            ("📋 Modified Work Schedule",          "warning", "Shift heavy labour to early morning (6–10 am) and late evening (5–7 pm). Document heat-index monitoring at site every hour."),
        ],
    },
    "Normal Conditions": {
        "level": "normal",
        "icon": "☀️",
        "alerts": [
            ("✅ Standard Safety Protocols",       "safe",    "All routine PPE and safety measures apply. Conduct scheduled toolbox talk. Verify first-aid kit inventory and equipment pre-use checks."),
            ("📋 Daily Inspection Checklist",      "info",    "Complete morning site walk using IS 4130 checklist. Sign-off required from Safety Officer before mobilising workforce."),
            ("🔧 Equipment Maintenance Window",    "info",    "Optimal conditions for planned maintenance. Service compressors, check slinging gear, and calibrate surveying instruments."),
        ],
    },
}

CHATBOT_DEMO_RESPONSES = [
    "Based on IS 456:2000, for M25 concrete grade you need a minimum cement content of 300 kg/m³ with a maximum w/c ratio of 0.50. For severe exposure zones, reduce this to 320 kg/m³.",
    "For RCC column design per IS 456, the minimum eccentricity must be ≥ 20 mm or L/500 + D/30, whichever is greater. Ensure lateral ties at spacing not exceeding 300 mm or least lateral dimension.",
    "Scaffolding erected per IS 3696 Part 1 must have base plates on sound foundations, cross-bracing at every third frame, and working platforms ≥450 mm wide with toe-boards of ≥150 mm height.",
    "For concrete curing in hot weather (>35°C), IS 456 recommends moist curing for minimum 14 days for OPC and 10 days for blended cements, using wet burlap, curing compounds, or ponding methods.",
    "Per OSHA 29 CFR 1926.502, fall protection is mandatory at heights ≥1.8 m (6 ft) on construction sites. Acceptable systems include guardrails, safety nets, and personal fall arrest systems with anchors rated for 22.2 kN.",
]


# ─────────────────────────────────────────────
# AI ANALYSIS FUNCTIONS
# ─────────────────────────────────────────────
def analyze_ppe(image_bytes, model):
    """Call Gemini to analyze PPE compliance from an image."""
    if model is None:
        time.sleep(1.5)
        result = DEMO_SAFETY_RESULT.copy()
        result["safety_score"] = random.randint(55, 88)
        result["generated_at"] = datetime.now().isoformat()
        return result

    prompt = """You are a certified construction safety inspector. Analyze this construction site photo meticulously.

Return ONLY a valid JSON object (no markdown, no code fences) with this exact schema:
{
  "safety_score": <integer 0-100>,
  "overall_status": "<Compliant | Moderate Risk | High Risk | Critical Risk>",
  "ppe_detection": [
    {
      "item": "<PPE item name>",
      "compliant": <true|false>,
      "coverage_pct": <integer 0-100>,
      "notes": "<brief observation>"
    }
  ],
  "site_hazards": [
    {
      "hazard": "<hazard name>",
      "severity": "<Low|Medium|High|Critical>",
      "remedy": "<specific corrective action>"
    }
  ],
  "compliance_standards": ["<applicable standard>"],
  "generated_at": "<ISO timestamp>"
}

PPE items to evaluate: Safety Helmet/Hard Hat, High-Visibility Vest, Steel-Toe Boots, Safety Harness (if working at height), Safety Goggles, Gloves.
Hazard categories: falls, electrical, struck-by, caught-in, housekeeping, fire, structural.
Apply OSHA 29 CFR 1926 and IS 456:2000 standards. Be specific and actionable."""

    try:
        img_part = {"mime_type": "image/jpeg", "data": base64.b64encode(image_bytes).decode()}
        resp = model.generate_content([prompt, img_part])
        text = resp.text.strip()
        # Strip accidental code fences
        if text.startswith("```"):
            text = "\n".join(text.split("\n")[1:])
            text = text.rsplit("```", 1)[0]
        return json.loads(text)
    except Exception as e:
        st.error(f"AI analysis error: {e}")
        return DEMO_SAFETY_RESULT


def analyze_crack(image_bytes, model):
    """Call Gemini to classify concrete crack defects."""
    if model is None:
        time.sleep(1.5)
        result = DEMO_CRACK_RESULT.copy()
        result["generated_at"] = datetime.now().isoformat()
        return result

    prompt = """You are a structural engineer specializing in concrete diagnostics. Analyze this crack/defect image.

Return ONLY a valid JSON object (no markdown, no code fences):
{
  "defect_type": "<Hairline | Settlement Crack | Structural Shear Crack | Thermal Expansion Crack | Spalling | Map/Pattern Cracking | Other>",
  "confidence": <integer 0-100>,
  "crack_width_mm": <float>,
  "severity": "<Low|Medium|High|Critical>",
  "root_causes": ["<cause 1>", "<cause 2>"],
  "affected_zone": "<description of location and extent>",
  "repairs": [
    {
      "method": "<repair method>",
      "description": "<detailed procedure>"
    }
  ],
  "urgency": "<description of time-sensitivity>",
  "standards": ["<IS/OSHA standard>"],
  "generated_at": "<ISO timestamp>"
}

Classify carefully: Hairline <0.2mm, Medium 0.2-1mm, Wide >1mm. Reference IS 456:2000 Table 19 for permissible crack widths. Recommend epoxy injection, structural re-grouting, spalling repair, or other methods as appropriate."""

    try:
        img_part = {"mime_type": "image/jpeg", "data": base64.b64encode(image_bytes).decode()}
        resp = model.generate_content([prompt, img_part])
        text = resp.text.strip()
        if text.startswith("```"):
            text = "\n".join(text.split("\n")[1:])
            text = text.rsplit("```", 1)[0]
        return json.loads(text)
    except Exception as e:
        st.error(f"AI analysis error: {e}")
        return DEMO_CRACK_RESULT


def chat_with_assistant(user_msg, history, model):
    """Send a message to the Gemini construction assistant."""
    if model is None:
        time.sleep(0.8)
        return random.choice(CHATBOT_DEMO_RESPONSES)

    system_context = """You are ConstructAI, a senior construction engineering assistant with expertise in:
- Indian Standards (IS 456, IS 800, IS 875, IS 1343, NBC 2016)
- OSHA safety regulations (29 CFR 1926)
- Structural design, RCC, steel, and pre-stressed concrete
- Project management and valuation (RERA, CPWD rates)
- Construction materials (cement, steel, aggregates)
- Site safety, PPE, and emergency protocols

Provide concise, technically accurate answers. Cite specific IS clause numbers or OSHA standards when relevant.
Format responses clearly with bullet points or numbered steps where appropriate. Keep answers under 200 words unless complex calculations are required."""

    try:
        # Build conversation history
        contents = [{"role": "user", "parts": [system_context + "\n\nUser: " + user_msg]}]
        if len(history) > 1:
            gemini_history = []
            for msg in history[-8:]:  # last 4 exchanges
                role = "user" if msg["role"] == "user" else "model"
                gemini_history.append({"role": role, "parts": [msg["content"]]})
            chat = model.start_chat(history=gemini_history[:-1] if gemini_history else [])
            resp = chat.send_message(user_msg)
        else:
            resp = model.generate_content(system_context + "\n\n" + user_msg)
        return resp.text
    except Exception as e:
        return f"⚠️ Could not generate response: {e}"


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        # Logo + Title
        st.markdown("""
        <div style="text-align:center;padding:1rem 0 0.5rem;">
            <div style="font-size:2.5rem;margin-bottom:0.25rem;">🏗️</div>
            <div style="font-size:1.05rem;font-weight:800;color:#FF6B00;line-height:1.2;">Construction</div>
            <div style="font-size:1.05rem;font-weight:800;color:#FF6B00;">Intelligence Platform</div>
            <div style="font-size:0.72rem;color:#8892A0;margin-top:0.3rem;letter-spacing:0.05em;">SKILL WALLET · CAPSTONE 1</div>
        </div>
        <hr style="border:none;border-top:1px solid rgba(255,107,0,0.2);margin:0.75rem 0;">
        """, unsafe_allow_html=True)

        # API Key Input
        st.markdown("#### 🔑 API Configuration")
        api_key = st.text_input(
            "Google Gemini API Key",
            type="password",
            value=st.session_state.get("gemini_api_key", ""),
            placeholder="AIza...",
            help="Get your key at https://aistudio.google.com/app/apikey",
        )
        if api_key != st.session_state.get("gemini_api_key", ""):
            st.session_state["gemini_api_key"] = api_key
            st.rerun()

        if api_key:
            st.markdown('<div style="color:#22C55E;font-size:0.8rem;">✅ API Key configured — Live AI mode active</div>',
                        unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#F59E0B;font-size:0.8rem;">⚡ Demo mode — No AI key provided</div>',
                        unsafe_allow_html=True)

        st.markdown("<hr style='border:none;border-top:1px solid rgba(255,255,255,0.07);margin:1rem 0;'>",
                    unsafe_allow_html=True)

        # Architecture
        st.markdown("#### 🏛️ Architecture Overview")
        st.markdown("""
        <div style="font-size:0.8rem;color:#8892A0;line-height:1.8;">
        <b style="color:#FF6B00;">Frontend</b> → Streamlit 1.35+<br>
        <b style="color:#FF6B00;">AI Core</b> → Gemini 1.5 Flash<br>
        <b style="color:#FF6B00;">Vision</b> → Multimodal Prompting<br>
        <b style="color:#FF6B00;">Standards</b> → IS 456, OSHA CFR 1926<br>
        <b style="color:#FF6B00;">Valuation</b> → CPWD Rate Analysis<br>
        <b style="color:#FF6B00;">Deploy</b> → Streamlit Community Cloud
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='border:none;border-top:1px solid rgba(255,255,255,0.07);margin:1rem 0;'>",
                    unsafe_allow_html=True)

        # Feature Nav
        st.markdown("#### 🗺️ Module Navigator")
        navs = [
            ("🦺", "Tab 1", "Site Safety & PPE Audit",   "Epic 2"),
            ("🔍", "Tab 2", "Crack Diagnostics",          "Epic 2"),
            ("💰", "Tab 3", "Planning & Valuation",       "Epic 3"),
            ("🤖", "Tab 4", "Daily Site Assistant",       "Epic 5"),
        ]
        for icon, tab, name, epic in navs:
            st.markdown(f"""
            <div class="nav-item">
                <span class="nav-icon">{icon}</span>
                <span><b style="color:#F0F2F5;">{name}</b><br>
                <span style="font-size:0.72rem;color:#8892A0;">{tab} · {epic}</span></span>
            </div>""", unsafe_allow_html=True)

        st.markdown("<hr style='border:none;border-top:1px solid rgba(255,255,255,0.07);margin:1rem 0;'>",
                    unsafe_allow_html=True)

        # System Info
        st.markdown(f"""
        <div style="font-size:0.72rem;color:#5A6370;text-align:center;padding:0.25rem 0;">
            v1.0.0 · {datetime.now().strftime("%d %b %Y %H:%M")} IST<br>
            © 2024 Skill Wallet Capstone Project
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TAB 1 — SITE SAFETY & PPE AUDIT
# ─────────────────────────────────────────────
def tab_safety():
    if is_demo_mode():
        render_demo_notice()

    section_header("🦺", "Site Safety & PPE Compliance Audit",
                   "OSHA 29 CFR 1926 · IS 456:2000 · Multimodal AI Analysis")

    st.markdown("""
    <div class="card" style="background:linear-gradient(135deg,rgba(255,107,0,0.08),rgba(30,35,46,1));border-color:rgba(255,107,0,0.25);">
        <p style="font-size:0.88rem;color:#8892A0;margin:0;line-height:1.6;">
        Upload a construction site photograph to receive an AI-powered PPE compliance audit. The system evaluates
        worker protective equipment against <b style="color:#FF6B00;">OSHA 29 CFR 1926</b> and
        <b style="color:#FF6B00;">IS 456:2000</b> standards, generates a safety score, identifies site hazards,
        and recommends corrective measures.
        </p>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Upload Construction Site Photo",
        type=["jpg", "jpeg", "png", "webp"],
        help="Supports JPG, PNG, WebP up to 200 MB",
        key="ppe_upload",
    )

    if uploaded:
        col_img, col_ctrl = st.columns([1, 1], gap="large")
        with col_img:
            img = Image.open(uploaded)
            st.image(img, caption="📸 Uploaded Site Photo", use_container_width=True)
            st.markdown(f"""
            <div style="font-size:0.78rem;color:#8892A0;margin-top:0.5rem;">
                📁 {uploaded.name} · {img.size[0]}×{img.size[1]}px · {uploaded.size//1024} KB
            </div>""", unsafe_allow_html=True)

        with col_ctrl:
            st.markdown("""
            <div class="card">
                <div class="card-title">Analysis Parameters</div>
                <div style="font-size:0.85rem;color:#8892A0;margin:0.5rem 0 1rem;">
                    The AI model will evaluate:<br>
                    • PPE coverage per worker<br>
                    • Fall protection compliance<br>
                    • Site hazard identification<br>
                    • OSHA & IS 456 adherence
                </div>
            </div>
            """, unsafe_allow_html=True)

            run_btn = st.button("🔍 Run Safety Audit", use_container_width=True, key="run_ppe")

        if run_btn or st.session_state.get("ppe_result"):
            if run_btn:
                with st.spinner("🤖 AI analyzing site safety conditions..."):
                    model = get_model()
                    img_bytes = image_to_bytes(img)
                    result = analyze_ppe(img_bytes, model)
                    st.session_state["ppe_result"] = result

            result = st.session_state.get("ppe_result", {})
            if not result:
                return

            st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)
            section_header("📊", "Audit Results", "AI-Generated Safety Report")

            # Score + status row
            score = result.get("safety_score", 0)
            status = result.get("overall_status", "Unknown")
            score_col, status_col, stds_col = st.columns([1, 1.5, 1.5])

            score_color = "#22C55E" if score >= 80 else "#F59E0B" if score >= 60 else "#EF4444"
            score_col.markdown(score_svg(score, score_color), unsafe_allow_html=True)

            with status_col:
                st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
                pill_style = "safe" if score >= 80 else "warning" if score >= 60 else "danger"
                st.markdown(f'<div class="card"><div class="card-title">Overall Status</div>'
                            f'<div style="margin:0.75rem 0"><span class="pill pill-{pill_style}">{"✅" if score>=80 else "⚠️" if score>=60 else "🔴"} {status}</span></div>'
                            f'<div class="card-sub">Site evaluated {datetime.now().strftime("%d %b %Y, %H:%M")} IST</div></div>',
                            unsafe_allow_html=True)

            with stds_col:
                st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
                stds = result.get("compliance_standards", [])
                stds_html = "".join([f'<div style="display:flex;align-items:center;gap:6px;margin-bottom:6px;font-size:0.83rem;"><span style="color:#FF6B00;">⚖️</span> {s}</div>' for s in stds])
                st.markdown(f'<div class="card"><div class="card-title">Applied Standards</div><div style="margin-top:0.5rem;">{stds_html}</div></div>',
                            unsafe_allow_html=True)

            # PPE Checklist
            st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
            section_header("🦺", "PPE Detection Checklist")
            ppe_items = result.get("ppe_detection", [])

            table_rows = ""
            for item in ppe_items:
                icon = "✅" if item.get("compliant") else "❌"
                pct = item.get("coverage_pct", 0)
                bar_color = "#22C55E" if pct >= 80 else "#F59E0B" if pct >= 50 else "#EF4444"
                bar_html = f'<div style="background:#1E232E;border-radius:10px;height:8px;overflow:hidden;width:120px;display:inline-block;"><div style="height:100%;width:{pct}%;background:{bar_color};border-radius:10px;"></div></div> <span style="font-size:0.78rem;color:#8892A0;">{pct}%</span>'
                row_bg = "rgba(34,197,94,0.04)" if item.get("compliant") else "rgba(239,68,68,0.04)"
                table_rows += f"""<tr style="background:{row_bg}">
                    <td><b>{icon} {item.get('item','—')}</b></td>
                    <td>{bar_html}</td>
                    <td><span style="color:{'#22C55E' if item.get('compliant') else '#EF4444'};font-weight:600;">{'Compliant' if item.get('compliant') else 'Non-Compliant'}</span></td>
                    <td style="color:#8892A0;">{item.get('notes','—')}</td>
                </tr>"""

            st.markdown(f"""
            <div class="card" style="overflow-x:auto;">
                <table class="ppe-table">
                    <thead><tr>
                        <th>PPE Item</th><th>Coverage</th><th>Status</th><th>Observations</th>
                    </tr></thead>
                    <tbody>{table_rows}</tbody>
                </table>
            </div>""", unsafe_allow_html=True)

            # Hazards
            hazards = result.get("site_hazards", [])
            if hazards:
                section_header("⚠️", "Site Hazards Identified", f"{len(hazards)} hazards detected")
                h_col1, h_col2 = st.columns(2)
                for i, hz in enumerate(hazards):
                    sev = hz.get("severity", "Low").lower()
                    sev_colors = {"low": "#22C55E", "medium": "#F59E0B", "high": "#EF4444", "critical": "#DC2626"}
                    c = sev_colors.get(sev, "#8892A0")
                    col = h_col1 if i % 2 == 0 else h_col2
                    col.markdown(f"""
                    <div class="hazard-card {sev}">
                        <div class="hazard-title">{hz.get('hazard','—')}
                            <span style="float:right;font-size:0.72rem;font-weight:700;color:{c};background:rgba(255,255,255,0.07);padding:2px 8px;border-radius:12px;">{hz.get('severity','—')}</span>
                        </div>
                        <div class="hazard-remedy">🔧 {hz.get('remedy','No remedy specified')}</div>
                    </div>""", unsafe_allow_html=True)

            # Download
            st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
            json_str = json.dumps(result, indent=2)
            st.download_button(
                label="⬇️ Download Full Audit Report (JSON)",
                data=json_str,
                file_name=f"safety_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True,
            )
    else:
        st.markdown("""
        <div class="render-placeholder" style="margin-top:1.5rem;">
            <div style="font-size:3rem;margin-bottom:1rem;">📷</div>
            <div style="font-size:1rem;font-weight:600;color:#F0F2F5;margin-bottom:0.5rem;">Upload a Site Photo to Begin</div>
            <div style="font-size:0.85rem;">Supports JPG, PNG, WebP · Construction site, elevation work, scaffolding photos recommended</div>
        </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TAB 2 — CRACK DIAGNOSTICS
# ─────────────────────────────────────────────
def tab_crack():
    if is_demo_mode():
        render_demo_notice()

    section_header("🔍", "Crack Diagnostics & Structural Integrity Assessment",
                   "IS 456:2000 · IS 13920:1993 · Defect Classification Engine")

    st.markdown("""
    <div class="card" style="background:linear-gradient(135deg,rgba(59,130,246,0.08),rgba(30,35,46,1));border-color:rgba(59,130,246,0.25);">
        <p style="font-size:0.88rem;color:#8892A0;margin:0;line-height:1.6;">
        Upload an image of a concrete wall, column, beam, or slab surface. The AI classifies crack type,
        estimates width in millimetres, identifies root causes, and prescribes engineering repair methods
        (epoxy injection, structural re-grouting, etc.) per <b style="color:#3B82F6;">IS 456:2000</b> and
        <b style="color:#3B82F6;">IS 13920:1993</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Upload Concrete/Wall Surface Image",
        type=["jpg", "jpeg", "png", "webp"],
        help="Best results with clear, well-lit photos of the crack zone",
        key="crack_upload",
    )

    if uploaded:
        col_img, col_meta = st.columns([1, 1], gap="large")
        with col_img:
            img = Image.open(uploaded)
            st.image(img, caption="🔬 Surface Under Analysis", use_container_width=True)

        with col_meta:
            st.markdown("""
            <div class="card">
                <div class="card-title">Diagnostic Parameters</div>
                <div style="font-size:0.85rem;color:#8892A0;margin:0.5rem 0 1rem;line-height:1.8;">
                    The diagnostic engine classifies:<br>
                    • <b style="color:#F0F2F5;">Defect type</b> (Hairline → Structural Shear)<br>
                    • <b style="color:#F0F2F5;">Crack width</b> in millimetres<br>
                    • <b style="color:#F0F2F5;">Root causes</b> (settlement, thermal, etc.)<br>
                    • <b style="color:#F0F2F5;">Repair methods</b> with detailed procedures<br>
                    • <b style="color:#F0F2F5;">Urgency classification</b> and time-to-act
                </div>
            </div>
            """, unsafe_allow_html=True)
            run_btn = st.button("🔬 Diagnose Structure", use_container_width=True, key="run_crack")

        if run_btn or st.session_state.get("crack_result"):
            if run_btn:
                with st.spinner("🤖 AI performing structural diagnosis..."):
                    model = get_model()
                    img_bytes = image_to_bytes(img)
                    result = analyze_crack(img_bytes, model)
                    st.session_state["crack_result"] = result

            result = st.session_state.get("crack_result", {})
            if not result:
                return

            st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)
            section_header("📋", "Diagnostic Report", "AI Structural Assessment")

            # Top metrics
            c1, c2, c3, c4 = st.columns(4)
            defect_icons = {
                "Hairline": "〰️", "Settlement Crack": "📉", "Structural Shear Crack": "⚡",
                "Thermal Expansion Crack": "🌡️", "Spalling": "💥", "Map/Pattern Cracking": "🕸️",
            }
            d_icon = defect_icons.get(result.get("defect_type",""), "🔍")
            sev_map = {"Low": "safe", "Medium": "warning", "High": "danger", "Critical": "critical"}
            sev_pill = sev_map.get(result.get("severity","Low"), "info")

            metric_card("Defect Type",
                        d_icon + " " + result.get("defect_type","—")[:18],
                        f"Confidence: {result.get('confidence',0)}%", c1)
            metric_card("Crack Width",
                        f"{result.get('crack_width_mm',0):.1f} mm",
                        "Estimated visual width", c2)
            metric_card("Severity",
                        result.get("severity","—"),
                        "Per IS 456:2000 Table 19", c3)
            with c4:
                st.markdown(f"""
                <div class="card">
                    <div class="card-title">Urgency</div>
                    <div style="margin-top:0.5rem;font-size:0.82rem;font-weight:600;color:#EF4444;line-height:1.4;">
                        {result.get('urgency','—')}
                    </div>
                </div>""", unsafe_allow_html=True)

            # Root causes
            section_header("🧪", "Root Cause Analysis")
            causes = result.get("root_causes", [])
            cause_html = "".join([
                f'<div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:10px;font-size:0.87rem;">'
                f'<span style="color:#FF6B00;font-weight:700;flex-shrink:0;">{i+1}.</span>'
                f'<span style="color:#F0F2F5;">{c}</span></div>'
                for i, c in enumerate(causes)
            ])
            st.markdown(f'<div class="card">{cause_html}</div>', unsafe_allow_html=True)

            # Affected zone
            zone = result.get("affected_zone", "")
            if zone:
                st.markdown(f"""
                <div class="card" style="border-color:rgba(239,68,68,0.3);">
                    <div class="card-title">📍 Affected Zone</div>
                    <div style="font-size:0.88rem;color:#F0F2F5;margin-top:0.5rem;">{zone}</div>
                </div>""", unsafe_allow_html=True)

            # Repair methods
            section_header("🔧", "Recommended Engineering Repairs")
            repairs = result.get("repairs", [])
            for r in repairs:
                st.markdown(f"""
                <div class="card" style="border-left:4px solid #FF6B00;">
                    <div style="font-size:0.95rem;font-weight:700;color:#FF6B00;margin-bottom:0.5rem;">
                        🔩 {r.get('method','—')}
                    </div>
                    <div style="font-size:0.85rem;color:#8892A0;line-height:1.6;">{r.get('description','—')}</div>
                </div>""", unsafe_allow_html=True)

            # Standards
            stds = result.get("standards", [])
            if stds:
                stds_text = " · ".join([f"<b style='color:#3B82F6;'>{s}</b>" for s in stds])
                st.markdown(f'<div style="font-size:0.8rem;color:#8892A0;margin-top:0.5rem;">⚖️ Standards applied: {stds_text}</div>',
                            unsafe_allow_html=True)

            # Download
            st.download_button(
                label="⬇️ Download Diagnostic Report (JSON)",
                data=json.dumps(result, indent=2),
                file_name=f"crack_diagnostic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True,
            )
    else:
        st.markdown("""
        <div class="render-placeholder" style="margin-top:1.5rem;">
            <div style="font-size:3rem;margin-bottom:1rem;">🧱</div>
            <div style="font-size:1rem;font-weight:600;color:#F0F2F5;margin-bottom:0.5rem;">Upload a Surface Image to Begin</div>
            <div style="font-size:0.85rem;">Concrete walls, columns, beams, slabs, or structural surfaces recommended</div>
        </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TAB 3 — PLANNING & VALUATION
# ─────────────────────────────────────────────
def tab_valuation():
    section_header("💰", "Planning & Real Estate Valuation Engine",
                   "CPWD Rate Analysis · Indian Market Pricing · 3D Concept Rendering")

    # Input Panel
    st.markdown("### 📋 Project Parameters")
    r1c1, r1c2, r1c3 = st.columns(3)
    with r1c1:
        struct_type = st.selectbox("Structure Type", [
            "Residential Apartment", "Commercial Complex", "Industrial Shed",
            "Villa / Bungalow", "Mixed-Use Township",
        ], key="val_struct")
    with r1c2:
        sqft = st.number_input("Built-up Area (sq. ft.)", min_value=500, max_value=500000,
                               value=2400, step=100, key="val_sqft")
    with r1c3:
        tier = st.selectbox("Location Tier", [
            "Tier 1 (Metro)", "Tier 2 (Urban)", "Tier 3 (Semi-Urban)"
        ], key="val_tier")

    completion = st.slider("Completion Percentage (%)", 0, 100, 45, key="val_completion",
                           help="Percentage of project work completed to date")

    # Milestone Progress
    milestones = [
        (10,  "Foundation Complete"),
        (30,  "Substructure Done"),
        (55,  "Superstructure Complete"),
        (75,  "MEP & Finishes"),
        (90,  "Handover Prep"),
        (100, "Project Delivered"),
    ]
    st.markdown("<div style='margin:1rem 0 0.5rem;font-size:0.85rem;font-weight:600;color:#8892A0;text-transform:uppercase;letter-spacing:0.05em;'>Milestone Tracker</div>",
                unsafe_allow_html=True)
    milestone_html = ""
    for pct, label in milestones:
        reached = completion >= pct
        color = "#22C55E" if reached else "#2A2F3D"
        text_color = "#F0F2F5" if reached else "#5A6370"
        milestone_html += f"""
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
            <div style="width:28px;height:28px;border-radius:50%;background:{color};display:flex;align-items:center;justify-content:center;font-size:0.75rem;font-weight:700;color:white;flex-shrink:0;">{'✓' if reached else str(pct)+'%'}</div>
            <div style="font-size:0.85rem;font-weight:{'600' if reached else '400'};color:{text_color};">{label}</div>
            {'<span style="font-size:0.72rem;color:#22C55E;margin-left:auto;">Reached</span>' if reached else ''}
        </div>"""
    st.markdown(f'<div class="card">{progress_bar_html(completion, f"Overall Progress: {completion}%")}{milestone_html}</div>',
                unsafe_allow_html=True)

    # Calculate
    val = generate_demo_valuation(struct_type, sqft, tier, completion)

    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)
    section_header("📊", "Financial Valuation Summary", "CPWD Rates · Indian Market Multipliers")

    m1, m2, m3 = st.columns(3)
    metric_card("Total Project Budget", val["total_budget"],
                f"{struct_type} · {sqft:,} sq.ft.", m1)
    metric_card("Capital Expenditure Incurred", val["capex_incurred"],
                f"{completion}% completion stage", m2)
    metric_card("Current Market Asset Value", val["market_value"],
                f"{tier} market premium applied", m3)

    s1, s2, s3 = st.columns(3)
    metric_card("Steel Requirement", val["steel_kg"],
                "@ 4.5 kg per sq.ft. norm", s1)
    metric_card("Cement Requirement", val["cement_bags"],
                "@ 0.22 bags per sq.ft. norm", s2)

    # ROI indicator
    if val["raw_market"] > 0 and val["raw_budget"] > 0:
        roi = ((val["raw_market"] - val["raw_budget"]) / val["raw_budget"]) * 100
        roi_color = "#22C55E" if roi > 0 else "#EF4444"
        s3.markdown(f"""
        <div class="card">
            <div class="card-title">Estimated ROI</div>
            <div class="card-value" style="color:{roi_color};">{roi:+.1f}%</div>
            <div class="card-sub">Market vs. Cost at {completion}% stage</div>
        </div>""", unsafe_allow_html=True)

    # 3D Rendering
    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)
    section_header("🎨", "Conceptual 3D Architectural Render", "Pollinations AI · Prompt-Based Generation")

    render_col, prompt_col = st.columns([1, 1], gap="large")
    with prompt_col:
        user_additions = st.text_area(
            "Additional Design Notes (optional)",
            placeholder="e.g. Modern minimalist with glass facade, rooftop garden, underground parking...",
            height=100, key="render_notes",
        )
        render_btn = st.button("🎨 Generate 3D Concept Render", use_container_width=True, key="gen_render")

    with render_col:
        if render_btn or st.session_state.get("render_img_url"):
            if render_btn:
                prompt_text = (
                    f"photorealistic 3D architectural rendering of a {struct_type} in India, "
                    f"{sqft:,} sq ft, {tier.split('(')[0].strip()} city location, "
                    f"modern Indian architecture style, daytime, blue sky, professional visualization, "
                    f"construction {completion}% complete. {user_additions}"
                ).replace(" ", "%20")

                pollinations_url = f"https://image.pollinations.ai/prompt/{prompt_text}?width=800&height=500&nologo=true&model=flux"
                st.session_state["render_img_url"] = pollinations_url

            url = st.session_state.get("render_img_url")
            if url:
                try:
                    with st.spinner("🎨 Generating architectural render..."):
                        resp = requests.get(url, timeout=45)
                        if resp.status_code == 200:
                            render_img = Image.open(io.BytesIO(resp.content))
                            st.image(render_img, caption=f"🏗️ Conceptual render — {struct_type}",
                                     use_container_width=True)
                        else:
                            st.warning("Render generation timed out. Try again.")
                except Exception:
                    st.markdown("""
                    <div class="render-placeholder">
                        <div style="font-size:2rem;margin-bottom:0.75rem;">🎨</div>
                        <div style="font-size:0.9rem;">3D render generation requires internet connection to Pollinations AI</div>
                    </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="render-placeholder">
                <div style="font-size:2.5rem;margin-bottom:0.75rem;">🏗️</div>
                <div style="font-size:0.95rem;font-weight:600;color:#F0F2F5;margin-bottom:0.5rem;">3D Concept Render</div>
                <div style="font-size:0.82rem;">Click "Generate" to create a photorealistic architectural visualization</div>
                <div style="font-size:0.78rem;margin-top:0.75rem;color:#5A6370;">Powered by Pollinations AI · Flux Model</div>
            </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TAB 4 — DAILY SITE ASSISTANT
# ─────────────────────────────────────────────
def tab_assistant():
    if is_demo_mode():
        render_demo_notice()

    section_header("🤖", "Daily Site Assistant & Weather-Aware Advisory",
                   "Real-Time Safety Alerts · AI Construction Engineering Chatbot")

    # Weather Advisory
    st.markdown("### 🌤️ Weather Condition Advisory")
    weather = st.selectbox(
        "Current Site Weather Condition",
        list(WEATHER_ADVISORIES.keys()),
        key="weather_select",
    )

    advisory = WEATHER_ADVISORIES[weather]
    level = advisory["level"]
    icon = advisory["icon"]
    level_colors = {
        "extreme": ("#DC2626", "rgba(220,38,38,0.12)", "rgba(220,38,38,0.3)"),
        "warning": ("#F59E0B", "rgba(245,158,11,0.10)", "rgba(245,158,11,0.3)"),
        "normal":  ("#22C55E", "rgba(34,197,94,0.08)",  "rgba(34,197,94,0.25)"),
    }
    txt_c, bg_c, brd_c = level_colors.get(level, level_colors["normal"])

    st.markdown(f"""
    <div style="background:{bg_c};border:1px solid {brd_c};border-radius:12px;padding:1.25rem 1.5rem;margin-bottom:1.25rem;">
        <div style="font-size:1.15rem;font-weight:800;color:{txt_c};margin-bottom:0.5rem;">
            {icon} {weather} — Site Advisory Active
        </div>
        <div style="font-size:0.82rem;color:#8892A0;">{len(advisory['alerts'])} safety protocols triggered for this condition</div>
    </div>
    """, unsafe_allow_html=True)

    sev_style_map = {"safe": ("#22C55E","rgba(34,197,94,0.1)"), "warning": ("#F59E0B","rgba(245,158,11,0.1)"),
                     "danger": ("#EF4444","rgba(239,68,68,0.1)"), "extreme": ("#DC2626","rgba(220,38,38,0.12)"),
                     "info": ("#3B82F6","rgba(59,130,246,0.1)")}

    alert_col1, alert_col2 = st.columns(2)
    for i, (title, sev, body) in enumerate(advisory["alerts"]):
        c_text, c_bg = sev_style_map.get(sev, ("#8892A0","rgba(255,255,255,0.05)"))
        target_col = alert_col1 if i % 2 == 0 else alert_col2
        target_col.markdown(f"""
        <div style="background:{c_bg};border:1px solid {c_text}30;border-left:4px solid {c_text};border-radius:10px;padding:1rem 1.25rem;margin-bottom:0.75rem;">
            <div style="font-weight:700;font-size:0.9rem;color:{c_text};margin-bottom:0.4rem;">{title}</div>
            <div style="font-size:0.82rem;color:#8892A0;line-height:1.55;">{body}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)

    # Chatbot
    section_header("💬", "ConstructAI Engineering Assistant",
                   "Multi-turn · IS Standards · OSHA Expert · Real-time Q&A")

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = [
            {
                "role": "assistant",
                "content": (
                    "👋 Hello! I'm **ConstructAI**, your expert construction engineering assistant. "
                    "I specialize in:\n\n"
                    "• **IS Standards** (IS 456, IS 800, IS 875, IS 1343, NBC 2016)\n"
                    "• **OSHA Safety Regulations** (29 CFR 1926)\n"
                    "• **Structural Design** — RCC, Steel, Pre-stressed Concrete\n"
                    "• **Project Management** — RERA, CPWD Rate Analysis\n"
                    "• **Materials** — Cement, Steel, Aggregates, Mix Design\n\n"
                    "How can I assist your site today? 🏗️"
                ),
            }
        ]

    # Render chat history
    chat_html = ""
    for msg in st.session_state["chat_history"]:
        is_user = msg["role"] == "user"
        role_class = "user" if is_user else "bot"
        avatar_icon = "👷" if is_user else "🤖"
        content = msg["content"].replace("\n", "<br>")
        chat_html += f"""
        <div class="chat-msg {role_class}">
            <div class="chat-avatar {role_class}">{avatar_icon}</div>
            <div class="chat-bubble {role_class}">{content}</div>
        </div>"""

    st.markdown(f'<div class="chat-container" id="chat-box">{chat_html}</div>', unsafe_allow_html=True)

    # Quick prompts
    st.markdown("**💡 Quick Prompts:**")
    qp_cols = st.columns(3)
    quick_prompts = [
        "What is the minimum cover for RCC columns per IS 456?",
        "OSHA requirements for scaffolding over 10 feet?",
        "How to calculate cement-sand ratio for M20 concrete?",
        "Safety protocol for working at heights in monsoon?",
        "What is bar bending schedule for a footing?",
        "Concrete curing period as per IS 456:2000?",
    ]
    for i, qp in enumerate(quick_prompts[:3]):
        if qp_cols[i].button(f"💬 {qp[:30]}...", key=f"qp_{i}", use_container_width=True):
            st.session_state["pending_msg"] = qp

    # Chat input
    user_input = st.chat_input("Ask anything about construction, safety, IS standards, materials...")

    # Handle quick prompt or typed input
    msg_to_send = st.session_state.pop("pending_msg", None) or user_input

    if msg_to_send:
        st.session_state["chat_history"].append({"role": "user", "content": msg_to_send})
        with st.spinner("ConstructAI is thinking..."):
            model = get_model()
            reply = chat_with_assistant(msg_to_send, st.session_state["chat_history"], model)
        st.session_state["chat_history"].append({"role": "assistant", "content": reply})
        st.rerun()

    if st.button("🗑️ Clear Conversation", key="clear_chat"):
        st.session_state["chat_history"] = [st.session_state["chat_history"][0]]
        st.rerun()


# ─────────────────────────────────────────────
# MAIN APPLICATION
# ─────────────────────────────────────────────
def main():
    inject_css()

    # Initialize session state defaults
    for key in ["gemini_api_key", "ppe_result", "crack_result", "render_img_url"]:
        if key not in st.session_state:
            st.session_state[key] = "" if key == "gemini_api_key" else None

    render_sidebar()

    # Hero Banner
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-badge">🏗️ Skill Wallet · Capstone Project 1 · Epic 2, 3, 5</div>
        <h1>Multimodal Construction Intelligence Platform</h1>
        <p>AI-powered safety auditing, structural diagnostics, real estate valuation & site advisory — powered by Google Gemini</p>
    </div>
    """, unsafe_allow_html=True)

    # Top Stats Row (always visible)
    s1, s2, s3, s4 = st.columns(4)
    s1.markdown("""<div class="card" style="text-align:center;padding:1rem;">
        <div style="font-size:1.8rem;">🦺</div>
        <div style="font-size:0.78rem;color:#8892A0;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;margin-top:0.3rem;">PPE Audit</div>
        <div style="font-size:0.75rem;color:#FF6B00;">OSHA · IS 456</div>
    </div>""", unsafe_allow_html=True)
    s2.markdown("""<div class="card" style="text-align:center;padding:1rem;">
        <div style="font-size:1.8rem;">🔍</div>
        <div style="font-size:0.78rem;color:#8892A0;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;margin-top:0.3rem;">Crack Diagnostics</div>
        <div style="font-size:0.75rem;color:#3B82F6;">IS 456 · IS 13920</div>
    </div>""", unsafe_allow_html=True)
    s3.markdown("""<div class="card" style="text-align:center;padding:1rem;">
        <div style="font-size:1.8rem;">💰</div>
        <div style="font-size:0.78rem;color:#8892A0;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;margin-top:0.3rem;">Valuation Engine</div>
        <div style="font-size:0.75rem;color:#22C55E;">CPWD · Indian Market</div>
    </div>""", unsafe_allow_html=True)
    s4.markdown("""<div class="card" style="text-align:center;padding:1rem;">
        <div style="font-size:1.8rem;">🤖</div>
        <div style="font-size:0.78rem;color:#8892A0;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;margin-top:0.3rem;">Site Assistant</div>
        <div style="font-size:0.75rem;color:#F59E0B;">Gemini · Multi-turn</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # Main Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🦺 Site Safety & PPE Audit",
        "🔍 Crack Diagnostics",
        "💰 Planning & Valuation",
        "🤖 Daily Site Assistant",
    ])

    with tab1:
        tab_safety()
    with tab2:
        tab_crack()
    with tab3:
        tab_valuation()
    with tab4:
        tab_assistant()


if __name__ == "__main__":
    main()
