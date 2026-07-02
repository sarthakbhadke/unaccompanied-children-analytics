import streamlit as st
import sys
sys.path.append('.')

from src.charts      import chart_cbp_vs_hhs, chart_monthly_avg_bar
from src.filter_data import apply_filters

st.set_page_config(page_title='CBP vs HHS', page_icon='🔄', layout='wide')

if 'df' not in st.session_state:
    st.warning('⚠️ Please navigate from the main page first.')
    st.stop()

df_f, monthly_f, weekly_f, granularity, show_rolling = apply_filters(
    st.session_state['df'],
    st.session_state['monthly'],
    st.session_state['weekly']
)
kpis = st.session_state['kpis']

st.title('🔄 CBP vs HHS Comparison')
st.caption(f"Showing {len(df_f)} reporting days | Granularity: {granularity}")
st.divider()

# ── Pipeline KPIs ─────────────────────────────────────────────────────
st.subheader('Care Pipeline Summary')
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric('Total Apprehended',       f"{kpis['total_apprehended']:,}")
with c2:
    st.metric('Total Transferred to HHS',f"{int(df_f['cbp_transferred'].sum()):,}")
with c3:
    st.metric('Total Discharged',        f"{int(df_f['hhs_discharged'].sum()):,}")
with c4:
    st.metric('Discharge Offset Ratio',  f"{kpis['discharge_offset_ratio']}x")

st.divider()

# ── Charts ────────────────────────────────────────────────────────────
st.subheader('CBP Custody vs HHS Care Load Over Time')
fig1 = chart_cbp_vs_hhs(df_f)
st.plotly_chart(fig1, use_container_width=True)

st.subheader('Average Monthly HHS Care Load')
fig2 = chart_monthly_avg_bar(monthly_f)
st.plotly_chart(fig2, use_container_width=True)

st.info(
    f"📌 **Discharge Offset Ratio of {kpis['discharge_offset_ratio']}x** — "
    f"for every child transferred into HHS, 1.35 children were discharged "
    f"to sponsors. The system processed more than it received."
)

with st.expander('🔍 View pipeline data for selected range'):
    st.dataframe(
        df_f[['date','cbp_apprehended','cbp_in_custody',
              'cbp_transferred','hhs_discharged']].reset_index(drop=True),
        use_container_width=True
    )