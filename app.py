import streamlit as st
import sys
sys.path.append('.')

from src.data_loader import load_clean_data
from src.features   import add_features
from src.trends     import get_monthly_trends, get_weekly_trends
from src.kpis       import calculate_kpis

# ── Page config ───────────────────────────────────────────────────────
st.set_page_config(
    page_title = 'UAC Care Analytics',
    page_icon  = '🏥',
    layout     = 'wide'
)

# ── Load and cache all data once ──────────────────────────────────────
@st.cache_data
def load_all_data():
    df      = load_clean_data()
    df      = add_features(df)
    monthly = get_monthly_trends(df)
    weekly  = get_weekly_trends(df)
    kpis    = calculate_kpis(df, monthly)
    return df, monthly, weekly, kpis

df, monthly, weekly, kpis = load_all_data()

# ── Store base data in session state ──────────────────────────────────
st.session_state['df']      = df
st.session_state['monthly'] = monthly
st.session_state['weekly']  = weekly
st.session_state['kpis']    = kpis

# ── Sidebar ───────────────────────────────────────────────────────────
with st.sidebar:
    st.title('🏥 UAC Analytics')
    st.caption('System Capacity & Care Load\nDept. of Health & Human Services')
    st.divider()

    st.subheader('Filters')

    min_date = df['date'].min().date()
    max_date = df['date'].max().date()

    date_range = st.date_input(
        'Date Range',
        value     = (min_date, max_date),
        min_value = min_date,
        max_value = max_date,
        key       = 'date_range_input'
    )

    granularity = st.radio(
        'Time Granularity',
        options = ['Daily', 'Weekly', 'Monthly'],
        index   = 0,
        key     = 'granularity_input'
    )

    show_rolling = st.toggle(
        'Show 7-Day Average',
        value = True,
        key   = 'rolling_input'
    )

    st.divider()
    st.caption(f"📅 Data: Jan 2023 – Dec 2025\n📊 {len(df)} reporting days")

# ── Save filter state ─────────────────────────────────────────────────
# Only save date_range when BOTH dates have been selected
if isinstance(date_range, tuple) and len(date_range) == 2:
    st.session_state['date_range']   = date_range
    st.session_state['granularity']  = granularity
    st.session_state['show_rolling'] = show_rolling

# ── Home page ─────────────────────────────────────────────────────────
st.title('🏥 UAC System Capacity & Care Load Analytics')
st.markdown("""
This dashboard provides analytics for the **Unaccompanied Alien Children (UAC)**
care pipeline managed by the U.S. Department of Health & Human Services.

**Navigate using the sidebar** to explore:
- 📊 **Overview** — System-wide KPIs and care load timeline
- 🔄 **CBP vs HHS** — Custody pipeline comparison
- 📈 **Intake & Backlog** — Pressure and relief trends
""")

st.divider()

# ── Headline KPIs ─────────────────────────────────────────────────────
st.subheader('Headline Numbers')
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label = '🔺 Peak Care Load',
        value = f"{kpis['peak_care_load']:,}",
        delta = kpis['peak_care_load_date']
    )
with col2:
    st.metric(
        label = '📍 Current Care Load',
        value = f"{kpis['current_hhs_care']:,}",
        delta = f"-{kpis['reduction_pct']}% from peak",
    )
with col3:
    st.metric(
        label = '✅ Total Discharged',
        value = f"{kpis['total_discharged']:,}",
        delta = 'Full timeline'
    )
with col4:
    st.metric(
        label = '🔄 System Status',
        value = kpis['system_status'],
        delta = f"{kpis['high_stress_days']} high-stress days"
    )