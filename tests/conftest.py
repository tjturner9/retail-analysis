import pytest
from src.load import load_data
from src.clean import clean_data


@pytest.fixture(scope="module")
def cleaned_df():
    df_raw = load_data()
    return clean_data(df_raw)