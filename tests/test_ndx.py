import pandas as pd
import pytest
import numpy as np
from pydashboard import components as s
from pydashboard.example_data.example_data import dat
from pydashboard.components import (
    Dimension,
    MultiDimension,
    NamedDimension,
    NamedDimension2,
    DATA_COLUMNS,
    VE,
    VC,
    VS,
)
from pydashboard.dc_components import (
    PieChart,
    RowChart,
    ScatterPlot,
    BarChart,
    BubbleChart,
    Label,
    LineChart,
    Legend,
    Margin,
    ScaleLinear,
    Title,
    HTML)
from pydashboard.dominate_template import dashboard3 as t
from dominate.tags import h2


def compare_strings(s1, s2):
    s1_replaced = str(s1).replace("\n", "").replace(" ", "").replace("\t", "")
    s2_replaced = str(s2).replace("\n", "").replace(" ", "").replace("\t", "")
    return s1_replaced == s2_replaced


def test_absgain_VE_string(monkeypatch):
    monkeypatch.setattr(s, "DATA_COLUMNS", "{'close', 'open'}")
    absGain = (VC("close") - VC("open")) * VC(100)
    expected = "((v.close - v.open) * 100)"
    assert str(absGain) == expected


def test_absgain_VS_string(monkeypatch):
    monkeypatch.setattr(s, "DATA_COLUMNS", "{'close', 'open'}")
    absGain_eq = (VC("close") - VC("open")) * VC(100)
    absGain = VS("absGain", absGain_eq)
    expected = "p.absGain -= (v.close - v.open) * 100;"
    assert str(absGain) == expected


def test_VE_with_abs(monkeypatch):
    monkeypatch.setattr(s, "DATA_COLUMNS", "{'close', 'open'}")
    output = abs(VC("close") - VC("open"))
    assert str(output) == "(Math.abs(v.close - v.open))"


def test_VE_with_constant(monkeypatch):
    monkeypatch.setattr(s, "DATA_COLUMNS", "{'close', 'open'}")
    output = (VC("close") - VC("open")) * VC(100)
    assert str(output) == "((v.close - v.open) * 100)"


def test_VE_with_division(monkeypatch):
    monkeypatch.setattr(s, "DATA_COLUMNS", "{'close', 'open'}")
    output = (VC("open") + VC("close")) / VC(2)
    assert "((v.open + v.close) / 2)" == str(output)


def test_VE_division_p_col(monkeypatch):
    monkeypatch.setattr(s, "DATA_COLUMNS", "{'close', 'open'}")
    output = VC("sumIndex") / VC("count", fix_zero_division=True)
    assert "p.count ? (p.sumIndex / p.count) : 0" == str(output)


def test_ndx_bubble_chart(monkeypatch):
    monkeypatch.setattr(s, "DATA_COLUMNS", "{'close', 'open'}")


