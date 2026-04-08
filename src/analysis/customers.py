from src.load import load_data
from src.clean import clean_data
import pandas as pd


def calc_rfm(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculated a rfm table.
    - Recency — how recently did they last buy? Recent buyers are more valuable.
    - Frequency — how many times have they bought? Loyal customers matter.
    - Monetary — how much have they spent in total? Revenue concentration lives here.

    Returns
    -------
    dataframe of the table with columns: CustomerID, Recency, Frequency, Monetary, R_rank_norm,
    F_rank_norm, M_rank_norm, RFM_Score
    """


    no_guest_df = df[df['Customer ID'].notna()]
    no_guest_sales = no_guest_df[~no_guest_df['Invoice'].str.startswith('C')]

    df_recency = no_guest_sales.groupby(by='Customer ID', as_index=False)['InvoiceDate'].max()
    df_recency.columns = ['CustomerID', 'LastPurchaseDate']
    recent_date = df_recency['LastPurchaseDate'].max()
    df_recency['Recency'] = df_recency['LastPurchaseDate'].apply(lambda x: (recent_date - x).days)

    frequency_df = no_guest_sales.groupby(by=['Customer ID'], as_index=False)['Invoice'].count()
    frequency_df.columns = ['CustomerID', 'Frequency']

    monetary_df = no_guest_df.groupby(by='Customer ID', as_index=False)['TotalPrice'].sum()
    monetary_df.columns = ['CustomerID', 'Monetary']

    rf_df = df_recency.merge(frequency_df, on='CustomerID')
    rfm_df = rf_df.merge(monetary_df, on='CustomerID').drop(columns='LastPurchaseDate')

    rfm_df['R_rank'] = rfm_df['Recency'].rank(ascending=False)
    rfm_df['F_rank'] = rfm_df['Frequency'].rank(ascending=True)
    rfm_df['M_rank'] = rfm_df['Monetary'].rank(ascending=True)

    rfm_df['R_rank_norm'] = (rfm_df['R_rank'] / rfm_df['R_rank'].max())
    rfm_df['F_rank_norm'] = (rfm_df['F_rank'] / rfm_df['F_rank'].max())
    rfm_df['M_rank_norm'] = (rfm_df['M_rank'] / rfm_df['M_rank'].max())

    rfm_df.drop(columns=['R_rank', 'F_rank', 'M_rank'], inplace=True)

    rfm_df['R_rank_quart'] = pd.qcut(rfm_df['R_rank_norm'], 4, labels=False) + 1
    rfm_df['F_rank_quart'] = pd.qcut(rfm_df['F_rank_norm'], 4, labels=False) + 1
    rfm_df['M_rank_quart'] = pd.qcut(rfm_df['M_rank_norm'], 4, labels=False) + 1

    rfm_df['RFM_Score'] = rfm_df['R_rank_quart'] + rfm_df['F_rank_quart'] + rfm_df['M_rank_quart']

    return rfm_df


def revenue_by_top_n_perc(n_percent, rfm_df: pd.DataFrame, df: pd.DataFrame):
    top_customers = list(rfm_df[rfm_df['RFM_Score'] >= rfm_df['RFM_Score'].quantile(1 - (n_percent/100))]['CustomerID'])
    top_customers_df = df[df["Customer ID"].isin(top_customers)]

    return top_customers_df['TotalPrice'].sum()