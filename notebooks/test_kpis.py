import sys
sys.path.append('.')

from src.data_loader import load_clean_data
from src.features import add_features
from src.trends import get_monthly_trends
from src.kpis import calculate_kpis

# Full pipeline
df = load_clean_data()
df = add_features(df)
monthly = get_monthly_trends(df)
kpis = calculate_kpis(df, monthly)

# Print all KPIs cleanly
print("=" * 50)
print("DASHBOARD KPI SUMMARY")
print("=" * 50)

print(f"\n── SCALE ──────────────────────────────────────")
print(f"Peak HHS Care Load     : {kpis['peak_care_load']:,} children")
print(f"Date of Peak           : {kpis['peak_care_load_date']}")
print(f"Peak System Load       : {kpis['peak_system_load']:,} children")
print(f"Peak System Load Date  : {kpis['peak_system_load_date']}")

print(f"\n── THROUGHPUT ─────────────────────────────────")
print(f"Total Apprehended      : {kpis['total_apprehended']:,}")
print(f"Total Discharged       : {kpis['total_discharged']:,}")
print(f"Net Intake Pressure    : {kpis['net_intake_pressure']:,}")
print(f"Discharge Offset Ratio : {kpis['discharge_offset_ratio']}")

print(f"\n── STRESS ─────────────────────────────────────")
print(f"High Stress Days       : {kpis['high_stress_days']} ({kpis['high_stress_pct']}% of all days)")
print(f"Worst Month            : {kpis['worst_month']} (avg {kpis['worst_month_avg']:,})")

print(f"\n── CURRENT STATUS ─────────────────────────────")
print(f"Current HHS Care Load  : {kpis['current_hhs_care']:,} children")
print(f"As of                  : {kpis['current_date']}")
print(f"Reduction from Peak    : {kpis['reduction_from_peak']:,} children ({kpis['reduction_pct']}%)")
print(f"System Status          : {kpis['system_status']}")

print(f"\n── RECOVERY ───────────────────────────────────")
print(f"Best Recent Month      : {kpis['best_recent_month']} (avg {kpis['best_recent_month_avg']:,})")