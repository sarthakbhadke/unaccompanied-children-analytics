import sys
sys.path.append('.')

import pandas as pd

from src.data_loader import load_clean_data

df = load_clean_data()

print("Dataset loaded:", df.shape)
print()

# ── BASIC STATS ──────────────────────────────────────────────────────
print("=" * 55)
print("BASIC STATISTICS")
print("=" * 55)
print(df.describe().round(1))
print()

# ── PEAK STRESS: most children in HHS care at one time ───────────────
print("=" * 55)
print("TOP 5 HIGHEST HHS CARE LOAD DAYS")
print("=" * 55)
top_hhs = df.nlargest(5, 'hhs_in_care')[['date', 'hhs_in_care', 'cbp_in_custody']]
print(top_hhs.to_string(index=False))
print()

# ── PEAK INTAKE: most children apprehended in one day ────────────────
print("=" * 55)
print("TOP 5 HIGHEST SINGLE-DAY APPREHENSIONS")
print("=" * 55)
top_cbp = df.nlargest(5, 'cbp_apprehended')[['date', 'cbp_apprehended', 'cbp_in_custody']]
print(top_cbp.to_string(index=False))
print()

# ── RELIEF: most children discharged in one day ──────────────────────
print("=" * 55)
print("TOP 5 HIGHEST SINGLE-DAY DISCHARGES")
print("=" * 55)
top_discharge = df.nlargest(5, 'hhs_discharged')[['date', 'hhs_discharged', 'hhs_in_care']]
print(top_discharge.to_string(index=False))
print()

# ── MONTHLY AVERAGES ─────────────────────────────────────────────────
print("=" * 55)
print("MONTHLY AVERAGE - HHS CARE LOAD")
print("=" * 55)

# dt.to_period('M') converts a date like 2023-01-12 to the period "2023-01"
# This lets us group all days in the same month together
monthly = df.groupby(df['date'].dt.to_period('M')).agg(
    avg_hhs_care   = ('hhs_in_care',     'mean'),
    avg_cbp        = ('cbp_in_custody',  'mean'),
    avg_discharged = ('hhs_discharged',  'mean'),
    days_reported  = ('date',            'count')
).round(1)

print(monthly.to_string())
print()

# ── YEAR OVER YEAR ───────────────────────────────────────────────────
print("=" * 55)
print("YEARLY SUMMARY")
print("=" * 55)

yearly = df.groupby(df['date'].dt.year).agg(
    avg_hhs_care    = ('hhs_in_care',    'mean'),
    max_hhs_care    = ('hhs_in_care',    'max'),
    total_discharge = ('hhs_discharged', 'sum'),
    total_apprehend = ('cbp_apprehended','sum'),
    days_reported   = ('date',           'count')
).round(1)

yearly.index.name = 'year'
print(yearly.to_string())
print()

# ── BALANCE: is intake overwhelming discharge? ───────────────────────
print("=" * 55)
print("INTAKE vs DISCHARGE BALANCE (by year)")
print("=" * 55)

balance = df.groupby(df['date'].dt.year).agg(
    total_transferred_to_hhs = ('cbp_transferred',  'sum'),
    total_discharged_from_hhs= ('hhs_discharged',   'sum'),
).round(1)

balance['net_pressure'] = (
    balance['total_transferred_to_hhs'] - balance['total_discharged_from_hhs']
)

balance.index.name = 'year'
print(balance.to_string())
print()
print("Positive net_pressure = more kids entering HHS than leaving")
print("Negative net_pressure = more kids leaving than entering (system relieving)")