def test_nameddimension_VC(monkeypatch):
    monkeypatch.setattr(s, "DATA_COLUMNS", "{'close', 'open'}")
    absGain_eq = (VC("close") - VC("open")) * VC(100)
    fluctuation_eq = abs(VC("close") - VC("open"))
    sumIndex_eq = (VC("open") + VC("close")) / VC(2)
    avgIndex_eq = VC("sumIndex") / VC("count", fix_zero_division=True)
    percentageGain_eq = (VC("absGain") / VC("avgIndex", fix_zero_division=True)) * VC(100)
    fluctuationPercentage_eq = (VC("fluctuation") / VC("avgIndex", fix_zero_division=True)) * VC(100)

    absGain = VS("absGain", absGain_eq)
    fluctuation = VS("fluctuation", fluctuation_eq)
    sumIndex = VS("sumIndex", sumIndex_eq)
    avgIndex = VS("avgIndex", avgIndex_eq)
    percentageGain = VS("percentageGain", percentageGain_eq)
    fluctuationPercentage = VS("fluctuationPercentage", fluctuationPercentage_eq)

    eqs = [
        absGain,
        fluctuation,
        sumIndex,
        avgIndex,
        percentageGain,
        fluctuationPercentage,
    ]

    output = NamedDimension(columns=eqs, groupby=["year"])

    expected = """
            var year_group = year_dimension.group().reduce(
                /* callback for when data is added to the current filter results */
                function (p, v) {
                    ++p.count;
                    p.absGain += (v.close - v.open) * 100;
                    p.fluctuation += Math.abs(v.close - v.open);
                    p.sumIndex += (v.open + v.close) / 2;
                    p.avgIndex = p.count ? (p.sumIndex / p.count) : 0;
                    p.percentageGain = p.avgIndex ? (p.absGain / p.avgIndex) * 100 : 0;
                    p.fluctuationPercentage = p.avgIndex ? (p.fluctuation / p.avgIndex) * 100 : 0;
                    return p;
                },
                /* callback for when data is removed from the current filter results */
                function (p, v) {
                    --p.count;
                    p.absGain -= (v.close - v.open) * 100;
                    p.fluctuation -= Math.abs(v.close - v.open);
                    p.sumIndex -= (v.open + v.close) / 2;
                    p.avgIndex = p.count ? (p.sumIndex / p.count) : 0;
                    p.percentageGain = p.avgIndex ? (p.absGain / p.avgIndex) * 100 : 0;
                    p.fluctuationPercentage = p.avgIndex ? (p.fluctuation / p.avgIndex) * 100 : 0;
                    return p;
                },
                /* initialize p */
                function () {
                    return {
                        count: 0,
                        absGain: 0,
                        fluctuation: 0,
                        sumIndex: 0,
                        avgIndex: 0,
                        percentageGain: 0,
                        fluctuationPercentage: 0
                    };
                }
    );"""

    assert str(output).replace("\n", "").replace(" ", "").replace("\t", "") == str(expected).replace("\n", "").replace(" ", "").replace("\t", "")


def test_gainOrLossChart(ndx):
    def gainOrLoss(x):
        if x < 0:
            return "Loss"
        else:
            return "Gain"

    dat = ndx
    dat["change"] = dat.close - dat.open
    dat["gainOrLoss"] = dat.change.apply(gainOrLoss)
    gainOrLoss_dim = Dimension("gainOrLoss")

    gainOrLossChart = PieChart(
        "gain-loss-chart",
        gainOrLoss_dim,
        width=180,
        height=180,
        radius=80,
        inner_radius=40,
        renderLabel=True,
        label=Label("percent", precision=0),
        transitionDuration=500,
        colors=["#3182bd", "#6baed6", "#9ecae1", "#c6dbef", "#dadaeb"],
        colorDomain=[-1750, 1644],
        colorAccessor=True,
    )

    dc_documentation_string = """
    var pie_chart_gain_loss_chart = dc.pieChart("#gain-loss-chart")
            .width(180)
            .height(180)
            .radius(80) 
            .dimension(gainOrLoss_dimension)
            .group(gainOrLoss_group)
            .renderLabel(true) 
            .innerRadius(40) 
            .transitionDuration(500) 
            .colors(['#3182bd', '#6baed6', '#9ecae1', '#c6dbef', '#dadaeb']) 
            .colorDomain([-1750, 1644]) 
            .colorAccessor(function(d, i){return d.value;});

    pie_chart_gain_loss_chart.label(function (d) {
                if (pie_chart_gain_loss_chart.hasFilter() && !pie_chart_gain_loss_chart.hasFilter(d.key)) {
                    return d.key + '(0%)';
                }
                var label = d.key;
                if (all.value()) {
                    label += '(' + Math.floor(d.value / all.value() * 100)/1 + '%)';
                }
                return label;
            });
            """

    gainOrLossChart_replaced = (
        str(gainOrLossChart).replace("\n", "").replace(" ", "").replace("\t", "")
    )
    dc_documentation_string_replaced = (
        str(dc_documentation_string)
        .replace("\n", "")
        .replace(" ", "")
        .replace("\t", "")
    )

    assert gainOrLossChart_replaced == dc_documentation_string_replaced


