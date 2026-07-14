"""
Palo Alto Networks — Employee Engagement, Satisfaction & Burnout Dashboard
Himanshu Rai
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Palo Alto Networks — HR Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────────────────
# SVG ICON SYSTEM (replaces all emoji usage across the app)
# ─────────────────────────────────────────────────────────────────────────────
def icon(name, size=16, color="currentColor"):
    icons = {
        "dashboard": f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="9" rx="1"/><rect x="14" y="3" width="7" height="5" rx="1"/><rect x="14" y="12" width="7" height="9" rx="1"/><rect x="3" y="16" width="7" height="5" rx="1"/></svg>''',
        "filter": f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polygon points="4 4 20 4 14 12.5 14 19 10 21 10 12.5 4 4"/></svg>''',
        "info": f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><line x1="12" y1="11" x2="12" y2="16"/><line x1="12" y1="8" x2="12" y2="8"/></svg>''',
        "search": f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>''',
        "alert-triangle": f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M10.3 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.7 3.86a2 2 0 0 0-3.4 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12" y2="17"/></svg>''',
        "trend-up": f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 17 9 11 13 15 21 7"/><polyline points="14 7 21 7 21 14"/></svg>''',
        "target": f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/></svg>''',
        "heart-pulse": f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20.42 4.58a5.4 5.4 0 0 0-7.65 0L12 5.35l-.77-.77a5.4 5.4 0 0 0-7.65 7.65L12 20.5l8.42-8.27a5.4 5.4 0 0 0 0-7.65z"/><polyline points="7 12 9.5 12 11 9.5 13 15 14.5 12 17 12"/></svg>''',
        "flame": f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/></svg>''',
        "briefcase": f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>''',
        "compass": f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>''',
        "pin": f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-6.1-7-11a7 7 0 0 1 14 0c0 4.9-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>''',
        "construction": f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="14" width="20" height="6" rx="1"/><path d="M4 14V9l8-5 8 5v5"/><line x1="12" y1="4" x2="12" y2="14"/></svg>''',
        "chart-growth": f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="M7 14l4-4 3 3 5-6"/></svg>''',
        "folder": f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7z"/></svg>''',
    }
    return icons.get(name, "")


# ─────────────────────────────────────────────────────────────────────────────
# THEME
# One locked theme, sourced from config.toml + this dict. Earlier versions of
# this app had a second, independent theme switcher (Streamlit's own native
# "⋮ > Settings > Theme" menu) running alongside a custom in-app toggle — two
# systems that don't talk to each other, so changing either one repainted
# only half the app and produced unreadable combinations (e.g. dark cards
# with light native widgets underneath). Fixed by removing the in-app toggle
# and locking the native theme via config.toml (toolbarMode = "minimal" hides
# the native theme menu entirely). One theme, applied everywhere, means there
# is nothing left to disagree.
# ─────────────────────────────────────────────────────────────────────────────
T = {
    "app_bg":         "#0e1117",
    "card_bg":        "#1c2230",
    "card_border":    "#2c3547",
    "text_primary":   "#e8ecf1",
    "text_secondary": "#9aa5b5",
    "header_grad":    "linear-gradient(135deg, #05070a 0%, #161c27 100%)",
    "sidebar_grad":   "linear-gradient(180deg, #05070a 0%, #12161f 100%)",
    "plot_bg":        "#1c2230",
    "plot_font":      "#e8ecf1",
    "plot_grid":      "#2c3547",
    "alert_red_bg":   "#3a1f1f", "alert_red_text":   "#f5b7b1",
    "alert_amber_bg": "#3a331a", "alert_amber_text": "#f6e0a0",
    "alert_green_bg": "#173324", "alert_green_text": "#a9e6c4",
}

# accent colors used for tier/risk semantics — constant regardless of theme
C_HIGH = "#2ecc71"
C_MED  = "#f39c12"
C_LOW  = "#e74c3c"
C_BLUE = "#3498db"

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS
# Covers every native Streamlit widget the app actually uses (sliders,
# checkboxes/radio, multiselect tags, st.info/error/success, download button,
# dataframe, expander) so nothing is left unstyled and falling back to
# Streamlit's default light chrome.
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
    .stApp {{ background-color: {T['app_bg']}; }}

    section[data-testid="stSidebar"] {{ background: {T['sidebar_grad']}; }}
    section[data-testid="stSidebar"] * {{ color: #ecf0f1 !important; }}
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMultiSelect label,
    section[data-testid="stSidebar"] .stSlider label,
    section[data-testid="stSidebar"] .stRadio label {{ color: #bdc3c7 !important; font-size: 0.82rem; }}

    .stMarkdown, .stMarkdown p, h1, h2, h3, h4, h5, h6,
    div[data-testid="stMetricValue"], div[data-testid="stMetricLabel"],
    label, div[data-testid="stWidgetLabel"] p {{
        color: {T['text_primary']} !important;
    }}

    div[data-testid="metric-container"] {{
        background: {T['card_bg']};
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        border-left: 4px solid {C_BLUE};
        border-top: 1px solid {T['card_border']};
        border-right: 1px solid {T['card_border']};
        border-bottom: 1px solid {T['card_border']};
    }}

    .section-header {{
        font-size: 1.15rem;
        font-weight: 700;
        color: {T['text_primary']};
        border-bottom: 2px solid {C_BLUE};
        padding-bottom: 6px;
        margin-bottom: 16px;
        margin-top: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    .alert-red, .alert-amber, .alert-green {{
        border-radius: 6px;
        padding: 12px 16px;
        margin: 8px 0;
        font-size: 0.88rem;
        line-height: 1.6;
    }}
    .alert-red   {{ background: {T['alert_red_bg']};   border-left: 4px solid {C_LOW};  color: {T['alert_red_text']}; }}
    .alert-amber {{ background: {T['alert_amber_bg']}; border-left: 4px solid {C_MED};  color: {T['alert_amber_text']}; }}
    .alert-green {{ background: {T['alert_green_bg']}; border-left: 4px solid {C_HIGH}; color: {T['alert_green_text']}; }}

    button[data-baseweb="tab"] {{
        font-size: 0.92rem;
        font-weight: 600;
        color: {T['text_primary']} !important;
    }}

    /* Native widgets that otherwise fall back to Streamlit's default chrome */
    div[data-testid="stExpander"], div[data-testid="stDataFrame"] {{
        background: {T['card_bg']};
        border-radius: 8px;
        border: 1px solid {T['card_border']};
    }}
    div[data-testid="stAlert"] {{
        background: {T['card_bg']} !important;
        color: {T['text_primary']} !important;
        border: 1px solid {T['card_border']} !important;
    }}
    div[data-baseweb="tag"] {{
        background: {C_BLUE}33 !important;
        color: {T['text_primary']} !important;
    }}
    button[kind="secondary"], .stDownloadButton button {{
        background: {T['card_bg']} !important;
        color: {T['text_primary']} !important;
        border: 1px solid {T['card_border']} !important;
    }}
    ul[data-testid="stSelectboxVirtualDropdown"], div[data-baseweb="popover"] div[role="listbox"] {{
        background: {T['card_bg']} !important;
    }}

    footer {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)


def alert_box(kind, title, body):
    """One alert box helper — replaces six copies of duplicated raw HTML."""
    icon_map = {"red": "alert-triangle", "amber": "alert-triangle", "green": "trend-up"}
    ic = icon(icon_map.get(kind, "info"), 14)
    return f"<div class='alert-{kind}'><strong>{ic} {title}</strong> {body}</div>"


def themed_chart(fig, height=None):
    """Apply the locked theme's colors to a Plotly figure."""
    layout_kwargs = dict(
        paper_bgcolor=T["plot_bg"],
        plot_bgcolor=T["plot_bg"],
        font=dict(color=T["plot_font"]),
    )
    if height:
        layout_kwargs["height"] = height
    fig.update_layout(**layout_kwargs)
    fig.update_xaxes(gridcolor=T["plot_grid"], zerolinecolor=T["plot_grid"])
    fig.update_yaxes(gridcolor=T["plot_grid"], zerolinecolor=T["plot_grid"])
    return fig


