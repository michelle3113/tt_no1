import pandas as pd
import numpy as np
import scipy
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import shuffle

from sklearn.metrics import mean_squared_error # MSE
from sklearn.metrics import confusion_matrix
from scipy import stats
from sklearn.metrics import r2_score # R^2
from scipy.stats import pearsonr

from sklearn.preprocessing import OneHotEncoder

shifu = pd.read_excel('input/儿科路径病人明细_s1.xlsx')

# remove duplicate column
unique_col = [col for col in list(shifu.columns) if not '.' in col]
shifu = shifu[unique_col]
shifu.to_excel('results/shifu_demo_unique.xlsx', index=False)

# remove columns that containing null more that 85% ratio
shifu = shifu.loc[:, shifu.notna().mean() > 0.85]
# or shifu = shifu.dropnqa(1,thresh=len(shifu.index)*0.85)
shifu.to_excel('results/shifu_demo_nonull.xlsx', index=False)

# delete '-'
shifu = shifu.loc[:, (shifu == '-').sum() == 0]
shifu.to_excel('results/shifu_demo_nogang.xlsx', index=False)

# standard admiss_date: 2014-03-25 09:34:28:613 -> 2014-03-25 09:34:28
shifu['admiss_date'] = shifu['admiss_date'].apply(lambda s: s[:s.rfind(':')])

# convert object to datetime class
shifu['admiss_date'] = pd.to_datetime(shifu['admiss_date'])
shifu['dis_date'] = pd.to_datetime(shifu['dis_date'])

# generate target DIH column
DIH_day = (shifu['dis_date'] - shifu['admiss_date']).apply(lambda d: f'day_{d.days}')
shifu['DIH_day'] = DIH_day
shifu.to_excel('results/shifu_demo_add_target.xlsx', index=False)

########################################################
# data standard (**very important**)

# for sex attribute: normalize the value into range[0, 1] not [1, 2]
shifu['sex'] = shifu['sex'] - 1

########################################################

dis_diag = [['J18.000'], ['R94.500'], ['J18.000'], ['Z54.000']]
ohe=OneHotEncoder()
ohe.fit(dis_diag)
one_hot1=ohe.transform(dis_diag).toarray()
shifu['dis_diag']=one_hot1

admiss_diag=[['J18.000'], ['J18.000'], ['J18.000'], ['J18.000']]
ohe=OneHotEncoder()
ohe.fit(admiss_diag)
one_hot2=ohe.transform(admiss_diag).toarray()
shifu['admiss_diag']=one_hot2

shifu.to_excel('results/shifu_demo_one_hot.xlsx', index=False)

# shuffle dataset
shifu = shuffle(shifu)

# compute train num from train ratio
train_ratio = 0.70
train_num = int(len(shifu) * train_ratio)
print(f'Sample num: {len(shifu)}, Train num: {train_num}, Test num: {len(shifu) - train_num}')

# initialize target and generate all category name set
target, category_name = pd.factorize(shifu['DIH_day'])

# select train/test subset
# [      train_subset    |    test_subset   ]
# [......................|..................]
train_subset = shifu.iloc[:train_num]
train_target = target[:train_num]
test_subset = shifu.iloc[train_num:]
test_target = target[train_num:]


# payment=['charge 1','charge 2','charge 3']
# fts_for_leq_14=shifu[payment]
# fts_for_leq_14->fit->predict
payment=shifu['charge1','charge2','charge3','charge6','charge7','charge10']
fts_for_all_payment=shifu[payment]

# select specific features for fit stage
selected_fts = fts_for_all_payment

# initialize random forest classifier for fit
clf = RandomForestClassifier()
clf.fit(train_subset[selected_fts], train_target)

test_prediction = clf.predict(test_subset[selected_fts])

# overall description: confusion matrix
print(pd.crosstab(category_name[test_target], category_name[test_prediction],
                  rownames=['Target'], colnames=['Prediction'], margins=True))

# metric for RMSE
rmse = np.sqrt(mean_squared_error(test_target, test_prediction))
print(f'RMSE: {rmse}')

# metric for rho
rho, p_value = stats.spearmanr(test_target, test_prediction)
print(f'rho: {rho:.3f}')

# metric for MSE
mes = mean_squared_error(test_target, test_prediction)
print(f'MSE: {mes:.3f}')

# metric for MAPE
def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

mape = mean_absolute_percentage_error(test_target, test_prediction)
print(f'MAPE: {mape:.3f}')

# metric for Spec
TN, FP, FN, TP = confusion_matrix(test_target, test_prediction).ravel()
spec = TN/(TN+FP)
print(f'Spec: {spec:.3f}')

# metric fro Sens
sens = TP/(TP+FN)
print(f'Sens: {sens:.3f}')

# metric for Acc
acc = TP/(TP+FP+TN+FN)
print(f'Acc: {acc:.3f}')

# metric for R^2
r2 = r2_score(test_target, test_prediction)
print(f'R^2: {r2:.3f}')

# metric for abs(R)
# don't understand the formulation of |R|
r,_ =pearsonr(test_target, test_prediction)
print(f'abs(R):{r:.3f}')