def test_dayOfWeekChart(ndx):
    def day_of_week(x):
        y = pd.to_datetime(x)
        return day_list[y.dayofweek]

    dat = ndx

    day_list = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    dat["day_of_week"] = dat.date.apply(day_of_week)
    day_of_week_dim = Dimension("day_of_week")
    row_chart = RowChart(
        "day-of-week-chart",
        day_of_week_dim,
        elasticX=True,
        height=180,
        width=180,
        xAxis="ticks(4)",
        label=Label("key", part=0),
    )

    dc_documentation_string = """
        var row_chart_day_of_week_chart = dc.rowChart("#day-of-week-chart")
            .width(180)
            .height(180)
            .margins({top: 20, left: 10, right: 10, bottom: 20})
            .group(day_of_week_group)
            .dimension(day_of_week_dimension)
            .ordinalColors(['#3182bd', '#6baed6', '#9ecae1', '#c6dbef', '#dadaeb'])
            .title(function (d) {
                return d.value;
            })
            .elasticX(true)
            .label(function (d) {
                return d.key[0];
            });
            
        row_chart_day_of_week_chart.xAxis().ticks(4);
        
    """

    row_chart_replaced = (
        str(row_chart).replace("\n", "").replace(" ", "").replace("\t", "")
    )
    dc_documentation_string_replaced = (
        str(dc_documentation_string)
        .replace("\n", "")
        .replace(" ", "")
        .replace("\t", "")
    )

    assert row_chart_replaced == dc_documentation_string_replaced


def test_fluctuationChart(ndx):
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
        round='dc.round.floor',
        margins = Margin(top=10, right=50, bottom=30, left=40),
        xAxis="tickFormat(function(v){return v+'%';})",
        yAxis="ticks(5)",
        x='d3.scaleLinear().domain([-25, 25])',
        filter_printer=True
    )

    dc_documentation_string = """
    var bar_chart_volume_month_chart = dc.barChart("#volume-month-chart")
        .width(420)
        .height(180)
        .margins({top: 10, right: 50, bottom: 30, left: 40})
        .dimension(fluctuation_dimension)
        .group(fluctuation_group)
        .elasticY(true)
        .centerBar(true)
        .gap(1)
        .round(dc.round.floor)
        .alwaysUseRounding(true)
        .renderHorizontalGridLines(true)
        .x(d3.scaleLinear().domain([-25, 25]))
        .filterPrinter(function (filters) {
            var filter = filters[0], s = '';
            s += numberFormat(filter[0]) + '% -> ' + numberFormat(filter[1]) + '%';
            return s;
        });
        
    bar_chart_volume_month_chart.xAxis().tickFormat(
        function (v) { return v + '%'; });
    
    bar_chart_volume_month_chart.yAxis().ticks(5);
    """

    row_chart_replaced = (
        str(fluctuation_chart).replace("\n", "").replace(" ", "").replace("\t", "")
    )
    dc_documentation_string_replaced = (
        str(dc_documentation_string)
        .replace("\n", "")
        .replace(" ", "")
        .replace("\t", "")
    )

    assert row_chart_replaced == dc_documentation_string_replaced


def test_moveChart(monkeypatch, ndx):
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
        legend=Legend(x=800, y=10, itemHeight=13, gap=5),
        renderArea=True,
        margins=Margin(top=30, right=50, bottom=25, left=40),
        xUnits="d3.timeMonths",
    )

    dc_documentation_string = """
    var line_chart_monthly_move_chart = dc.lineChart("#monthly-move-chart")
        .renderArea(true)
        .width(990)
        .height(200)
        .transitionDuration(1000)
        .margins({top: 30, right: 50, bottom: 25, left: 40})
        .dimension(month_dimension)
        .mouseZoomable(true)
        .rangeChart(volumeChart)
        .x(d3.scaleTime().domain([new Date(1985, 0, 1), new Date(2012, 11, 31)]))
        .round(d3.timeMonth.round)
        .xUnits(d3.timeMonths)
        .elasticY(true)
        .renderHorizontalGridLines(true)
        .legend(dc.legend().x(800).y(10).itemHeight(13).gap(5))
        .brushOn(false) 
        .group(month_group, 'Monthly Index Average')
        .valueAccessor(function (d) {
            return d.value.avg;
        }) 
        .stack(monthlyMoveGroup, 'Monthly Index Move', function (d) {
            return d.value;
        })
        .title(function (d) {
            var value = d.value.avg ? d.value.avg : d.value;
            if (isNaN(value)) {
                value = 0;
            }
            return dateFormat(d.key) + numberFormat(value);
        });
    """

    line_chart_replaced = (
        str(line_chart).replace("\n", "").replace(" ", "").replace("\t", "")
    )
    dc_documentation_string_replaced = (
        str(dc_documentation_string)
        .replace("\n", "")
        .replace(" ", "")
        .replace("\t", "")
    )

    assert line_chart_replaced == dc_documentation_string_replaced