def render_chart(fig, **kwargs):
    st.plotly_chart(themed_chart(fig), width="stretch", **kwargs)


# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING & FEATURE ENGINEERING  (cached)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("Palo_Alto_Networks.csv")

    df["OverTime_num"]       = (df["OverTime"] == "Yes").astype(int)
    df["Gender_num"]         = (df["Gender"] == "Male").astype(int)
    bt_map = {"Non-Travel": 0, "Travel_Rarely": 1, "Travel_Frequently": 2}
    df["BusinessTravel_num"] = df["BusinessTravel"].map(bt_map)

    ord_cols = ["JobSatisfaction", "EnvironmentSatisfaction",
                "RelationshipSatisfaction", "JobInvolvement", "WorkLifeBalance"]
    for c in ord_cols:
        df[c + "_norm"] = (df[c] - 1) / 3

    eng_cols = ["JobSatisfaction_norm", "EnvironmentSatisfaction_norm",
                "RelationshipSatisfaction_norm", "JobInvolvement_norm"]
    df["EngagementIndex"] = df[eng_cols].mean(axis=1)

    def eng_tier(x):
        if x >= 0.67: return "High"
        elif x >= 0.33: return "Medium"
        return "Low"
    df["EngagementTier"] = df["EngagementIndex"].apply(eng_tier)

    def burnout_score(row):
        s = 0
        if row["OverTime"] == "Yes": s += 2
        if row["WorkLifeBalance"] <= 2: s += 2
        if row["EngagementIndex"] < 0.33: s += 1
        if row["BusinessTravel"] == "Travel_Frequently": s += 1
        return s
    df["BurnoutScore"] = df.apply(burnout_score, axis=1)
    df["BurnoutRisk"]  = df["BurnoutScore"].apply(
        lambda s: "High" if s >= 4 else ("Medium" if s >= 2 else "Low"))

    df["SatStability"] = df[eng_cols].std(axis=1)

    def stab_tier(x):
        if x < 0.20: return "Stable"
        elif x < 0.35: return "Moderate"
        return "Unstable"
    df["StabilityTier"] = df["SatStability"].apply(stab_tier)

    df["WorkloadStress"] = (df["OverTime_num"] * 3
                            + df["BusinessTravel_num"]
                            + (df["DistanceFromHome"] > 15).astype(int))
    df["StressLevel"] = pd.cut(df["WorkloadStress"],
                               bins=[-1, 1, 3, 6],
                               labels=["Low", "Moderate", "High"])

    def tenure_band(y):
        if y <= 2:  return "New (0-2yr)"
        elif y <= 5: return "Early (3-5yr)"
        elif y <= 10: return "Mid (6-10yr)"
        return "Senior (10+yr)"
    df["TenureBand"] = df["YearsAtCompany"].apply(tenure_band)
    df["TenureOrder"] = df["YearsAtCompany"].apply(
        lambda y: 0 if y<=2 else (1 if y<=5 else (2 if y<=10 else 3)))

    def commute_band(d):
        if d <= 5: return "Near (≤5km)"
        elif d <= 15: return "Mid (6-15km)"
        return "Far (>15km)"
    df["CommuteBand"] = df["DistanceFromHome"].apply(commute_band)

    return df


