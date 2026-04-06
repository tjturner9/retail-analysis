from src.analysis.revenue import calc_revenue, calculate_monthly_breakdown

def test_calc_revenue(cleaned_df):
    result = calc_revenue(cleaned_df)
    # Net revenue should be less than gross
    assert result['net_revenue'] < result['gross_revenue']
    # Cancellation revenue should be negative
    assert result['cancellation_revenue'] < 0
    # Cancellation rate should be a small percentage, not zero
    assert 0 < result['cancellation_rate'] < 20
    # All values should be positive except cancellation_revenue
    assert result['gross_revenue'] > 0
    assert result['net_revenue'] > 0

def test_monthly_breakdown(cleaned_df):
    result = calculate_monthly_breakdown(cleaned_df)
    assert len(result) == 25
    assert list(result.columns) == ['Month', 'Gross Revenue', 'Cancellations', 'Net Revenue', 'Cancellation Rate']
    assert result['Month'].iloc[0] == '2009-12'
    # Net should always be less than gross
    assert (result['Net Revenue'] <= result['Gross Revenue']).all()
    # Cancellation rates should be positive
    assert (result['Cancellation Rate'] >= 0).all()