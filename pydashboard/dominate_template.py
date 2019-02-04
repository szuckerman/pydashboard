from dominate.tags import *
from pydashboard import components as c

template1 = div(cls='container')
template1_row1 = template1.add(div(cls='row'))
template1_row2 = template1.add(div(cls='row'))

template1_row1.add(div(cls='col-md-6', id='A'))
template1_row1.add(div(cls='col-md-6', id='B'))

template1_row2.add(div(cls='col-md-4', id='C'))
template1_row2.add(div(cls='col-md-4', id='D'))
template1_row2.add(div(cls='col-md-4', id='E'))
# row2.add(div(cls='col-md-4', id='D'))
# row2.add(div(cls='col-md-4', id='E'))


template2 = div(cls='container')
template2_row1 = template2.add(div(cls='row'))

template2_row1.add(div(cls='col-md-12', id='A'))



cola=c.Col6(id='A', height=50)
colb=c.Col6(id='C', height=50)
colc=c.Col6(id='D', height=50)
cold=c.Col6(id='E', height=50)

rowa = c.Row([cola, colb])
rowb = c.Row([colc, cold])

col1 = c.Col6([rowa, rowb])
col2 = c.Col6(id='B', height=100)

row1 = c.Row([col2,col1])

dashboard = c.Container(row1)