df_raw = load_data()


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — GLOBAL FILTERS
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        f"<div style='display:flex;align-items:center;gap:9px;margin-top:6px;'>"
        f"{icon('filter', 20, '#ecf0f1')}<span style='font-size:1.05rem;font-weight:700;'>Global Filters</span></div>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    all_depts = sorted(df_raw["Department"].unique())
    sel_dept  = st.multiselect("Department", all_depts, default=all_depts, key="dept")

    all_roles = sorted(df_raw["JobRole"].unique())
    sel_roles = st.multiselect("Job Role", all_roles, default=all_roles, key="roles")

    # A single radio replaces three independent checkboxes that previously
    # allowed contradictory states (e.g. both "Overtime only" and "No
    # overtime" checked at once, which silently applied no filter at all).
    ot_filter = st.radio(
        "Overtime", ["All employees", "Overtime only", "No overtime"],
        index=0, key="ot_filter"
    )

    eng_threshold = st.slider(
        "Min Engagement Index", 0.0, 1.0, 0.0, 0.05,
        help="Filter to employees at or above this engagement level")

    tenure_min, tenure_max = st.slider(
        "Tenure at Company (years)", 0, 40, (0, 40), key="tenure")

    st.markdown("---")
    st.markdown(
        f"<div style='display:flex;align-items:center;gap:8px;font-weight:700;font-size:0.95rem;'>"
        f"{icon('folder', 16, '#ecf0f1')}Project Info</div>",
        unsafe_allow_html=True,
    )
    st.markdown("""
    <div style='font-size:0.78rem; color:#95a5a6; line-height:1.7'>
    Data Science Internship Project<br>
    Analyst: Himanshu Rai<br>
    Dataset: 1,470 employees<br>
    Tool: Python + Streamlit
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────────────────────────────────────────
df = df_raw.copy()

if sel_dept:
    df = df[df["Department"].isin(sel_dept)]
if sel_roles:
    df = df[df["JobRole"].isin(sel_roles)]

if ot_filter == "Overtime only":
    df = df[df["OverTime"] == "Yes"]
elif ot_filter == "No overtime":
    df = df[df["OverTime"] == "No"]

df = df[df["EngagementIndex"] >= eng_threshold]
df = df[(df["YearsAtCompany"] >= tenure_min) & (df["YearsAtCompany"] <= tenure_max)]

n = len(df)

if n == 0:
    st.error("No employees match the current filters. Please widen your selection.")
    st.stop()


# ─────────────────────────────────────────────────────────────────────────────
# HEADER BANNER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style='background: {T["header_grad"]};
            border-radius: 12px; padding: 28px 32px; margin-bottom: 20px;'>
    <h1 style='color:white; margin:0; font-size:1.7rem; display:flex; align-items:center; gap:12px;'>
        {icon('dashboard', 26, '#ffffff')} Employee Engagement, Satisfaction & Burnout
    </h1>
    <p style='color:#95a5a6; margin:6px 0 0 0; font-size:0.95rem;'>
        Palo Alto Networks — HR Analytics Dashboard
    </p>
</div>
""", unsafe_allow_html=True)

if n < len(df_raw):
    st.info(f"{icon('search', 15)} Showing **{n:,} of {len(df_raw):,} employees** after filters", icon=None)


# ─────────────────────────────────────────────────────────────────────────────
# TOP-LEVEL KPI ROW
# ─────────────────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)

avg_ei        = df["EngagementIndex"].mean()
attrition_pct = df["Attrition"].mean() * 100
high_burnout  = (df["BurnoutRisk"] == "High").sum()
high_stress   = (df["StressLevel"] == "High").sum()
ot_pct        = df["OverTime_num"].mean() * 100

k1.metric("Avg Engagement Index", f"{avg_ei:.3f}", f"{avg_ei*100:.1f}% of max")
k2.metric("Overall Attrition Rate", f"{attrition_pct:.1f}%", f"{df['Attrition'].sum()} employees left")
k3.metric("High Burnout Risk", f"{high_burnout:,}", f"{high_burnout/n*100:.1f}% of filtered")
k4.metric("High Workload Stress", f"{high_stress:,}", f"{high_stress/n*100:.1f}% of filtered")
k5.metric("Working Overtime", f"{ot_pct:.1f}%", f"{df['OverTime_num'].sum()} employees")

