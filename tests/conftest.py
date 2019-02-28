import pytest
import pandas as pd
import numpy as np

from pydashboard.components import Dimension
from pydashboard.dc_components import BarChart


@pytest.fixture(scope="session")
def ndx():
    return pd.read_csv("../pydashboard/example_data/ndx.csv")

@pytest.fixture
def bar_chart(ndx):
    dat = ndx

    dat["fluctuation"] = np.round((dat.close - dat.open) / dat.open * 100)

    fluctuation_dim = Dimension("fluctuation")

    fluctuation_chart = BarChart(
        "volume-month-chart",
        fluctuation_dim,
        width=420,
        height=180,
        elasticY=True,
        gap=1,
        centerBar=True,
        alwaysUseRounding=True,
        xAxis="tickFormat(function(v){return v+'%';})",
        yAxis="ticks(5)",
    )

    return fluctuation_chart

