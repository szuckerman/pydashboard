from pydashboard import components as s
from pydashboard.example_data.example_data import dat
from pydashboard.components import Dimension
from pydashboard.dc_components import PieChart, RowChart
from pydashboard.dominate_template import dashboard as t


dim_address = Dimension("address")
dim_Pstatus = Dimension("Pstatus")
dim_famsize = Dimension("famsize")
dim_romantic = Dimension("romantic")
dim_studytime = Dimension("studytime")

pie_chart = PieChart("A", dim_address, radius=200, height=500, width=500)
pie_chart2 = PieChart("B", dim_Pstatus, radius=100, slicesCap=2)
pie_chart3 = PieChart("C", dim_famsize, radius=100, inner_radius=20)
pie_chart4 = PieChart("D", dim_romantic)
pie_chart5 = RowChart("E", dim_studytime, elasticX=True, xAxis='tickValues([0, 20, 200])')


dashboard = s.Dashboard(pie_chart, pie_chart2, pie_chart3, pie_chart4, pie_chart5, data=dat, template=t)

dashboard.view_outlines()
# dashboard.run()
# s.Dashboard(data=iris_df).run()
# {'pie_chart': pie_chart}
# dashboard.run_outlines()
