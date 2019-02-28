import pytest
import pandas as pd
import numpy as np

from pydashboard import components as s
from pydashboard.components import Dimension, NamedDimension, VC, VS
from pydashboard.dc_components import BarChart, LineChart


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


@pytest.fixture
def line_chart(monkeypatch, ndx):
    monkeypatch.setattr(s, "DATA_COLUMNS", "{'close', 'open'}")

    dat = ndx

    def get_month(x):
        return x.month

    dat["month"] = pd.to_datetime(dat.date)
    dat["month"] = dat.month.apply(get_month)

    total_eq = (VC("open") + VC("close")) / VC(2)
    total = VS("total", total_eq)

    avg_eq = round(VC("total") / VC("count"))
    avg = VS("avg", avg_eq)

    eqs = [total, avg]

    move_months_dim = NamedDimension(
        eqs, groupby=["month"], group_text="Monthly Index Average"
    )

    line_chart = LineChart(
        "monthly-move-chart",
        move_months_dim,
        width=990,
        height=200,
        valueAccessor="avg",
    )

    return line_chart