from src.analysis.customers import calc_rfm, revenue_by_top_n_perc


def test_rfm_shape(cleaned_df):
    """RFM table should have one row per customer with a Customer ID."""
    rfm = calc_rfm(cleaned_df)
    assert rfm['CustomerID'].nunique() == len(rfm)
    assert rfm['CustomerID'].notna().all()


def test_rfm_columns(cleaned_df):
    """RFM table should have expected columns."""
    rfm = calc_rfm(cleaned_df)
    expected = ['CustomerID', 'Recency', 'Frequency', 'Monetary',
                'R_rank_norm', 'F_rank_norm', 'M_rank_norm',
                'R_rank_quart', 'F_rank_quart', 'M_rank_quart', 'RFM_Score']
    assert list(rfm.columns) == expected


def test_rfm_scores_in_range(cleaned_df):
    """RFM scores should be between 3 and 12."""
    rfm = calc_rfm(cleaned_df)
    assert rfm['RFM_Score'].min() >= 3
    assert rfm['RFM_Score'].max() <= 12


def test_no_negative_recency(cleaned_df):
    """Recency should never be negative."""
    rfm = calc_rfm(cleaned_df)
    assert (rfm['Recency'] >= 0).all()


def test_revenue_by_top_20(cleaned_df):
    """Top 20% of customers should generate majority of revenue."""
    rfm = calc_rfm(cleaned_df)
    result = revenue_by_top_n_perc(20, rfm, cleaned_df)
    assert result['customer_count'] == 1170
    assert result['revenue_share'] > 70
    assert result['revenue_share'] < 100


def test_revenue_share_increases_with_percentile(cleaned_df):
    """Revenue share should increase as we include more customers."""
    rfm = calc_rfm(cleaned_df)
    result_10 = revenue_by_top_n_perc(10, rfm, cleaned_df)
    result_20 = revenue_by_top_n_perc(20, rfm, cleaned_df)
    result_30 = revenue_by_top_n_perc(30, rfm, cleaned_df)
    assert result_10['revenue_share'] < result_20['revenue_share'] < result_30['revenue_share']