from src.analysis.customers import calc_cohort_period_table, calc_one_time_buyers, calc_rfm, generate_retention_matrix, revenue_by_top_n_perc


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


def test_no_negative_period(cleaned_df):
    """No period should be negative"""
    cohort_data = calc_cohort_period_table(cleaned_df)
    assert cohort_data['Period'].min() >= 0


def test_cohort_period_shape(cleaned_df):
    """Table should have Cohort, Period and Customers columns, period starts at 0."""
    cohort_data = calc_cohort_period_table(cleaned_df)
    assert list(cohort_data.columns) == ['Cohort', 'Period', 'Customers']
    assert cohort_data['Period'].min() == 0

def test_retention_matrix(cleaned_df):
    cohort_data = calc_cohort_period_table(cleaned_df)
    retention_matrix = generate_retention_matrix(cohort_data)
    assert retention_matrix.min().min() >= 0
    assert retention_matrix.max().max() <= 100

def test_retention_period_zero_is_100(cleaned_df):
    """Period 0 should always be 100% before first cohort is dropped."""
    cohort_data = calc_cohort_period_table(cleaned_df)
    cohort_matrix = cohort_data.pivot_table(index='Cohort', columns='Period', values='Customers')
    cohort_size = cohort_matrix[0]
    raw_retention = cohort_matrix.divide(cohort_size, axis=0) * 100
    assert (raw_retention[0] == 100.0).all()

def test_one_time_buyer_rate_range(cleaned_df):
    """One time buyer rate should be between 0 and 100."""
    rfm = calc_rfm(cleaned_df)
    result = calc_one_time_buyers(rfm)
    assert 0 <= result['one_time_rate'] <= 100

def test_one_time_buyers(cleaned_df):
    rfm = calc_rfm(cleaned_df)
    one_time_buyer_stat = calc_one_time_buyers(rfm)
    assert one_time_buyer_stat['total_customers'] > one_time_buyer_stat['one_time_count']