def test_bar_chart_attributes(bar_chart):
    bar_chart_attributes_set = {
        "name",
        "dimension",
        "alwaysUseRounding",
        "barPadding",
        "centerBar",
        "gap",
        "outerPadding",
        "xAxis",
        "yAxis",
    }

    for col in bar_chart_attributes_set:
        assert hasattr(bar_chart, col)


def test_round_and_division_VS():
    avg_div = VC("total") / VC("count", fix_zero_division=True)
    avg_eq = round(avg_div)
    avg = VS("avg", avg_eq)

    expected_avg_div = 'p.count ? (p.total / p.count) : 0'
    expected_avg_eq = '(Math.round(p.count ? (p.total / p.count) : 0))'
    expected_avg = 'p.avg = Math.round(p.count ? (p.total / p.count) : 0);'

    assert str(avg_div) == expected_avg_div
    assert str(avg_eq) == expected_avg_eq
    assert str(avg) == expected_avg


def test_avg_index_eq():

    avgIndex_eq = VC("sumIndex") / VC("count", fix_zero_division=True)
    avgIndex = VS("avgIndex", avgIndex_eq)

    expected_eq = 'p.count ? (p.sumIndex / p.count) : 0'
    expected = 'p.avgIndex = p.count ? (p.sumIndex / p.count) : 0;'

    assert expected_eq == str(avgIndex_eq)
    assert expected == str(avgIndex)


def test_move_months_dim(monkeypatch, ndx):
    monkeypatch.setattr(s, "DATA_COLUMNS", "{'close', 'open'}")

    expected = '''
    var month_group = month_dimension.group().reduce(
        function (p, v) {
            ++p.days;
            p.total += (v.open + v.close) / 2;
            p.avg = Math.round(p.total / p.days);
            return p;
        },
        function (p, v) {
            --p.days;
            p.total -= (v.open + v.close) / 2;
            p.avg = p.days ? Math.round(p.total / p.days) : 0;
            return p;
        },
        function () {
            return {days: 0, total: 0, avg: 0};
        }
    );
    '''

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

    compare_strings(str(move_months_dim), expected)


def test_line_chart_attributes(line_chart):
    line_chart_attributes_set = {
        "name",
        "dimension",
        "transitionDuration",
        "elasticY",
        "renderHorizontalGridLines",
    }

    for col in line_chart_attributes_set:
        assert hasattr(line_chart, col)


def test_legend():
    legend = Legend(x=800, y=10, itemHeight=13, gap=5)
    assert str(legend) == f"dc.legend().x(800).y(10).itemHeight(13).gap(5)"


def test_margin():
    margin = Margin(top=30, right=50, bottom=25, left=40)
    assert str(margin) == "{top:30,right:50,bottom:25,left:40}"


