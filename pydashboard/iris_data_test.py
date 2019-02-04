import numpy as np
import pandas as pd
from sklearn.datasets import load_iris


iris = load_iris()
iris_df = pd.DataFrame(
    data=np.c_[iris["data"], iris["target"]], columns=iris["feature_names"] + ["target"]
)

def name_target(x):
    x = int(x)
    return iris["target_names"][x]


iris_df["flower"] = iris_df["target"].apply(name_target)
iris_df.drop("target", axis=1, inplace=True)