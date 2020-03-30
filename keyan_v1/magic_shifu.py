import pandas as pd


def preprocess(data):
    return data


def spilt_train_test(data):
    train_ft, train_lbl, test_ft, test_lbl = [], [], [], []
    return train_ft, train_lbl, test_ft, test_lbl


def train_test_model(train_ft, train_lbl, test_ft, test_lbl, model_name):
    predict, target = [], []
    return predict, target


def eval(pred, targ, metrics=None):
    pass


def _main():
    data = []
    data = preprocess(data)

    train_ft, train_lbl, test_ft, test_lbl = spilt_train_test(data)

    pred, targ = train_test_model(train_ft, train_lbl, test_ft, test_lbl, 'randomforest')

    eval(pred, targ)


if __name__ == '__main__':
    _main()
