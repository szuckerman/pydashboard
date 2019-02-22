import pandas as pd
import numpy as np
from pydashboard import components as s
from pydashboard.example_data.example_data import dat
from pydashboard.components import (
    Dimension,
    MultiDimension,
    NamedDimension,
    DATA_COLUMNS,
    VC,
    VE,
    VS,
)
from pydashboard.dc_components import (
    PieChart,
    RowChart,
    ScatterPlot,
    BarChart,
    Label,
    BubbleChart,
)
from pydashboard.dominate_template import dashboard3 as t

dat = pd.read_csv(
    "/Users/zucks/PycharmProjects/pydashboard/pydashboard/example_data/ndx.csv"
)


dat["change"] = dat.close - dat.open

dat.head()

day_list = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


def day_of_week(x):
    y = pd.to_datetime(x)
    return day_list[y.dayofweek]


def gainOrLoss(x):
    if x < 0:
        return "Loss"
    else:
        return "Gain"


dat["fluctuation"] = np.round((dat.close - dat.open) / dat.open * 100)


def get_year(x):
    return x.split("/")[2]


dat["gain"] = dat.change.apply(gainOrLoss)
dat["year"] = dat.date.apply(get_year)
dat["day_of_week"] = dat.date.apply(day_of_week)

gain_dim = Dimension("gain")
# year_dim = Dimension("year")
fluctuation_dim = Dimension("fluctuation")
day_of_week_dim = Dimension("day_of_week")

pie_chart1 = PieChart("A", gain_dim, radius=200, label=Label("percent", precision=2))
pie_chart2 = BarChart(
    "B",
    fluctuation_dim,
    width=400,
    margin_left=50,
    height=350,
    elasticY=True,
    alwaysUseRounding=True,
    gap=1,
    centerBar=True,
)

row_chart = RowChart("B", day_of_week_dim, elasticX=True, height=350, xAxis="ticks(4)")



absGain_eq = (VC("close") - VC("open")) * VC(100)
fluctuation_eq = abs(VC('close') - VC('open'))
sumIndex_eq = (VC('open') + VC('close')) / VC(2)
avgIndex_eq = VC('sumIndex') / VC('count')
percentageGain_eq = (VC('absGain') / VC('avgIndex')) * VC(100)
fluctuationPercentage_eq = (VC('fluctuation') / VC('avgIndex')) * VC(100)

absGain = VS('absGain', absGain_eq)
fluctuation = VS('fluctuation', fluctuation_eq)
sumIndex = VS('sumIndex', sumIndex_eq)
avgIndex = VS('avgIndex', avgIndex_eq)
percentageGain = VS('percentageGain', percentageGain_eq)
fluctuationPercentage = VS('fluctuationPercentage', fluctuationPercentage_eq)

columns = [absGain, fluctuation, sumIndex, avgIndex, percentageGain, fluctuationPercentage]


named_dim = NamedDimension(columns, groupby="year")

str(fluctuation.statement)
str(fluctuation_eq)
str(absGain_eq)
str(avgIndex_eq)

named_dim.reduce_group_code


bub_params = {
    "width": 400,
    "height": 750,
    "x": True,
    "y": True,
    "r": True,
    "colorAccessor": "absGain",
    "keyAccessor": "absGain",
    "valueAccessor": "absGain",
    "radiusValueAccessor": "fluctuationPercentage",
}

bub = BubbleChart("C", named_dim, **bub_params)
str(bub)

dashboard = s.Dashboard(pie_chart1, pie_chart2, bub, data=dat, template=t)

# dashboard.view_outlines()
dashboard.view()

pie_chart1

sumIndex = VC("sumIndex")
count = VC("count")
open = VC("open")
sumIndex + open

abs(open)

absGain_eq = (VC("close") - VC("open")) * VC(100)
fluctuation_eq = abs(VC('close') - VC('open'))
sumIndex_eq = (VC('open') + VC('close'))/VC(2)
avgIndex_eq = VC('sumIndex')/VC('count')
percentageGain_eq = (VC('absGain') /VC('avgIndex')) * VC(100)
fluctuationPercentage_eq = (VC('fluctuation') /VC('avgIndex')) * VC(100)

str(absGain_eq)

my_dict = { 'absGain': absGain_eq,
'fluctuation': fluctuation_eq,
'sumIndex': sumIndex_eq,
'avgIndex': avgIndex_eq,
'percentageGain': percentageGain_eq,
'fluctuationPercentage': fluctuationPercentage_eq}

s.DATA_COLUMNS = {"open", "close"}

for k, v in my_dict.items():
    if isinstance(v, VE) and '/' not in str(v):
        print("p.{k} += {v};".format(k=k, v=str(v)[1:-1]))
    else:
        print("p.{k} += {v};".format(k=k, v=str(v)))

my_dict.keys()

sam=NamedDimension(columns = my_dict, groupby=['year'])

from pprint import pprint as pp
pp(sam.reduce_group_code)