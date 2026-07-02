import pandas as pd

def add_features(df):
    """
    Takes the clean dataframe from load_clean_data()
    and adds engineered columns for dashboard use.
    Always call load_clean_data() first, then pass
    the result into this function.
    """

    # Work on a copy so the original is never modified
    df = df.copy()

    # ── FEATURE 1: Total System Load ─────────────────────────────────
    # How many children is the entire system responsible for on each day?
    # CBP custody + HHS care = full picture
    df['total_system_load'] = df['cbp_in_custody'] + df['hhs_in_care']

    # ── FEATURE 2: Net Daily Intake ──────────────────────────────────
    # Are more children entering HHS than leaving on this day?
    # Positive = system pressure building
    # Negative = system relieving
    df['net_daily_intake'] = df['cbp_transferred'] - df['hhs_discharged']

    # ── FEATURE 3: Care Load Growth Rate (day over day %) ────────────
    # How much did HHS care load change compared to yesterday?
    # pct_change() calculates: (today - yesterday) / yesterday * 100
    df['care_load_growth_pct'] = df['hhs_in_care'].pct_change() * 100
    df['care_load_growth_pct'] = df['care_load_growth_pct'].round(2)

    # ── FEATURE 4: 7-day Rolling Average of HHS Care Load ────────────
    # Smooths out day-to-day noise to show the real trend
    # min_periods=1 means: start calculating even if we have fewer than 7 days
    df['hhs_care_7day_avg'] = (
        df['hhs_in_care']
        .rolling(window=7, min_periods=1)
        .mean()
        .round(1)
    )

    # ── FEATURE 5: 7-day Rolling Average of Net Intake ───────────────
    # Shows whether pressure is building or relieving on a trend basis
    df['net_intake_7day_avg'] = (
        df['net_daily_intake']
        .rolling(window=7, min_periods=1)
        .mean()
        .round(1)
    )

    # ── FEATURE 6: Cumulative Backlog ────────────────────────────────
    # Running total of net_daily_intake over time
    # Shows whether the system is accumulating or reducing its load
    # across the entire timeline
    df['cumulative_backlog'] = df['net_daily_intake'].cumsum().round(1)

    return df