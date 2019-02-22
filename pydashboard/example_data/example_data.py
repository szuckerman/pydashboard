import pandas as pd

dat = pd.read_csv(
    "/Users/zucks/PycharmProjects/pydashboard/pydashboard/example_data/student-mat.csv",
    sep=";",
)

dat.columns
