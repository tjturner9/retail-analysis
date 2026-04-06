import os
import kagglehub
import pandas as pd
from datetime import datetime


def load_data(include_cancellations: bool = True, keep_na: bool = True) -> pd.DataFrame:
    """
    Load the UCI Online Retail II dataset via kagglehub.

    Parameters
    ----------
    include_cancellations : bool
        If False, removes all invoices with a 'C' prefix.
    keep_na : bool
        If False, drops rows with a null Customer ID.

    Returns
    -------
    pd.DataFrame
    """
    path = kagglehub.dataset_download("mashlyn/online-retail-ii-uci")
    file_path = os.path.join(path, "online_retail_II.csv")

    df = pd.read_csv(file_path)

    # Type coercion
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['Customer ID'] = pd.to_numeric(df['Customer ID'], errors='coerce').astype('Int64')
    df['TotalPrice'] = df['Quantity'] * df['Price']

    # Remove test stock codes
    df = df[~df['StockCode'].str.startswith('TEST', na=False)]

    # Remove duplicates
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)

    if not include_cancellations:
        df = df[~df['Invoice'].str.startswith('C', na=False)]

    if not keep_na:
        df = df.dropna(subset=['Customer ID'])
        df['Customer ID'] = df['Customer ID'].astype('Int64')

    # Sanity checks
    assert df['InvoiceDate'].gt(datetime(2009, 1, 1)).all(), "Date range check failed — lower bound"
    assert df['InvoiceDate'].lt(datetime(2012, 1, 1)).all(), "Date range check failed — upper bound"

    # Profile
    print("── Data loaded ──────────────────────────")
    print(f"Rows:              {len(df):,}")
    print(f"Date range:        {df['InvoiceDate'].min().date()} → {df['InvoiceDate'].max().date()}")
    print(f"Unique customers:  {df['Customer ID'].nunique():,}")
    print(f"Cancellations:     {df['Invoice'].str.startswith('C').sum():,}")
    print(f"Null Customer IDs: {df['Customer ID'].isna().sum():,}")
    print(f"─────────────────────────────────────────")

    return df