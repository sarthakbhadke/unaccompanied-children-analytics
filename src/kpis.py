import pandas as pd

def calculate_kpis(df, monthly):
    """
    Calculates all dashboard KPI values.
    
    Parameters:
        df      : full daily dataframe with features from add_features()
        monthly : monthly summary from get_monthly_trends()
    
    Returns:
        dict of KPI name -> value, ready to display in Streamlit
    """
    kpis = {}

    # ── KPI 1: Peak Care Load ─────────────────────────────────────────
    # Single highest number of children in HHS care on any one day
    kpis['peak_care_load'] = int(df['hhs_in_care'].max())
    kpis['peak_care_load_date'] = df.loc[
        df['hhs_in_care'].idxmax(), 'date'
    ].strftime('%B %d, %Y')

    # ── KPI 2: Total Children Discharged ─────────────────────────────
    # Sum of all successful sponsor placements across full timeline
    kpis['total_discharged'] = int(df['hhs_discharged'].sum())

    # ── KPI 3: Total Children Apprehended ────────────────────────────
    kpis['total_apprehended'] = int(df['cbp_apprehended'].sum())

    # ── KPI 4: Peak System Load (CBP + HHS combined) ─────────────────
    kpis['peak_system_load'] = int(df['total_system_load'].max())
    kpis['peak_system_load_date'] = df.loc[
        df['total_system_load'].idxmax(), 'date'
    ].strftime('%B %d, %Y')

    # ── KPI 5: Net Intake Pressure (full timeline) ───────────────────
    # Total transfers into HHS minus total discharges
    # Negative = system has discharged more than it received overall
    total_transferred = df['cbp_transferred'].sum()
    total_discharged  = df['hhs_discharged'].sum()
    kpis['net_intake_pressure'] = int(total_transferred - total_discharged)

    # ── KPI 6: Discharge Offset Ratio ────────────────────────────────
    # For every child that entered HHS, how many were discharged?
    # > 1.0 means discharges outpaced intake (healthy)
    # < 1.0 means intake outpaced discharges (pressure building)
    kpis['discharge_offset_ratio'] = round(
        total_discharged / total_transferred, 2
    )

    # ── KPI 7: High Stress Days ───────────────────────────────────────
    # Days where HHS care load exceeded 75th percentile
    threshold = df['hhs_in_care'].quantile(0.75)
    kpis['high_stress_days'] = int((df['hhs_in_care'] > threshold).sum())
    kpis['high_stress_pct'] = round(
        kpis['high_stress_days'] / len(df) * 100, 1
    )

    # ── KPI 8: Current Care Load (most recent day) ───────────────────
    # Last row = most recent date after sorting
    kpis['current_hhs_care'] = int(df['hhs_in_care'].iloc[-1])
    kpis['current_date'] = df['date'].iloc[-1].strftime('%B %d, %Y')

    # ── KPI 9: Care Load Change from Peak ────────────────────────────
    # How much has the system reduced since its worst day?
    peak = kpis['peak_care_load']
    current = kpis['current_hhs_care']
    kpis['reduction_from_peak'] = int(peak - current)
    kpis['reduction_pct'] = round((peak - current) / peak * 100, 1)

    # ── KPI 10: System Status ─────────────────────────────────────────
    # Based on last 30 days trend — is the system growing or shrinking?
    last_30 = df.tail(30)
    recent_avg = last_30['hhs_in_care'].mean()
    prior_30 = df.iloc[-60:-30]
    prior_avg = prior_30['hhs_in_care'].mean()

    if recent_avg > prior_avg * 1.05:
        kpis['system_status'] = 'Expanding'
        kpis['status_color'] = 'red'
    elif recent_avg < prior_avg * 0.95:
        kpis['system_status'] = 'Contracting'
        kpis['status_color'] = 'green'
    else:
        kpis['system_status'] = 'Stable'
        kpis['status_color'] = 'orange'

        # ── KPI 11: Worst Month ───────────────────────────────────────────
    worst_month_idx = monthly['avg_hhs_care'].idxmax()
    kpis['worst_month'] = monthly.loc[worst_month_idx, 'month_label']
    kpis['worst_month_avg'] = round(
        monthly.loc[worst_month_idx, 'avg_hhs_care'], 0
    )

    # ── KPI 12: Best Recent Month ────────────────────────────────────
    # Lowest average care load in 2025 (most recent year)
    monthly_2025 = monthly[monthly['date'].dt.year == 2025]
    best_idx = monthly_2025['avg_hhs_care'].idxmin()
    kpis['best_recent_month'] = monthly.loc[best_idx, 'month_label']
    kpis['best_recent_month_avg'] = round(
        monthly.loc[best_idx, 'avg_hhs_care'], 0
    )

    return kpis

