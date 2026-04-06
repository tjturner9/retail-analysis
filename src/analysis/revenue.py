import pandas as pd


def _split_cancellations(df: pd.DataFrame):
    """Split dataframe into sales and cancellation invoices."""
    cancellations = df[df['Invoice'].str.startswith('C', na=False)]
    sales = df[~df['Invoice'].str.startswith('C', na=False)]
    return sales, cancellations


def calc_revenue(df: pd.DataFrame) -> dict:
    """
    Calculate gross, cancellation and net revenue from cleaned dataframe.

    Returns
    -------
    dict with keys: gross_revenue, cancellation_revenue, net_revenue, cancellation_rate
    """
    sales, cancellations = _split_cancellations(df)
    gross_revenue = sales['TotalPrice'].sum()
    cancellation_revenue = cancellations['TotalPrice'].sum()
    net_revenue = gross_revenue + cancellation_revenue
    return {
        'gross_revenue': gross_revenue,
        'cancellation_revenue': cancellation_revenue,
        'net_revenue': net_revenue,
        'cancellation_rate': abs(cancellation_revenue) / gross_revenue * 100
    }


def calculate_monthly_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate gross revenue, cancellations, net revenue and cancellation
    rate by month.

    Returns
    -------
    pd.DataFrame with columns: Month, Gross Revenue, Cancellations,
    Net Revenue, Cancellation Rate
    """
    sales, cancellations = _split_cancellations(df)

    sales_by_month = (
        sales
        .groupby(sales['InvoiceDate'].dt.strftime('%Y-%m'))['TotalPrice']
        .sum()
        .reset_index()
        .rename(columns={'InvoiceDate': 'Month', 'TotalPrice': 'Gross Revenue'})
    )

    cancellation_by_month = (
        cancellations
        .groupby(cancellations['InvoiceDate'].dt.strftime('%Y-%m'))['TotalPrice']
        .sum()
        .reset_index()
        .rename(columns={'InvoiceDate': 'Month', 'TotalPrice': 'Cancellations'})
    )

    totals_by_month = sales_by_month.merge(cancellation_by_month, on='Month')
    totals_by_month['Net Revenue'] = (
        totals_by_month['Gross Revenue'] + totals_by_month['Cancellations']
    )
    totals_by_month['Cancellation Rate'] = (
        abs(totals_by_month['Cancellations']) / totals_by_month['Gross Revenue'] * 100
    ).round(2)

    return totals_by_month