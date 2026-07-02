import sys
sys.path.append('.')

from src.data_loader import load_clean_data
from src.features import add_features

# Step 1: load clean data
df = load_clean_data()

# Step 2: add engineered features
df = add_features(df)

# ── Verify new columns exist ─────────────────────────────────────────
print("Columns after feature engineering:")
for col in df.columns:
    print(" ", col)
print()

# ── Check first 5 rows of new columns ────────────────────────────────
new_cols = [
    'date',
    'total_system_load',
    'net_daily_intake',
    'care_load_growth_pct',
    'hhs_care_7day_avg',
    'net_intake_7day_avg',
    'cumulative_backlog'
]
print("Sample of engineered features:")
print(df[new_cols].head(10).to_string(index=False))
print()

# ── Sanity checks ────────────────────────────────────────────────────
print("Max total system load:",  df['total_system_load'].max())
print("Date of max load:     ",  df.loc[df['total_system_load'].idxmax(), 'date'])
print()
print("Max cumulative backlog:", df['cumulative_backlog'].max())
print("Min cumulative backlog:", df['cumulative_backlog'].min())