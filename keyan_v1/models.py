from sklearn import svm
from sklearn.ensemble import RandomForestClassifier


def get_model(model_name):
    if model_name.lower() == 'randomforest':
        cfg = {

        }
        return RandomForestClassifier(**cfg)
    elif model_name.lower() == 'svm':
        cfg = {
            'kernel': 'linear',
            'gamma': 10,
            'decision_function_shape': 'ovr',
        }
        return svm.SVC(**cfg)
    else:
        raise NotImplementedError
