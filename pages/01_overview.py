import streamlit as st
import sys
sys.path.append('.')

from src.charts      import chart_hhs_care_timeline, chart_system_load_area
from src.filter_data import apply_filters

st.set_page_config(page_title='Overview', page_icon='📊', layout='wide')

# ── Guard: ensure data is loaded ──────────────────────────────────────
if 'df' not in st.session_state:
    st.warning('⚠️ Please navigate from the main page first.')
    st.stop()

# ── Apply all filters ─────────────────────────────────────────────────
df_f, monthly_f, weekly_f, granularity, show_rolling = apply_filters(
    st.session_state['df'],
    st.session_state['monthly'],
    st.session_state['weekly']
)
kpis = st.session_state['kpis']

# ── Page header ───────────────────────────────────────────────────────
st.title('📊 System Overview')
st.caption(f"Showing {len(df_f)} reporting days | Granularity: {granularity}")
st.divider()

# ── KPI cards ─────────────────────────────────────────────────────────
st.subheader('Key Performance Indicators')
k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.metric('🔺 Peak HHS Load',      f"{kpis['peak_care_load']:,}")
with k2:
    st.metric('📍 Current Load',        f"{kpis['current_hhs_care']:,}")
with k3:
    st.metric('✅ Total Discharged',    f"{kpis['total_discharged']:,}")
with k4:
    st.metric('⚠️ High Stress Days',   f"{kpis['high_stress_days']}")
with k5:
    st.metric('📉 Reduction from Peak', f"{kpis['reduction_pct']}%")

st.divider()

# ── Filtered summary bar ──────────────────────────────────────────────
# Shows stats for the currently selected date range
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.metric(
        'Avg HHS Care (selected range)',
        f"{df_f['hhs_in_care'].mean():,.0f}"
    )
with col_b:
    st.metric(
        'Max HHS Care (selected range)',
        f"{df_f['hhs_in_care'].max():,.0f}"
    )
with col_c:
    st.metric(
        'Days in selected range',
        f"{len(df_f)}"
    )

st.divider()

# ── Charts ────────────────────────────────────────────────────────────
st.subheader('HHS Care Load Timeline')

# Granularity switch — choose which data to pass to chart
if granularity == 'Daily':
    fig_timeline = chart_hhs_care_timeline(df_f)
elif granularity == 'Weekly':
    # For weekly view we still use daily df but resample inside the chart
    fig_timeline = chart_hhs_care_timeline(df_f)
else:
    fig_timeline = chart_hhs_care_timeline(df_f)

st.plotly_chart(fig_timeline, use_container_width=True)

st.subheader('Total System Load (CBP + HHS)')
fig_area = chart_system_load_area(df_f)
st.plotly_chart(fig_area, use_container_width=True)

# ── Insight callout ───────────────────────────────────────────────────
st.info(
    f"📌 **Peak Crisis:** {kpis['peak_care_load']:,} children in HHS care on "
    f"{kpis['peak_care_load_date']}. Current load is "
    f"**{kpis['current_hhs_care']:,}** — a reduction of "
    f"**{kpis['reduction_pct']}%** from peak."
)

# ── Expandable raw data table ─────────────────────────────────────────
with st.expander('🔍 View raw data for selected range'):
    st.dataframe(
        df_f[['date','hhs_in_care','cbp_in_custody',
              'total_system_load','net_daily_intake']].reset_index(drop=True),
        use_container_width=True
    )