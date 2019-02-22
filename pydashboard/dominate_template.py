from dominate.tags import *
from pydashboard import components as c

template1 = div(cls="container")
template1_row1 = template1.add(div(cls="row"))
template1_row2 = template1.add(div(cls="row"))

template1_row1.add(div(cls="col-md-6", id="A"))
template1_row1.add(div(cls="col-md-6", id="B"))

template1_row2.add(div(cls="col-md-4", id="C"))
template1_row2.add(div(cls="col-md-4", id="D"))
template1_row2.add(div(cls="col-md-4", id="E"))
# row2.add(div(cls='col-md-4', id='D'))
# row2.add(div(cls='col-md-4', id='E'))


template2 = div(cls="container")
template2_row1 = template2.add(div(cls="row"))

template2_row1.add(div(cls="col-md-12", id="A"))

# Splitting on columns splits the width in half
# Splitting on rows splits the height in half

cola = c.Col6(id="A", height=50)
colb = c.Col6(id="C", height=50)
colc = c.Col6(id="D", height=50)
cold = c.Col6(id="E", height=50)

rowa = c.Row([cola, colb])
rowb = c.Row([colc, cold])

col1 = c.Col6([rowa, rowb])
col2 = c.Col6(id="B", height=100)

row1 = c.Row([col2, col1])

dashboard = c.Container(row1)


A = c.Col4(id="A", height=33)
B = c.Col4(id="B", height=33)
C = c.Col4(id="C", height=33)
D = c.Col4(id="D", height=33)
E = c.Col4(id="E", height=33)
F = c.Col4(id="F", height=33)
G = c.Col4(id="G", height=33)
H = c.Col4(id="H", height=33)
I = c.Col4(id="I", height=33)

rowa = c.Row([A, B, C])
rowb = c.Row([D, E, F])
rowc = c.Row([G, H, I])

# row1 = c.Row([col2,col1])

dashboard2 = c.Container([rowa, rowb, rowc])


A = c.Col4(id="A", height=100)
B = c.Col4(id="B", height=100)
C = c.Col4(id="C", height=100)

rowa = c.Row([A, B, C])

# row1 = c.Row([col2,col1])

dashboard3 = c.Container(rowa)
