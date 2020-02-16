# love you tons! tiaotiao
import numpy as np


# metric for MAPE
def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


def acc(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    N_tp = ((y_true >= 1) and (y_pred >= 1)).sum()
    N_tn = ((y_true >= 1) and (y_pred == 0)).sum()
    return (N_tp + N_tn) / y_true.size()
