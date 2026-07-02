import sys
sys.path.append('.')

from src.data_loader import load_clean_data
from src.features import add_features
from src.trends import get_weekly_trends, get_monthly_trends, get_stress_periods

# Build the full pipeline
df = load_clean_data()
df = add_features(df)

# ── Weekly trends ─────────────────────────────────────────────────────
weekly = get_weekly_trends(df)
print("WEEKLY TRENDS SHAPE:", weekly.shape)
print("Columns:", list(weekly.columns))
print()
print("First 4 weeks:")
print(weekly.head(4).to_string(index=False))
print()

# ── Monthly trends ────────────────────────────────────────────────────
monthly = get_monthly_trends(df)
print("MONTHLY TRENDS SHAPE:", monthly.shape)
print()
print("All months - HHS care load:")
print(monthly[['month_label', 'avg_hhs_care', 'max_hhs_care',
               'total_discharged', 'net_intake_total']].to_string(index=False))
print()

# ── Stress periods ────────────────────────────────────────────────────
df_stress = get_stress_periods(df)
print()
print("Stress breakdown:")
print(df_stress['stress_label'].value_counts())