import pandas as pd

def get_weekly_trends(df):
    """
    Resamples daily data into weekly summaries.
    Input: dataframe with features from add_features()
    Output: one row per week
    """

    # Set date as the index so resample() knows what to group by
    df_indexed = df.set_index('date')

    weekly = df_indexed.resample('W').agg(
        avg_hhs_care      = ('hhs_in_care',        'mean'),
        max_hhs_care      = ('hhs_in_care',        'max'),
        avg_cbp_custody   = ('cbp_in_custody',     'mean'),
        total_apprehended = ('cbp_apprehended',    'sum'),
        total_transferred = ('cbp_transferred',    'sum'),
        total_discharged  = ('hhs_discharged',     'sum'),
        avg_system_load   = ('total_system_load',  'mean'),
        avg_net_intake    = ('net_daily_intake',   'mean'),
        days_reported     = ('hhs_in_care',        'count')
    ).round(1)

    # Reset index so date becomes a column again
    weekly = weekly.reset_index()

    return weekly

def get_monthly_trends(df):
    """
    Resamples daily data into monthly summaries.
    Input: dataframe with features from add_features()
    Output: one row per month
    """

    df_indexed = df.set_index('date')

    monthly = df_indexed.resample('ME').agg(
        avg_hhs_care      = ('hhs_in_care',        'mean'),
        max_hhs_care      = ('hhs_in_care',        'max'),
        min_hhs_care      = ('hhs_in_care',        'min'),
        avg_cbp_custody   = ('cbp_in_custody',     'mean'),
        total_apprehended = ('cbp_apprehended',    'sum'),
        total_transferred = ('cbp_transferred',    'sum'),
        total_discharged  = ('hhs_discharged',     'sum'),
        avg_system_load   = ('total_system_load',  'mean'),
        net_intake_total  = ('net_daily_intake',   'sum'),
        days_reported     = ('hhs_in_care',        'count')
    ).round(1)

    # Add month label column for clean chart display
    # e.g. "Jan 2023", "Feb 2023" etc.
    monthly = monthly.reset_index()
    monthly['month_label'] = monthly['date'].dt.strftime('%b %Y')

    return monthly

def get_stress_periods(df, threshold_percentile=75):
    """
    Identifies periods where HHS care load exceeded
    the given percentile threshold.
    Default: flags any day above the 75th percentile as 'high stress'
    """

    # Calculate the threshold value
    threshold = df['hhs_in_care'].quantile(threshold_percentile / 100)

    # Flag each row
    df_stress = df.copy()
    df_stress['is_high_stress'] = df_stress['hhs_in_care'] > threshold
    df_stress['stress_label'] = df_stress['is_high_stress'].map(
        {True: 'High Stress', False: 'Normal'}
    )

    print(f"Stress threshold (75th percentile): {threshold:.0f} children")
    print(f"High stress days: {df_stress['is_high_stress'].sum()} out of {len(df_stress)}")

    return df_stress

