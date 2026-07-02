import pandas as pd
import streamlit as st

def apply_filters(df, monthly, weekly):
    """
    Reads filter selections from session_state and returns
    filtered versions of df, monthly, and weekly.

    Called at the top of every page — ensures all charts
    respond to the same sidebar filter selections.
    """

    # ── Date filter ───────────────────────────────────────────────────
    # Get date range from session state, fall back to full range
    if 'date_range' in st.session_state:
        date_range = st.session_state['date_range']
    else:
        date_range = (df['date'].min().date(), df['date'].max().date())

    start_date, end_date = date_range

    # Filter daily df
    df_filtered = df[
        (df['date'].dt.date >= start_date) &
        (df['date'].dt.date <= end_date)
    ].copy()

    # Filter monthly — convert period index back to date for comparison
    monthly_filtered = monthly[
        (monthly['date'].dt.date >= start_date) &
        (monthly['date'].dt.date <= end_date)
    ].copy()

    # Filter weekly
    weekly_filtered = weekly[
        (weekly['date'].dt.date >= start_date) &
        (weekly['date'].dt.date <= end_date)
    ].copy()

    # ── Granularity ───────────────────────────────────────────────────
    granularity  = st.session_state.get('granularity', 'Daily')

    # ── Rolling avg toggle ────────────────────────────────────────────
    show_rolling = st.session_state.get('show_rolling', True)

    return df_filtered, monthly_filtered, weekly_filtered, granularity, show_rolling