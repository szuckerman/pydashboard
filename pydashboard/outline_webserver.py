from pydashboard import components as s
from pydashboard.iris_data_test import iris_df
from pydashboard.dominate_template import dashboard as t
#
# pie_chart = s.ChartElement("pie_chart", cls="div_background", height=45)
# line_chart = s.ChartElement("line_chart", cls="div_background", height=45)
# pie_chart = s.Col12(pie_chart)
# line_chart = s.Col12(line_chart)
# item1 = s.Row(pie_chart)
# item2 = s.Row(line_chart)
# item = s.Row(item1, item2)
# dashboard = s.Dashboard(item1, item2)

dashboard=s.Dashboard(data=iris_df, template=t)
# {'pie_chart': pie_chart}
dashboard.run_outlines()
