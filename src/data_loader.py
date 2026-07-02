import pandas as pd

def load_clean_data(path='data/hhs_data.csv'):
    
    # ── STEP A: Load raw CSV ─────────────────────────────────────────
    df = pd.read_csv(path)

    # ── STEP B: Drop completely empty rows ───────────────────────────
    df = df.dropna(how='all')

    # ── STEP C: Rename columns ───────────────────────────────────────
    df.columns = [
        'date',
        'cbp_apprehended',
        'cbp_in_custody',
        'cbp_transferred',
        'hhs_in_care',
        'hhs_discharged'
    ]

    # ── STEP D: Convert date from string to datetime ─────────────────
    df['date'] = pd.to_datetime(df['date'], format='%B %d, %Y')

    # ── STEP E: Clean hhs_in_care (remove commas, convert to number) ─
    df['hhs_in_care'] = df['hhs_in_care'].astype(str).str.replace(',', '', regex=False)
    df['hhs_in_care'] = pd.to_numeric(df['hhs_in_care'], errors='coerce')

    # ── STEP F: Sort oldest to newest ────────────────────────────────
    df = df.sort_values('date').reset_index(drop=True)

    return df