"""
shape
column names
cancellation rate values
sort order

"""
from src.analysis.products import calc_product_cancellation_rates


def test_rfm_shape(cleaned_df):
    """products table should have one row per product with a Description."""
    products = calc_product_cancellation_rates(cleaned_df)
    assert products['Description'].nunique() == len(products)
    assert products['Description'].notna().all()


def test_rfm_columns(cleaned_df):
    """RFM table should have expected columns."""
    rfm = calc_product_cancellation_rates(cleaned_df)
    expected = ['CustomerID', 'Recency', 'Frequency', 'Monetary',
                'R_rank_norm', 'F_rank_norm', 'M_rank_norm',
                'R_rank_quart', 'F_rank_quart', 'M_rank_quart', 'RFM_Score']
    assert list(rfm.columns) == expected