def test_bubble_chart(monkeypatch, ndx):
    monkeypatch.setattr(s, "DATA_COLUMNS", "{'close', 'open'}")

    dat = ndx

    absGain_eq = (VC("close") - VC("open")) * VC(100)
    fluctuation_eq = abs(VC("close") - VC("open"))
    sumIndex_eq = (VC("open") + VC("close")) / VC(2)
    avgIndex_eq = VC("sumIndex") / VC("count")
    percentageGain_eq = (VC("absGain") / VC("avgIndex")) * VC(100)
    fluctuationPercentage_eq = (VC("fluctuation") / VC("avgIndex")) * VC(100)

    absGain = VS("absGain", absGain_eq)
    fluctuation = VS("fluctuation2", fluctuation_eq)
    sumIndex = VS("sumIndex", sumIndex_eq)
    avgIndex = VS("avgIndex", avgIndex_eq)
    percentageGain = VS("percentageGain", percentageGain_eq)
    fluctuationPercentage = VS("fluctuationPercentage", fluctuationPercentage_eq)

    columns = [
        absGain,
        fluctuation,
        sumIndex,
        avgIndex,
        percentageGain,
        fluctuationPercentage,
    ]

    # my_dict = {
    #     "absGain": absGain_eq,
    #     "fluctuation": fluctuation_eq,
    #     "sumIndex": sumIndex_eq,
    #     "avgIndex": avgIndex_eq,
    #     "percentageGain": percentageGain_eq,
    #     "fluctuationPercentage": fluctuationPercentage_eq,
    # }

    bubble_named_dimension = NamedDimension(columns=columns, groupby=["year"])

    def percentage(x):
        return f"percentage({x})"

    title = {
        "Index Gain: ": "absGain",
        "Index Gain in Percentage: ": percentage("percentageGain"),
        "Fluctuation / Index Ratio: ": percentage("fluctuationPercentage"),
    }

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
        "yAxis": "tickFormat(function(v){return v+'%';})",
    }

    bubble_chart = BubbleChart(
        "yearly-bubble-chart", bubble_named_dimension, **bub_params
    )

    dc_documentation_string = r"""
        var bubble_chart_yearly_bubble_chart = dc.bubbleChart("#yearly-bubble-chart")
            .width(990) 
            .height(250)
            .transitionDuration(1500)
            .margins({top: 10, right: 50, bottom: 30, left: 40})
            .dimension(year_dimension)
            .group(year_group)
            .colors(d3.schemeRdYlGn[9])
            .colorDomain([-500, 500]) 
            .colorAccessor(function (d) {
                return d.value.absGain;
            })
            .keyAccessor(function (d) {
                return d.value.absGain;
            })
            .valueAccessor(function (d) {
                return d.value.percentageGain;
            })
            .radiusValueAccessor(function (d) {
                return d.value.fluctuationPercentage;
            })
            .maxBubbleRelativeSize(0.3)
            .x(d3.scaleLinear().domain([-2500, 2500]))
            .y(d3.scaleLinear().domain([-100, 100]))
            .r(d3.scaleLinear().domain([0, 4000]))
            .elasticX(true) 
            .elasticY(true)
            .xAxisPadding(500) 
            .yAxisPadding(100)
            .renderHorizontalGridLines(true) 
            .renderVerticalGridLines(true) 
            .xAxisLabel('Index Gain') 
            .yAxisLabel('Index Gain %') 
            .renderLabel(true)
            .label(function (d) {
                return d.key;
            }) 
            .renderTitle(true)
            .title(function (d) {
                return [
                    d.key,
                    'Index Gain: ' + numberFormat(d.value.absGain),
                    'Index Gain in Percentage: ' + numberFormat(d.value.percentageGain) + '%',
                    'Fluctuation / Index Ratio: ' + numberFormat(d.value.fluctuationPercentage) + '%'].join('\n')
            });
            
            bubble_chart_yearly_bubble_chart.yAxis()
            .tickFormat(function (v) {
                return v + '%';
            });
        """

    bubble_chart_replaced = (
        str(bubble_chart).replace("\n", "").replace(" ", "").replace("\t", "")
    )

    dc_documentation_string_replaced = (
        str(dc_documentation_string)
        .replace("\n", "")
        .replace(" ", "")
        .replace("\t", "")
    )

    assert bubble_chart_replaced == dc_documentation_string_replaced


def test_make_html():
    title_name = HTML('title', h2('Nasdaq 100 Index 1985/11/01-2012/06/29'))
    assert title_name.html_string == '<h2>Nasdaq 100 Index 1985/11/01-2012/06/29</h2>'


def test_volume_chart():
    monthDim = Dimension('month', group="volume", group_type='sum', modifier='/500000')

    stacked_area_range = BarChart(
        "stacked_area_range",
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

    expected = '''var bar_chart_stacked_area_range = dc.barChart("#stacked_area_range")
        .width(990)
        .height(40)
        .margins({top: 0, right: 50, bottom: 20, left: 40})
        .dimension(month_dimension)
        .group(month_group)
        .elasticY(true)
        .centerBar(true)
        .gap(1)
        .round(d3.timeMonth.round)
        .xUnits(d3.timeMonths)
        .alwaysUseRounding(true)
        .x(d3.scaleTime().domain([new Date(1985, 0, 1), new Date(2012, 11, 31)]));
        '''

    assert str(stacked_area_range).replace("\n", "").replace(" ", "").replace("\t", "") == str(expected).replace("\n", "").replace(" ", "").replace("\t", "")