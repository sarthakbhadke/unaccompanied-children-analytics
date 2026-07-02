import streamlit as st
import sys
sys.path.append('.')

from src.charts      import chart_net_intake_monthly, chart_cumulative_backlog
from src.filter_data import apply_filters

st.set_page_config(page_title='Intake & Backlog', page_icon='📈', layout='wide')

if 'df' not in st.session_state:
    st.warning('⚠️ Please navigate from the main page first.')
    st.stop()

df_f, monthly_f, weekly_f, granularity, show_rolling = apply_filters(
    st.session_state['df'],
    st.session_state['monthly'],
    st.session_state['weekly']
)
kpis = st.session_state['kpis']

st.title('📈 Net Intake & Backlog Trends')
st.caption(f"Showing {len(df_f)} reporting days | Granularity: {granularity}")
st.divider()

# ── Pressure KPIs ─────────────────────────────────────────────────────
st.subheader('Pressure Indicators')
p1, p2, p3, p4 = st.columns(4)

with p1:
    st.metric('Net Intake Pressure',  f"{kpis['net_intake_pressure']:,}")
with p2:
    st.metric('High Stress Days',     f"{kpis['high_stress_days']}")
with p3:
    st.metric('Worst Month',          kpis['worst_month'])
with p4:
    st.metric('Best Recent Month',    kpis['best_recent_month'])

st.divider()

# ── Charts ────────────────────────────────────────────────────────────
st.subheader('Monthly Net Intake — Green = Relief, Red = Pressure')
fig1 = chart_net_intake_monthly(monthly_f)
st.plotly_chart(fig1, use_container_width=True)

st.subheader('Cumulative Net Intake Over Time')
fig2 = chart_cumulative_backlog(df_f)
st.plotly_chart(fig2, use_container_width=True)

st.info(
    "📌 A consistently **negative cumulative backlog** means discharges "
    "outpaced transfers across the full timeline — a net positive outcome. "
    "Use the date filter to isolate specific pressure windows."
)

with st.expander('🔍 View intake & backlog data for selected range'):
    st.dataframe(
        df_f[['date','net_daily_intake','cumulative_backlog',
              'hhs_care_7day_avg','net_intake_7day_avg']].reset_index(drop=True),
        use_container_width=True
    )