st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# FOUR MODULE TABS
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "Engagement Health", "Burnout Risk", "Role & Career Stage", "Manager Action Panel"
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — ENGAGEMENT HEALTH OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown(f'<div class="section-header">{icon("heart-pulse", 18, C_BLUE)}Organisation-Wide Engagement Health</div>',
                unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1.2, 1.5, 1.5])

    with c1:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=avg_ei * 100,
            delta={"reference": 57.4, "valueformat": ".1f", "prefix": "vs full dataset: "},
            title={"text": "Engagement Index<br><span style='font-size:0.8em;'>% of maximum</span>"},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1},
                "bar":  {"color": C_BLUE, "thickness": 0.3},
                "steps": [
                    {"range": [0, 33],  "color": T["alert_red_bg"]},
                    {"range": [33, 67], "color": T["alert_amber_bg"]},
                    {"range": [67, 100],"color": T["alert_green_bg"]},
                ],
                "threshold": {"line": {"color": T["text_primary"], "width": 3}, "thickness": 0.8, "value": 57.4}
            }
        ))
        fig_gauge.update_layout(margin=dict(t=60, b=10, l=10, r=10))
        render_chart(fig_gauge, key="gauge")

    with c2:
        tier_counts = df["EngagementTier"].value_counts().reindex(["High", "Medium", "Low"]).fillna(0)
        fig_donut = px.pie(
            values=tier_counts.values, names=tier_counts.index, hole=0.55,
            color=tier_counts.index,
            color_discrete_map={"High": C_HIGH, "Medium": C_MED, "Low": C_LOW},
            title="Engagement Tier Distribution"
        )
        fig_donut.update_traces(textposition="outside", textinfo="percent+label")
        fig_donut.update_layout(
            margin=dict(t=50, b=10, l=10, r=10), showlegend=False,
            annotations=[dict(text=f"n={n:,}", x=0.5, y=0.5, font_size=14, showarrow=False, font_color=T["plot_font"])]
        )
        render_chart(fig_donut, key="donut")

    with c3:
        tier_attr = df.groupby("EngagementTier")["Attrition"].mean() * 100
        tier_attr = tier_attr.reindex(["High", "Medium", "Low"]).fillna(0)
        fig_tier_attr = go.Figure(go.Bar(
            x=tier_attr.index, y=tier_attr.values, marker_color=[C_HIGH, C_MED, C_LOW],
            text=[f"{v:.1f}%" for v in tier_attr.values], textposition="outside"
        ))
        overall_attr = df["Attrition"].mean() * 100
        fig_tier_attr.add_hline(y=overall_attr, line_dash="dash", line_color=T["text_secondary"],
                                annotation_text=f"Avg {overall_attr:.1f}%", annotation_position="top right")
        fig_tier_attr.update_layout(
            title="Attrition Rate by Engagement Tier", yaxis_title="Attrition Rate (%)",
            margin=dict(t=50, b=10, l=10, r=10),
            yaxis=dict(range=[0, max(tier_attr.values)*1.3 + 5])
        )
        render_chart(fig_tier_attr, key="tier_attr")

    st.markdown("---")
    st.markdown('<div class="section-header">Satisfaction Dimension Breakdown</div>', unsafe_allow_html=True)

    c4, c5 = st.columns(2)

    with c4:
        dims = ["Job Sat.", "Env. Sat.", "Rel. Sat.", "Job Inv.", "WLB"]
        cols = ["JobSatisfaction_norm", "EnvironmentSatisfaction_norm",
                "RelationshipSatisfaction_norm", "JobInvolvement_norm", "WorkLifeBalance_norm"]
        stayed_means = df[df["Attrition"] == 0][cols].mean().values * 100
        left_means   = df[df["Attrition"] == 1][cols].mean().values * 100

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=list(stayed_means) + [stayed_means[0]], theta=dims + [dims[0]],
            fill="toself", name="Stayed", line_color=C_BLUE, fillcolor="rgba(52,152,219,0.15)"
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=list(left_means) + [left_means[0]], theta=dims + [dims[0]],
            fill="toself", name="Left", line_color=C_LOW, fillcolor="rgba(231,76,60,0.15)"
        ))
        fig_radar.update_layout(
            polar=dict(bgcolor=T["plot_bg"],
                       radialaxis=dict(range=[0, 100], ticksuffix="%", gridcolor=T["plot_grid"]),
                       angularaxis=dict(gridcolor=T["plot_grid"])),
            title="Satisfaction Profile: Stayed vs Left",
            margin=dict(t=60, b=20, l=40, r=40), legend=dict(orientation="h", y=-0.1)
        )
        render_chart(fig_radar, key="radar")

    with c5:
        ei_stayed = df[df["Attrition"] == 0]["EngagementIndex"]
        ei_left   = df[df["Attrition"] == 1]["EngagementIndex"]

        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(x=ei_stayed, nbinsx=20, name=f"Stayed (n={len(ei_stayed):,})",
                                        marker_color=C_BLUE, opacity=0.65))
        fig_hist.add_trace(go.Histogram(x=ei_left, nbinsx=20, name=f"Left (n={len(ei_left):,})",
                                        marker_color=C_LOW, opacity=0.65))
        fig_hist.add_vline(x=ei_stayed.mean(), line_dash="dash", line_color=C_BLUE,
                           annotation_text=f"Stayed avg: {ei_stayed.mean():.3f}", annotation_position="top right")
        fig_hist.add_vline(x=ei_left.mean(), line_dash="dash", line_color=C_LOW,
                           annotation_text=f"Left avg: {ei_left.mean():.3f}", annotation_position="top left")
        fig_hist.update_layout(
            barmode="overlay", title="Engagement Score Distribution (Stayed vs Left)",
            xaxis_title="Engagement Index (0–1)", yaxis_title="Number of Employees",
            margin=dict(t=60, b=20, l=40, r=20), legend=dict(orientation="h", y=-0.15)
        )
        render_chart(fig_hist, height=320, key="hist_ei")

    st.markdown("---")
    st.markdown('<div class="section-header">Engagement by Department</div>', unsafe_allow_html=True)

    dept_stats = df.groupby("Department").agg(
        Employees=("EngagementIndex", "count"),
        AvgEI=("EngagementIndex", "mean"),
        Attrition=("Attrition", "mean")
    ).reset_index()
    dept_stats["AttritionPct"] = dept_stats["Attrition"] * 100
    dept_stats = dept_stats.sort_values("AvgEI")

    c6, c7 = st.columns(2)
    with c6:
        fig_dept = px.bar(
            dept_stats, x="AvgEI", y="Department", orientation="h", text="AvgEI",
            color="AvgEI", color_continuous_scale=["#e74c3c", "#f39c12", "#2ecc71"],
            range_color=[0.5, 0.65], title="Mean Engagement Index by Department"
        )
        fig_dept.update_traces(texttemplate="%{text:.3f}", textposition="outside")
        fig_dept.update_layout(margin=dict(t=50, b=20, l=10, r=40), coloraxis_showscale=False,
                               xaxis=dict(range=[0.5, 0.65]))
        render_chart(fig_dept, height=250, key="dept_ei")

    with c7:
        fig_dept_attr = px.bar(
            dept_stats, x="AttritionPct", y="Department", orientation="h", text="AttritionPct",
            color="AttritionPct", color_continuous_scale=["#2ecc71", "#f39c12", "#e74c3c"],
            title="Attrition Rate by Department (%)"
        )
        fig_dept_attr.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_dept_attr.update_layout(margin=dict(t=50, b=20, l=10, r=40), coloraxis_showscale=False)
        render_chart(fig_dept_attr, height=250, key="dept_attr")

    lowest_dept = dept_stats.loc[dept_stats["AvgEI"].idxmin(), "Department"]
    lowest_ei   = dept_stats["AvgEI"].min()
    st.markdown(
        alert_box("amber", "Department to watch:",
                  f"{lowest_dept} has the lowest average engagement index ({lowest_ei:.3f}) of any department."),
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — BURNOUT RISK DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown(f'<div class="section-header">{icon("flame", 18, C_LOW)}Burnout Risk Overview</div>',
                unsafe_allow_html=True)

    b1, b2, b3 = st.columns(3)
    high_b = df[df["BurnoutRisk"] == "High"]
    med_b  = df[df["BurnoutRisk"] == "Medium"]
    low_b  = df[df["BurnoutRisk"] == "Low"]

    b1.metric("High Burnout Risk", f"{len(high_b):,} employees",
              f"{len(high_b)/n*100:.1f}%  |  Attrition: {high_b['Attrition'].mean()*100:.1f}%")
    b2.metric("Medium Burnout Risk", f"{len(med_b):,} employees",
              f"{len(med_b)/n*100:.1f}%  |  Attrition: {med_b['Attrition'].mean()*100:.1f}%")
    b3.metric("Low Burnout Risk", f"{len(low_b):,} employees",
              f"{len(low_b)/n*100:.1f}%  |  Attrition: {low_b['Attrition'].mean()*100:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        burn_attr = pd.DataFrame({
            "Risk Tier": ["Low", "Medium", "High"],
            "Attrition %": [
                low_b["Attrition"].mean() * 100 if len(low_b) > 0 else 0,
                med_b["Attrition"].mean() * 100 if len(med_b) > 0 else 0,
                high_b["Attrition"].mean() * 100 if len(high_b) > 0 else 0
            ]
        })
        fig_burn_attr = px.bar(
            burn_attr, x="Risk Tier", y="Attrition %", color="Risk Tier",
            color_discrete_map={"Low": C_HIGH, "Medium": C_MED, "High": C_LOW},
            text="Attrition %", title="Attrition Rate by Burnout Risk Tier"
        )
        fig_burn_attr.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_burn_attr.add_hline(y=df["Attrition"].mean() * 100, line_dash="dash", line_color=T["text_secondary"],
                                annotation_text=f"Overall: {df['Attrition'].mean()*100:.1f}%")
        fig_burn_attr.update_layout(showlegend=False, margin=dict(t=50, b=20, l=10, r=10),
                                    yaxis=dict(range=[0, max(burn_attr["Attrition %"]) * 1.3 + 5]))
        render_chart(fig_burn_attr, height=320, key="burn_attr")

    with c2:
        # Rewritten from groupby().apply(..., include_groups=False), which only
        # exists on pandas >=2.2 and crashes on older installs. This version
        # is plain .agg() and works on any pandas version.
        role_burn = (
            df.assign(_is_high=(df["BurnoutRisk"] == "High").astype(int))
            .groupby("JobRole")
            .agg(**{"High Risk %": ("_is_high", "mean"), "n": ("_is_high", "count")})
            .reset_index()
        )
        role_burn["High Risk %"] *= 100
        role_burn = role_burn.sort_values("High Risk %", ascending=True)

        fig_role_burn = px.bar(
            role_burn, x="High Risk %", y="JobRole", orientation="h", text="High Risk %",
            color="High Risk %", color_continuous_scale=["#2ecc71", "#f39c12", "#e74c3c"],
            title="High Burnout Risk % by Job Role"
        )
        fig_role_burn.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        avg_br = (df["BurnoutRisk"] == "High").mean() * 100
        fig_role_burn.add_vline(x=avg_br, line_dash="dash", line_color=T["text_secondary"],
                                annotation_text=f"Avg {avg_br:.1f}%")
        fig_role_burn.update_layout(coloraxis_showscale=False, margin=dict(t=50, b=20, l=10, r=60))
        render_chart(fig_role_burn, height=320, key="role_burn")

    st.markdown("---")
    st.markdown('<div class="section-header">Overtime & Work-Life Balance Analysis</div>', unsafe_allow_html=True)

    c3, c4, c5 = st.columns(3)

    with c3:
        ot_data = df.groupby("OverTime").agg(
            AttritionPct=("Attrition", lambda x: x.mean() * 100),
            AvgEI=("EngagementIndex", "mean"),
            Count=("Attrition", "count")
        ).reset_index()

        fig_ot = px.bar(
            ot_data, x="OverTime", y="AttritionPct", color="OverTime",
            color_discrete_map={"No": C_HIGH, "Yes": C_LOW}, text="AttritionPct",
            title="Attrition Rate: Overtime vs No Overtime"
        )
        fig_ot.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_ot.update_layout(showlegend=False, yaxis_title="Attrition Rate (%)", margin=dict(t=50, b=20, l=10, r=10))
        render_chart(fig_ot, height=300, key="ot_attr")

    with c4:
        wlb_labels = {1: "1-Bad", 2: "2-Good", 3: "3-Better", 4: "4-Best"}
        wlb_data = df.groupby("WorkLifeBalance").agg(
            AttritionPct=("Attrition", lambda x: x.mean() * 100),
            Count=("Attrition", "count")
        ).reset_index()
        wlb_data["Label"] = wlb_data["WorkLifeBalance"].map(wlb_labels)

        fig_wlb = px.bar(
            wlb_data, x="Label", y="AttritionPct", color="AttritionPct",
            color_continuous_scale=["#2ecc71", "#f39c12", "#e74c3c"], text="AttritionPct",
            title="Attrition Rate by Work-Life Balance Score"
        )
        fig_wlb.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_wlb.update_layout(coloraxis_showscale=False, yaxis_title="Attrition Rate (%)",
                              margin=dict(t=50, b=20, l=10, r=10))
        render_chart(fig_wlb, height=300, key="wlb_attr")

    with c5:
        travel_ot = df.groupby(["BusinessTravel", "OverTime"])["Attrition"].mean() * 100
        travel_ot = travel_ot.reset_index()
        travel_ot.columns = ["Travel", "OT", "Attrition%"]
        travel_order = ["Non-Travel", "Travel_Rarely", "Travel_Frequently"]
        travel_ot["Travel"] = pd.Categorical(travel_ot["Travel"], categories=travel_order, ordered=True)
        travel_ot = travel_ot.sort_values("Travel")

        pivot = travel_ot.pivot(index="Travel", columns="OT", values="Attrition%")
        fig_hmap = go.Figure(go.Heatmap(
            z=pivot.values, x=["No Overtime", "Overtime"],
            y=["Non-Travel", "Rarely Travels", "Freq. Travel"],
            colorscale="RdYlGn_r",
            text=[[f"{v:.1f}%" for v in row] for row in pivot.values],
            texttemplate="%{text}", textfont={"size": 14, "color": "white"},
            zmin=0, zmax=45, showscale=True
        ))
        fig_hmap.update_layout(title="Attrition: Travel × Overtime (%)", margin=dict(t=50, b=20, l=10, r=10))
        render_chart(fig_hmap, height=300, key="hmap")

    st.markdown("---")
    st.markdown('<div class="section-header">Workload Stress Indicator (KPI 5)</div>', unsafe_allow_html=True)

    c6, c7 = st.columns(2)

    with c6:
        stress_data = df.groupby("WorkloadStress").agg(
            Count=("EngagementIndex", "count"),
            AttritionPct=("Attrition", lambda x: x.mean() * 100),
            AvgEI=("EngagementIndex", "mean")
        ).reset_index()

        fig_stress = make_subplots(specs=[[{"secondary_y": True}]])
        fig_stress.add_trace(
            go.Bar(x=stress_data["WorkloadStress"], y=stress_data["AttritionPct"],
                   name="Attrition %", marker_color=C_LOW, opacity=0.8,
                   text=[f"{v:.1f}%" for v in stress_data["AttritionPct"]], textposition="outside"),
            secondary_y=False
        )
        fig_stress.add_trace(
            go.Scatter(x=stress_data["WorkloadStress"], y=stress_data["AvgEI"],
                       name="Avg Engagement", mode="lines+markers",
                       line=dict(color=C_BLUE, width=2.5), marker=dict(size=8)),
            secondary_y=True
        )
        fig_stress.update_layout(
            title="Attrition & Engagement vs Workload Stress",
            xaxis_title="Workload Stress Score (0–6)",
            margin=dict(t=60, b=20, l=10, r=10), legend=dict(orientation="h", y=-0.15)
        )
        fig_stress.update_yaxes(title_text="Attrition Rate (%)", secondary_y=False, color=C_LOW)
        fig_stress.update_yaxes(title_text="Avg Engagement Index", secondary_y=True, color=C_BLUE)
        render_chart(fig_stress, height=320, key="stress_paradox")

    with c7:
        level_data = df.groupby("StressLevel", observed=True).agg(
            Count=("EngagementIndex", "count"),
            AttritionPct=("Attrition", lambda x: x.mean() * 100),
            AvgEI=("EngagementIndex", "mean")
        ).reset_index()

        fig_levels = px.bar(
            level_data, x="StressLevel", y="AttritionPct", color="StressLevel",
            color_discrete_map={"Low": C_HIGH, "Moderate": C_MED, "High": C_LOW},
            text="AttritionPct", title="Attrition by Stress Level Bucket"
        )
        fig_levels.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_levels.update_layout(showlegend=False, yaxis_title="Attrition Rate (%)",
                                 margin=dict(t=60, b=20, l=10, r=10))
        render_chart(fig_levels, height=320, key="stress_level")

    danger = df[(df["BurnoutRisk"] == "High") & (df["EngagementTier"] == "Low")]
    if len(danger) > 0:
        d_left = danger["Attrition"].sum()
        d_rate = danger["Attrition"].mean() * 100
        st.markdown(
            alert_box("red", "High-risk overlap:",
                f"{len(danger)} employees show both high burnout risk and low engagement. "
                f"{d_left} of them ({d_rate:.1f}%) have already left — the highest attrition "
                f"rate of any segment here."),
            unsafe_allow_html=True,
        )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — ROLE & CAREER STAGE ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown(f'<div class="section-header">{icon("briefcase", 18, C_BLUE)}Engagement by Job Role and Level</div>',
                unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        role_data = df.groupby("JobRole").agg(
            AvgEI=("EngagementIndex", "mean"),
            AttritionPct=("Attrition", lambda x: x.mean() * 100),
            Count=("EngagementIndex", "count")
        ).reset_index().sort_values("AvgEI", ascending=True)

        fig_role_ei = px.bar(
            role_data, x="AvgEI", y="JobRole", orientation="h", text="AvgEI",
            color="AvgEI", color_continuous_scale=["#e74c3c", "#f39c12", "#2ecc71"],
            range_color=[0.52, 0.62], title="Mean Engagement Index by Job Role"
        )
        fig_role_ei.update_traces(texttemplate="%{text:.3f}", textposition="outside")
        fig_role_ei.update_layout(coloraxis_showscale=False, margin=dict(t=50, b=20, l=10, r=60))
        render_chart(fig_role_ei, height=340, key="role_ei")

    with c2:
        level_ei = df.groupby("JobLevel").agg(
            AvgEI=("EngagementIndex", "mean"),
            AttritionPct=("Attrition", lambda x: x.mean() * 100),
            Count=("EngagementIndex", "count")
        ).reset_index()
        level_ei["LevelLabel"] = level_ei["JobLevel"].map(
            {1: "L1 Entry", 2: "L2 Junior", 3: "L3 Mid", 4: "L4 Senior", 5: "L5 Executive"})

        fig_jl = make_subplots(specs=[[{"secondary_y": True}]])
        fig_jl.add_trace(
            go.Bar(x=level_ei["LevelLabel"], y=level_ei["AvgEI"], name="Avg Engagement",
                   marker_color=C_BLUE, opacity=0.8,
                   text=[f"{v:.3f}" for v in level_ei["AvgEI"]], textposition="outside"),
            secondary_y=False
        )
        fig_jl.add_trace(
            go.Scatter(x=level_ei["LevelLabel"], y=level_ei["AttritionPct"], name="Attrition %",
                       mode="lines+markers", line=dict(color=C_LOW, width=2.5), marker=dict(size=8)),
            secondary_y=True
        )
        fig_jl.update_layout(title="Engagement & Attrition by Job Level",
                             margin=dict(t=50, b=20, l=10, r=10), legend=dict(orientation="h", y=-0.15))
        fig_jl.update_yaxes(title_text="Avg Engagement Index", secondary_y=False, color=C_BLUE)
        fig_jl.update_yaxes(title_text="Attrition Rate (%)", secondary_y=True, color=C_LOW)
        render_chart(fig_jl, height=340, key="job_level")

    st.markdown("---")
    st.markdown('<div class="section-header">Tenure vs Engagement Trends</div>', unsafe_allow_html=True)

    c3, c4 = st.columns(2)

    with c3:
        tenure_order = ["New (0-2yr)", "Early (3-5yr)", "Mid (6-10yr)", "Senior (10+yr)"]
        tenure_data  = df.groupby("TenureBand").agg(
            AttritionPct=("Attrition", lambda x: x.mean() * 100),
            AvgEI=("EngagementIndex", "mean"),
            Count=("EngagementIndex", "count")
        ).reindex(tenure_order).reset_index()

        fig_tenure = px.bar(
            tenure_data, x="TenureBand", y="AttritionPct", color="AttritionPct",
            color_continuous_scale=["#2ecc71", "#f39c12", "#e74c3c"], text="AttritionPct",
            title="Attrition Rate by Tenure Band"
        )
        fig_tenure.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_tenure.add_hline(y=df["Attrition"].mean() * 100, line_dash="dash", line_color=T["text_secondary"],
                             annotation_text="Overall avg")
        fig_tenure.update_layout(coloraxis_showscale=False, xaxis_title="Tenure Band",
                                 yaxis_title="Attrition Rate (%)", margin=dict(t=50, b=20, l=10, r=10))
        render_chart(fig_tenure, height=300, key="tenure_attr")

    with c4:
        df_sample = df.sample(min(500, n), random_state=42)
        fig_scatter = px.scatter(
            df_sample, x="YearsAtCompany", y="EngagementIndex", color="EngagementTier",
            color_discrete_map={"High": C_HIGH, "Medium": C_MED, "Low": C_LOW},
            opacity=0.6, size_max=8, trendline="lowess",
            title="Engagement Journey: Tenure vs Engagement Index"
        )
        fig_scatter.update_layout(margin=dict(t=50, b=20, l=10, r=10), xaxis_title="Years at Company",
                                  yaxis_title="Engagement Index", legend=dict(orientation="h", y=-0.2))
        render_chart(fig_scatter, height=300, key="scatter")

    st.markdown("---")
    st.markdown('<div class="section-header">Promotion Stagnation Analysis</div>', unsafe_allow_html=True)

    c5, c6 = st.columns(2)

    with c5:
        promo_labels = ["Just Promoted\n(0yr)", "1–2 Years\nAgo", "3–5 Years\nAgo", "6+ Years\n(Stagnant)"]
        promo_data = []
        ranges = [(0,0), (1,2), (3,5), (6,15)]
        for (lo, hi), label in zip(ranges, promo_labels):
            g = df[(df["YearsSinceLastPromotion"] >= lo) & (df["YearsSinceLastPromotion"] <= hi)]
            if len(g) > 0:
                promo_data.append({
                    "Group": label, "AttritionPct": g["Attrition"].mean() * 100,
                    "AvgEI": g["EngagementIndex"].mean(), "Count": len(g)
                })
        promo_df = pd.DataFrame(promo_data)

        fig_promo = go.Figure()
        colors_promo = [C_MED, C_HIGH, C_HIGH, C_LOW]
        fig_promo.add_trace(go.Bar(
            x=promo_df["Group"], y=promo_df["AttritionPct"], marker_color=colors_promo[:len(promo_df)],
            text=[f"{v:.1f}%" for v in promo_df["AttritionPct"]], textposition="outside", name="Attrition %"
        ))
        fig_promo.update_layout(title="Attrition by Promotion Recency", yaxis_title="Attrition Rate (%)",
                                margin=dict(t=50, b=20, l=10, r=10), showlegend=False)
        render_chart(fig_promo, height=300, key="promo")

    with c6:
        df["RoleYrsBin"] = pd.cut(df["YearsInCurrentRole"], bins=[-1, 2, 5, 10, 18],
                                  labels=["0–2yr", "3–5yr", "6–10yr", "11+yr"])
        role_yr_data = df.groupby("RoleYrsBin", observed=True).agg(
            AvgEI=("EngagementIndex", "mean"),
            AttritionPct=("Attrition", lambda x: x.mean() * 100),
            Count=("EngagementIndex", "count")
        ).reset_index()

        fig_roleyrs = make_subplots(specs=[[{"secondary_y": True}]])
        fig_roleyrs.add_trace(
            go.Bar(x=role_yr_data["RoleYrsBin"].astype(str), y=role_yr_data["AvgEI"],
                   name="Avg Engagement", marker_color=C_BLUE, opacity=0.8),
            secondary_y=False
        )
        fig_roleyrs.add_trace(
            go.Scatter(x=role_yr_data["RoleYrsBin"].astype(str), y=role_yr_data["AttritionPct"],
                       name="Attrition %", mode="lines+markers", line=dict(color=C_LOW, width=2.5),
                       marker=dict(size=9)),
            secondary_y=True
        )
        fig_roleyrs.update_layout(title="Engagement & Attrition by Years in Current Role",
                                  margin=dict(t=50, b=20, l=10, r=10), legend=dict(orientation="h", y=-0.2))
        fig_roleyrs.update_yaxes(title_text="Avg Engagement", secondary_y=False, color=C_BLUE)
        fig_roleyrs.update_yaxes(title_text="Attrition %", secondary_y=True, color=C_LOW)
        render_chart(fig_roleyrs, height=300, key="role_yrs")

    new_emp  = df[df["TenureBand"] == "New (0-2yr)"]
    sen_emp  = df[df["TenureBand"] == "Senior (10+yr)"]
    new_attr = new_emp["Attrition"].mean() * 100 if len(new_emp) > 0 else 0
    sen_attr = sen_emp["Attrition"].mean() * 100 if len(sen_emp) > 0 else 0
    ratio    = new_attr / sen_attr if sen_attr > 0 else 0

    st.markdown(
        alert_box("red", "New-hire attrition:",
            f"Employees with 0–2 years tenure leave at {new_attr:.1f}% — {ratio:.1f}× the rate of "
            f"employees with 10+ years ({sen_attr:.1f}%). Structured onboarding and 30/60/90-day "
            f"check-ins are the standard fix for this pattern."),
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — MANAGER ACTION PANEL
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown(f'<div class="section-header">{icon("target", 18, C_LOW)}Priority Intervention Areas</div>',
                unsafe_allow_html=True)

    segments = []

    dz = df[(df["BurnoutRisk"] == "High") & (df["EngagementTier"] == "Low")]
    if len(dz) > 0:
        segments.append({
            "Priority": "CRITICAL", "Segment": "High Burnout + Low Engagement (Danger Zone)",
            "Employees": len(dz), "Attrition %": f"{dz['Attrition'].mean()*100:.1f}%",
            "Action": "Immediate 1:1 HR outreach and workload assessment"
        })

    hb = df[df["BurnoutRisk"] == "High"]
    if len(hb) > 0:
        segments.append({
            "Priority": "HIGH", "Segment": "High Burnout Risk",
            "Employees": len(hb), "Attrition %": f"{hb['Attrition'].mean()*100:.1f}%",
            "Action": "Overtime audit; workload redistribution plan"
        })

    ot_emp = df[df["OverTime"] == "Yes"]
    if len(ot_emp) > 0:
        segments.append({
            "Priority": "HIGH", "Segment": "Overtime Employees",
            "Employees": len(ot_emp), "Attrition %": f"{ot_emp['Attrition'].mean()*100:.1f}%",
            "Action": "Workload redistribution, not motivation programmes"
        })

    ftot = df[(df["BusinessTravel"] == "Travel_Frequently") & (df["OverTime"] == "Yes")]
    if len(ftot) > 0:
        segments.append({
            "Priority": "HIGH", "Segment": "Frequent Travel + Overtime",
            "Employees": len(ftot), "Attrition %": f"{ftot['Attrition'].mean()*100:.1f}%",
            "Action": "Review travel necessity; offer virtual alternatives"
        })

    new_e = df[df["TenureBand"] == "New (0-2yr)"]
    if len(new_e) > 0:
        segments.append({
            "Priority": "MEDIUM", "Segment": "New Employees (0–2yr Tenure)",
            "Employees": len(new_e), "Attrition %": f"{new_e['Attrition'].mean()*100:.1f}%",
            "Action": "Onboarding programme; 30-60-90 day check-ins"
        })

    stag = df[df["YearsSinceLastPromotion"] >= 6]
    if len(stag) > 0:
        segments.append({
            "Priority": "MEDIUM", "Segment": "Promotion Stagnation (6+ yrs since last promo)",
            "Employees": len(stag), "Attrition %": f"{stag['Attrition'].mean()*100:.1f}%",
            "Action": "Career pathway conversations; lateral growth options"
        })

    low_e = df[df["EngagementTier"] == "Low"]
    if len(low_e) > 0:
        segments.append({
            "Priority": "MEDIUM", "Segment": "Low Engagement Tier",
            "Employees": len(low_e), "Attrition %": f"{low_e['Attrition'].mean()*100:.1f}%",
            "Action": "Engagement review; exit interview analysis"
        })

    far = df[df["CommuteBand"] == "Far (>15km)"]
    if len(far) > 0:
        segments.append({
            "Priority": "MONITOR", "Segment": "Far Commute Employees (>15km)",
            "Employees": len(far), "Attrition %": f"{far['Attrition'].mean()*100:.1f}%",
            "Action": "Consider hybrid/remote work policy"
        })

    seg_df = pd.DataFrame(segments)
    if len(seg_df) > 0:
        st.dataframe(seg_df, width="stretch", hide_index=True,
                     column_config={
                         "Priority": st.column_config.TextColumn("Priority", width="small"),
                         "Segment": st.column_config.TextColumn("Segment", width="large"),
                         "Employees": st.column_config.NumberColumn("Employees", width="small"),
                         "Attrition %": st.column_config.TextColumn("Attrition %", width="small"),
                         "Action": st.column_config.TextColumn("Recommended Action", width="large")
                     })

    st.markdown("---")
    st.markdown('<div class="section-header">Low-Engagement Alerts by Department & Role</div>',
                unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        low_by_dept = df[df["EngagementTier"] == "Low"].groupby("Department").size().reset_index(name="Low Engagement Count")
        low_by_dept_all = df.groupby("Department").size().reset_index(name="Total")
        low_by_dept = low_by_dept.merge(low_by_dept_all, on="Department")
        low_by_dept["% of Dept"] = (low_by_dept["Low Engagement Count"] / low_by_dept["Total"] * 100).round(1)

        fig_low_dept = px.bar(
            low_by_dept.sort_values("Low Engagement Count"), x="Low Engagement Count", y="Department",
            orientation="h", text="Low Engagement Count", color="% of Dept",
            color_continuous_scale=["#2ecc71", "#e74c3c"], title="Low Engagement Employees by Department"
        )
        fig_low_dept.update_traces(textposition="outside")
        fig_low_dept.update_layout(coloraxis_showscale=True, margin=dict(t=50, b=20, l=10, r=60),
                                   coloraxis_colorbar=dict(title="% of Dept"))
        render_chart(fig_low_dept, height=260, key="low_dept")

    with c2:
        # Rewritten from groupby().apply(..., include_groups=False) — the
        # "Both" flag needs two columns at once, so this precomputes boolean
        # helper columns and aggregates with plain .agg(), which works on
        # every pandas version instead of only >=2.2.
        tmp = df.assign(
            _low_ei=(df["EngagementTier"] == "Low").astype(int),
            _high_burnout=(df["BurnoutRisk"] == "High").astype(int),
        )
        tmp["_both"] = tmp["_low_ei"] & tmp["_high_burnout"]
        overlap = (
            tmp.groupby("JobRole")
            .agg(**{"Low EI": ("_low_ei", "sum"), "High Burnout": ("_high_burnout", "sum"),
                    "Both": ("_both", "sum"), "Total": ("_low_ei", "count")})
            .reset_index()
        )
        overlap = overlap[overlap["High Burnout"] > 0].sort_values("High Burnout", ascending=True)

        fig_overlap = go.Figure()
        fig_overlap.add_trace(go.Bar(y=overlap["JobRole"], x=overlap["High Burnout"], name="High Burnout",
                                     orientation="h", marker_color=C_LOW, opacity=0.8))
        fig_overlap.add_trace(go.Bar(y=overlap["JobRole"], x=overlap["Low EI"], name="Low Engagement",
                                     orientation="h", marker_color=C_MED, opacity=0.8))
        fig_overlap.update_layout(barmode="group", title="High Burnout & Low Engagement by Role",
                                  margin=dict(t=50, b=20, l=10, r=20), legend=dict(orientation="h", y=-0.2))
        render_chart(fig_overlap, height=260, key="overlap")

    st.markdown("---")
    st.markdown(f'<div class="section-header">{icon("compass", 18, C_BLUE)}Recommended Actions</div>',
                unsafe_allow_html=True)

    act1, act2, act3 = st.columns(3)

    with act1:
        st.markdown(
            alert_box("red", "Immediate (0–3 months)",
                f"Contact all Danger Zone employees directly. Audit {len(ot_emp):,} overtime employees "
                f"for structural vs. project-driven overload. Review exit interviews from Low-EI leavers."),
            unsafe_allow_html=True,
        )

    with act2:
        st.markdown(
            alert_box("amber", "Medium-term (3–12 months)",
                "Launch 30/60/90-day onboarding check-ins for new hires. Pair promotions with a "
                "support package, not just a title change. Run a targeted engagement diagnostic for Sales."),
            unsafe_allow_html=True,
        )

    with act3:
        st.markdown(
            alert_box("green", "Long-term (12+ months)",
                "Turn these five KPIs into a standing quarterly HR dashboard. Extend hybrid/remote "
                "policy to employees commuting 15km+. Train managers on the workload/engagement paradox."),
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("Explore Filtered Employee Data"):
        cols_show = ["Age", "Department", "JobRole", "OverTime", "BusinessTravel",
                     "YearsAtCompany", "YearsSinceLastPromotion",
                     "EngagementIndex", "EngagementTier", "BurnoutRisk", "BurnoutScore",
                     "WorkloadStress", "StressLevel", "Attrition"]
        cols_show = [c for c in cols_show if c in df.columns]
        st.dataframe(df[cols_show].sort_values("EngagementIndex").reset_index(drop=True), width="stretch")
        st.caption(f"Showing {n:,} employees after current filters.")


# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style='text-align:center; color:{T["text_secondary"]}; font-size:0.78rem;
            border-top: 1px solid {T["card_border"]}; padding-top: 16px; margin-top: 20px;'>
    Palo Alto Networks HR Analytics Dashboard &nbsp;|&nbsp;
    Himanshu Rai &nbsp;|&nbsp;
    Dataset: 1,470 employees &nbsp;|&nbsp;
    Built with Python + Streamlit + Plotly
</div>
""", unsafe_allow_html=True)