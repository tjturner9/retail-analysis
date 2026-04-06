import pandas as pd


NON_STANDARD_CODES = {
    'POST', 'DOT', 'M', 'D', 'S', 'C2', 'B',
    'BANK CHARGES', 'AMAZONFEE', 'ADJUST'
}


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply cleaning decisions to the raw loaded dataframe.

    Excluded:
    - Non-standard StockCodes (POST, DOT, M, D, S, C2, B,
      BANK CHARGES, AMAZONFEE, ADJUST) — accounting/admin entries
    - Zero or negative price rows (non-cancellation) — warehouse
      adjustments, bad debt write-offs, samples
    - Null descriptions — uninformative, small volume

    Retained with flag:
    - Extreme quantities (>10,000 units) — possible wholesale orders,
      flagged as IsOutlier

    Null Customer IDs:
    - Retained in base cleaned data
    - Filter on Customer ID downstream for customer-level analysis
    """
    original_len = len(df)

    # Remove non-standard StockCodes
    df = df[~df['StockCode'].isin(NON_STANDARD_CODES)]

    # Remove zero/negative price rows that are not cancellations
    df = df[~((df['Price'] <= 0) & ~df['Invoice'].str.startswith('C', na=False))]

    # Remove null descriptions
    df = df[df['Description'].notna()]

    # Flag outliers but retain
    df = df.copy()
    df['IsOutlier'] = df['Quantity'] > 10000

    df.reset_index(drop=True, inplace=True)

    print("── Cleaning summary ─────────────────────")
    print(f"Rows before: {original_len:,}")
    print(f"Rows after:  {len(df):,}")
    print(f"Removed:     {original_len - len(df):,}")
    print(f"Outlier rows flagged: {df['IsOutlier'].sum()}")
    print(f"─────────────────────────────────────────")

    return df