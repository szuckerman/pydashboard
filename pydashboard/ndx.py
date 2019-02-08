import pandas as pd
import numpy as np
from pydashboard import components as s
from pydashboard.example_data.example_data import dat
from pydashboard.components import Dimension, MultiDimension
from pydashboard.dc_components import PieChart, RowChart, ScatterPlot, BarChart
from pydashboard.dominate_template import dashboard3 as t

dat = pd.read_csv('/Users/zucks/PycharmProjects/pydashboard/pydashboard/example_data/ndx.csv')
dat['change'] = dat.close - dat.open

dat.head()

def gainOrLoss(x):
    if x < 0:
        return 'Loss'
    else:
        return 'Gain'


dat['fluctuation'] = np.round((dat.close - dat.open) / dat.open * 100)


def get_year(x):
    return x.split('/')[2]


dat['gain'] = dat.change.apply(gainOrLoss)
dat['year'] = dat.date.apply(get_year)

gain_dim = Dimension('gain')
year_dim = Dimension('year')
fluctuation_dim = Dimension('fluctuation')

pie_chart1 = PieChart("A", gain_dim, radius=200, label=True)
pie_chart2 = BarChart("B", fluctuation_dim, width=400, height=250, elasticY=True, alwaysUseRounding=True, gap=1, centerBar=True)


dashboard = s.Dashboard(pie_chart1, pie_chart2, data=dat, template=t)

# dashboard.view_outlines()
dashboard.view()
