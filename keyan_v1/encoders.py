import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder


def replace_na_with_mean(data: pd.DataFrame):
    pass


def no_encode(data: pd.DataFrame):
    pass


def one_hot_encode(data: pd.DataFrame):
    data = np.array(data).tolist()
    ohe = OneHotEncoder()
    ohe.fit(data)
    encoded = ohe.transform(data).toarray()
    return encoded


def subtraction_encode(data: pd.DataFrame):
    pass


def mean_encode(data: pd.DataFrame):
    pass


def order_num_encode(data: pd.DataFrame):
    pass


def norm_encode(data: pd.DataFrame):
    pass


def nlp_encode(data: pd.DataFrame):
    pass

# def in_range_encode(data: pd.DataFrame):
#     pass
