import sys
sys.path.append('.')

from src.data_loader import load_clean_data
from src.features import add_features
from src.trends import get_monthly_trends
from src.charts import (
    chart_hhs_care_timeline,
    chart_cbp_vs_hhs,
    chart_net_intake_monthly,
    chart_system_load_area,
    chart_monthly_avg_bar,
    chart_cumulative_backlog
)

# Full pipeline
df      = load_clean_data()
df      = add_features(df)
monthly = get_monthly_trends(df)

# Test all 6 charts
charts = {
    'HHS Care Timeline'   : chart_hhs_care_timeline(df),
    'CBP vs HHS'          : chart_cbp_vs_hhs(df),
    'Net Intake Monthly'  : chart_net_intake_monthly(monthly),
    'System Load Area'    : chart_system_load_area(df),
    'Monthly Avg Bar'     : chart_monthly_avg_bar(monthly),
    'Cumulative Backlog'  : chart_cumulative_backlog(df),
}

for name, fig in charts.items():
    n_traces = len(fig.data)
    title    = fig.layout.title.text
    print(f"✅ {name}")
    print(f"   Title  : {title}")
    print(f"   Traces : {n_traces}")
    print()

print("All 6 charts created successfully")

# Open one chart in browser to visually verify
charts['HHS Care Timeline'].show()