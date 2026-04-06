import pytest
from src.load import load_data
from src.clean import clean_data


@pytest.fixture(scope="module")
def cleaned_df():
    df_raw = load_data()
    return clean_data(df_raw)


def test_row_count(cleaned_df):
    """Cleaning should remove ~11k rows, not more."""
    assert len(cleaned_df) == 1_021_374


def test_no_non_standard_codes(cleaned_df):
    """Non-standard StockCodes should be fully removed."""
    non_standard = {'POST', 'DOT', 'M', 'D', 'S', 'C2', 'B', 'BANK CHARGES', 'AMAZONFEE', 'ADJUST'}
    assert not cleaned_df['StockCode'].isin(non_standard).any()


def test_no_negative_prices_outside_cancellations(cleaned_df):
    """No negative prices on non-cancellation rows."""
    non_cancel = cleaned_df[~cleaned_df['Invoice'].str.startswith('C')]
    assert (non_cancel['Price'] >= 0).all()


def test_no_null_descriptions(cleaned_df):
    """All descriptions should be populated after cleaning."""
    assert cleaned_df['Description'].notna().all()


def test_outlier_flag_exists(cleaned_df):
    """IsOutlier column should exist and flag at least one row."""
    assert 'IsOutlier' in cleaned_df.columns
    assert cleaned_df['IsOutlier'].sum() > 0


def test_customer_id_dtype(cleaned_df):
    """Customer ID should be nullable integer type."""
    assert str(cleaned_df['Customer ID'].dtype) == 'Int64'