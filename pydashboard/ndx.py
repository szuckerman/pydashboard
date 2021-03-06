from collections import deque

import pandas as pd
import numpy as np
from dominate.tags import *

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
    h2)
from pydashboard.dc_components import (
    PieChart,
    RowChart,
    ScatterPlot,
    BarChart,
    Label,
    BubbleChart,
    ScaleLinear,
    Margin,
    Title,
    HTML, LineChart, Legend)
from pydashboard.dominate_template import ndx_dashboard_noheight as t


def percentage(x):
    return f"percentage({x})"


title = {
    "Index Gain: ": "absGain",
    "Index Gain in Percentage: ": percentage("percentageGain"),
    "Fluctuation / Index Ratio: ": percentage("fluctuationPercentage"),
}


dat = pd.read_csv(
    "/Users/zucks/PycharmProjects/pydashboard/pydashboard/example_data/ndx.csv"
)

dat["change"] = dat.close - dat.open

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


def get_quarter(x):
    month = x.split("/")[0]
    month = int(month)
    if month <= 3:
        return "Q1"
    elif month > 3 and month <= 6:
        return "Q2"
    elif month > 6 and month <= 9:
        return "Q3"
    else:
        return "Q4"


dat.head()
dat["fluctuation"] = np.round((dat.close - dat.open) / dat.open * 100)


def get_year(x):
    return x.split("/")[2]


dat["gain"] = dat.change.apply(gainOrLoss)
dat["year"] = dat.date.apply(get_year)
dat["quarter"] = dat.date.apply(get_quarter)
dat["day_of_week"] = dat.date.apply(day_of_week)

gain_dim = Dimension("gain")
fluctuation_dim = Dimension("fluctuation")
day_of_week_dim = Dimension("day_of_week")
quarter_dim = Dimension("quarter", group="volume", group_type="sum")

gain_loss_chart = PieChart(
    "gain_loss_chart",
    gain_dim,
    radius=80,
    width=180,
    height=180,
    label=Label("percent", precision=0),
)

quarter_chart = PieChart(
    "quarters", quarter_dim, radius=80, inner_radius=30, width=180, height=180
)

fluctuation_chart = BarChart(
    "fluctuation",
    fluctuation_dim,
    width=420,
    height=180,
    elasticY=True,
    gap=1,
    centerBar=True,
    alwaysUseRounding=True,
    round='dc.round.floor',
    margins=Margin(top=10, right=50, bottom=30, left=40),
    xAxis="tickFormat(function(v){return v+'%';})",
    yAxis="ticks(5)",
    x='d3.scaleLinear().domain([-25, 25])',
    filter_printer=True
)

day_of_week_chart = RowChart(
    "day_of_week",
    day_of_week_dim,
    elasticX=True,
    width=180,
    height=180,
    xAxis="ticks(4)",
)

monthDim = Dimension('month', group="volume", group_type='sum', modifier='/500000')

stacked_area_range = BarChart(
    "monthly-volume-chart",
    monthDim,
    width=990,
    height=40,
    elasticY=True,
    alwaysUseRounding=True,
    round='d3.timeMonth.round',
    gap=1,
    centerBar=True,
    xUnits='d3.timeMonths',
    margins=Margin(0, 50, 20, 40),
    renderHorizontalGridLines=False,
    x='d3.scaleTime().domain([new Date(1985, 0, 1), new Date(2012, 11, 31)])'
)

# .margins({top: 0, right: 50, bottom: 20, left: 40})
# .x(d3.scaleTime().domain([new Date(1985, 0, 1), new Date(2012, 11, 31)]))
# .round(d3.timeMonth.round)
# .xUnits(d3.timeMonths);


dat["month"] = pd.to_datetime(dat.date)
dat["month"] = dat.month.dt.month

total_eq = (VC("open") + VC("close")) / VC(2)
total = VS("total", total_eq)



avg_eq = round(VC("total") / VC("count"))
avg = VS("avg", avg_eq)

eqs = [total, avg]

move_months_dim = NamedDimension(
    eqs, groupby=["month"], group_text="Monthly Index Average"
)

str(move_months_dim)

