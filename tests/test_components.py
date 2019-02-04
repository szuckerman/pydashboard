import pytest
from pydashboard import components as s


def test_hello_world():
    assert s.hello_world("sam") == "hello sam!"


def test_make_something_chartelement():
    item = s.ChartElement(id="something", height=100)
    assertion_string = '<div id="something" style="height: 90vh">something</div>'
    assert str(item) == assertion_string


def test_make_something_chartelement_noheightclass():
    item = s.ChartElement("something")
    assert str(item) == '<div id="something">something</div>'


def test_make_square_with_something():
    chart_element = s.ChartElement("something")
    col6 = s.Col6(chart_element)
    row = s.Row(col6)
    assertion_string = """<div class="row"> <div class="col-md-6"> <div id="something">something</div> </div> </div>"""
    output = " ".join(str(row).split())
    # https://stackoverflow.com/questions/2142108/strip-whitespace-in-generated-html-using-pure-python-code
    assert output == assertion_string


def test_make_two_squares_with_something():
    chart_element1 = s.ChartElement("something1")
    chart_element2 = s.ChartElement("something2")
    col6_1 = s.Col6(chart_element1)
    col6_2 = s.Col6(chart_element2)
    item = s.Row([col6_1, col6_2])
    assertion_string = """<div class="row"> <div class="col-md-6"> <div id="something1">something1</div> </div> <div class="col-md-6"> <div id="something2">something2</div> </div> </div>"""
    output = " ".join(str(item).split())
    assert output == assertion_string


def test_print_skeleton_dashboard():
    chart_element = s.ChartElement("something")
    col6 = s.Col6(chart_element)
    item = s.Row(col6)
    dashboard = s.Dashboard(item)
    assertion_string = """<div class="container"><div class="row"> <div class="col-md-6"> <div id="something">something</div> </div> </div></div>"""
    output = " ".join(dashboard.show_chart_outlines().split())
    assert output == assertion_string
