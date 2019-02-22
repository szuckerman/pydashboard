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
    Label,
    BubbleChart,
)
from pydashboard.dominate_template import dashboard3 as t

def compare_strings(s1,s2):
    s1_replaced = str(s1).replace('\n', '').replace(' ', '').replace('\t', '')
    s2_replaced = str(s2).replace('\n', '').replace(' ', '').replace('\t', '')
    return list(s1_replaced) == list(s2_replaced)

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
    output = abs(VC('close') - VC('open'))
    assert str(output) == '(Math.abs(v.close - v.open))'


def test_VE_with_constant(monkeypatch):
    monkeypatch.setattr(s, "DATA_COLUMNS", "{'close', 'open'}")
    output = (VC("close") - VC("open")) * VC(100)
    assert str(output) == '((v.close - v.open) * 100)'


def test_VE_with_division(monkeypatch):
    monkeypatch.setattr(s, "DATA_COLUMNS", "{'close', 'open'}")
    output = (VC('open') + VC('close')) / VC(2)
    assert  '((v.open + v.close) / 2)' == str(output)


def test_VE_division_p_col(monkeypatch):
    monkeypatch.setattr(s, "DATA_COLUMNS", "{'close', 'open'}")
    output = VC('sumIndex') / VC('count')
    assert 'p.count ? (p.sumIndex / p.count)' == str(output)


def test_nameddimension_VC(monkeypatch):
    monkeypatch.setattr(s, "DATA_COLUMNS", "{'close', 'open'}")
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

    eqs = [absGain, fluctuation, sumIndex, avgIndex, percentageGain, fluctuationPercentage]

    output = NamedDimension(columns=eqs, groupby=['year'])

    expected = '''
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
    );'''

    assert compare_strings(output, expected)