line_chart = LineChart(
    "monthly-move-chart",
    move_months_dim,
    width=990,
    height=200,
    valueAccessor="avg",
    legend=Legend(x=800, y=10, itemHeight=13, gap=5),
    renderArea=True,
    margins=Margin(top=30, right=50, bottom=25, left=40),
    xUnits="d3.timeMonths",
    rangeChart=stacked_area_range
)

dashboard = s.Dashboard(data=dat, template=t)

dashboard.add_graph_title(gain_loss_chart, strong("Days by Gain/Loss"))
dashboard.add_graph_title(quarter_chart, strong("Quarters"))
dashboard.add_graph_title(day_of_week_chart, strong("Day of Week"))
dashboard.add_graph_title(fluctuation_chart, strong("Days by Fluctuation(%)"), display_filter=True)

dashboard.add_graph_title(
    line_chart, strong("Monthly Index Abs Move & Volume/500,000 Chart")
)

# dashboard.view_outlines()

absGain_eq = VC("close") - VC("open")
fluctuation_eq = abs(VC("close") - VC("open"))
sumIndex_eq = (VC("open") + VC("close")) / VC(2)
avgIndex_eq = VC("sumIndex") / VC("count")
percentageGain_eq = (VC("absGain") / VC("avgIndex")) * VC(100)
fluctuationPercentage_eq = (VC("fluctuation2") / VC("avgIndex")) * VC(100)


absGain = VS("absGain", absGain_eq)
fluctuation2 = VS("fluctuation2", fluctuation_eq)
sumIndex = VS("sumIndex", sumIndex_eq)
avgIndex = VS("avgIndex", avgIndex_eq)
percentageGain = VS("percentageGain", percentageGain_eq)
fluctuationPercentage = VS("fluctuationPercentage", fluctuationPercentage_eq)

sumIndex = VS("sumIndex", sumIndex_eq)
avgIndex = VS("avgIndex", avgIndex_eq, fix_zero_division=True)

columns = [sumIndex, avgIndex]

index_avg_by_month_group = NamedDimension(columns, base_dimension=monthDim)

monthDim

columns = [
    absGain,
    fluctuation2,
    sumIndex,
    avgIndex,
    percentageGain,
    fluctuationPercentage,
]

named_dim = NamedDimension(columns, groupby="year")

bub_params = {
    "width": 990,
    "height": 250,
    "x": ScaleLinear([-2500, 2500]),
    "y": ScaleLinear([-100, 100]),
    "r": ScaleLinear([-0, 4000]),
    "colorAccessor": "absGain",
    "keyAccessor": "absGain",
    "valueAccessor": "percentageGain",
    "radiusValueAccessor": "fluctuationPercentage",
    "transitionDuration": 1500,
    "margins": Margin(10, 50, 30, 40),
    "maxBubbleRelativeSize": 0.3,
    "xAxisPadding": 500,
    "yAxisPadding": 100,
    "xAxisLabel": "Index Gain",
    "yAxisLabel": "Index Gain %",
    "label": Label("key"),
    "title": str(Title(title)),
    "yAxis": "tickFormat(function(v){return v + '%';})",
}

bubble_chart = BubbleChart("bubble_chart", named_dim, **bub_params)
str(bubble_chart)

title_name = HTML('title', h2('Nasdaq 100 Index 1985/11/01-2012/06/29'))




dashboard.add_graphs(
    title_name, gain_loss_chart, quarter_chart, fluctuation_chart, day_of_week_chart, bubble_chart,
    stacked_area_range, line_chart
)

# dashboard.view_outlines()
dashboard.view()


#
# my_dict = {
#     "absGain": absGain_eq,
#     "fluctuation": fluctuation_eq,
#     "sumIndex": sumIndex_eq,
#     "avgIndex": avgIndex_eq,
#     "percentageGain": percentageGain_eq,
#     "fluctuationPercentage": fluctuationPercentage_eq,
# }
#
# s.DATA_COLUMNS = {"open", "close"}

# for k, v in my_dict.items():
#     if isinstance(v, VE) and "/" not in str(v):
#         print("p.{k} += {v};".format(k=k, v=str(v)[1:-1]))
#     else:
#         print("p.{k} += {v};".format(k=k, v=str(v)))

# sam = NamedDimension(columns=my_dict, groupby=["year"])
