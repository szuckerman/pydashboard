import pytest
import pandas as pd


@pytest.fixture(scope="session")
def ndx():
    return pd.read_csv("../pydashboard/example_data/ndx.csv")
