import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error  # MSE
from sklearn.metrics import r2_score  # R^2
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import confusion_matrix


def cal_metrics(lbl, pred, category_name, title):
    res = {}
    # confusion matrix
    c_matrix = confusion_matrix(lbl, pred)
    plot_confusion_matrix(c_matrix, category_name,
                          f'Confusion Matrix on {title} Attributes')

    # accuracy
    acc = accuracy_score(lbl, pred)
    print(f'Accuracy: {acc:.4f}')


def plot_confusion_matrix(cm, labels_name, title):
    # normalization
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]  # 归一化
    plt.imshow(cm, interpolation='nearest')
    plt.title(title)
    plt.colorbar()
    num_local = np.array(range(len(labels_name)))
    # plt.xticks(num_local, labels_name, rotation=90)
    plt.xticks(num_local, labels_name)
    plt.yticks(num_local, labels_name)
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.show()
