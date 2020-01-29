import os.path as osp
import warnings

import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import pearsonr
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import mean_squared_error  # MSE
from sklearn.metrics import r2_score  # R^2
from sklearn.preprocessing import OneHotEncoder
from sklearn.utils import shuffle

warnings.filterwarnings('ignore')

data_dir = 'input/儿科路径病人明细_s1.xlsx'
cache_folder = 'results'

payment = ['charge1', 'charge2', 'charge3', 'charge6', 'charge7', 'charge10']
# personal_information = ['sex', 'blood_type', 'age', 'home_district']
personal_information = ['sex', 'blood_type', 'home_district']
health_state = ['admiss_diag', 'dis_diag', 'admiss_times', 'dis_diag_no', 'dis_diag_type', 'dis_diag_status', 'admiss_status']
# others = ['pay_flag', 'local_flag']
others = ['local_flag']
all = [*payment, *personal_information, *health_state, *others]

payment.append('DIH_day')
personal_information.append('DIH_day')
health_state.append('DIH_day')
others.append('DIH_day')
all.append('DIH_day')


def preprocess():
    shifu = pd.read_excel(data_dir)

    # remove duplicate column
    unique_col = [col for col in list(shifu.columns) if not '.' in col]
    shifu = shifu[unique_col]
    shifu.to_excel(osp.join(cache_folder, 'shifu_demo_unique.xlsx'), index=False)

    # remove columns that containing null more that 85% ratio
    shifu = shifu.loc[:, shifu.notna().mean() > 0.85]
    # or shifu = shifu.dropnqa(1,thresh=len(shifu.index)*0.85)
    shifu.to_excel(osp.join(cache_folder, 'shifu_demo_nonull.xlsx'), index=False)

    # delete '-'
    shifu = shifu.loc[:, (shifu == '-').sum() == 0]
    shifu.to_excel(osp.join(cache_folder, 'shifu_demo_nogang.xlsx'), index=False)

    # standard admiss_date: 2014-03-25 09:34:28:613 -> 2014-03-25 09:34:28
    shifu['admiss_date'] = shifu['admiss_date'].apply(lambda s: s[:s.rfind(':')])

    # convert object to datetime class
    shifu['admiss_date'] = pd.to_datetime(shifu['admiss_date'])
    shifu['dis_date'] = pd.to_datetime(shifu['dis_date'])

    # generate target DIH column
    DIH_day = (shifu['dis_date'] - shifu['admiss_date']).apply(lambda d: d.days)
    shifu['DIH_day'] = DIH_day
    shifu.to_excel(osp.join(cache_folder, 'shifu_demo_add_target.xlsx'), index=False)

    ########################################################
    # data standard (**very important**)

    # for sex attribute: normalize the value into range[0, 1] not [1, 2]
    shifu['sex'] = shifu['sex'] - 1

    ########################################################

    # shuffle dataset
    shifu = shuffle(shifu)

    return shifu


def encode_shifu(shifu):
    tobe_encoded_names = ['dis_diag', 'admiss_diag']
    tobe_encoded_names = set(tobe_encoded_names) & set(shifu.columns)
    if tobe_encoded_names != set():
        column_list = np.array(shifu[tobe_encoded_names]).tolist()
        ohe = OneHotEncoder()
        ohe.fit(column_list)
        results = ohe.transform(column_list).toarray()
        shifu = pd.concat([shifu, pd.DataFrame(results)], axis=1)
        shifu = shifu.drop(tobe_encoded_names, axis=1)

    shifu.to_excel(osp.join(cache_folder, 'shifu_demo_one_hot.xlsx'), index=False)
    return shifu


def tiaotiao(shifu):
    shifu = encode_shifu(shifu)
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

    # fit and prediction:
    clf = RandomForestClassifier()
    clf.fit(train_subset, train_target)
    test_prediction = clf.predict(test_subset)

    # metrics:
    # metric for RMSE
    rmse = np.sqrt(mean_squared_error(test_target, test_prediction))

    # metric for rho
    rho, p_value = stats.spearmanr(test_target, test_prediction)

    # metric for MSE
    mes = mean_squared_error(test_target, test_prediction)

    # metric for MAPE
    def mean_absolute_percentage_error(y_true, y_pred):
        y_true, y_pred = np.array(y_true), np.array(y_pred)
        return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

    mape = mean_absolute_percentage_error(test_target, test_prediction)

    # metric for Spec
    TN, FP, FN, TP = confusion_matrix(test_target, test_prediction).ravel()
    spec = TN / (TN + FP)

    # metric fro Sens
    sens = TP / (TP + FN)

    # metric for Acc
    acc = TP / (TP + FP + TN + FN)

    # metric for R^2
    r2 = r2_score(test_target, test_prediction)

    # metric for abs(R)
    # don't understand the formulation of |R|
    r, _ = pearsonr(test_target, test_prediction)

    # overall description: confusion matrix
    # print(pd.crosstab(category_name[test_target], category_name[test_prediction],
    #                   rownames=['Target'], colnames=['Prediction'], margins=True))
    print(f'|RMSE: {rmse:10.3f} | rho : {rho:10.3f} | MSE   :{mes:10.3f}|')
    print(f'|MAPE: {mape:10.3f} | Spec: {spec:10.3f} | Sens  :{sens:10.3f}|')
    print(f'|Acc : {acc:10.3f} | R^2 : {r2:10.3f} | abs(R):{r:10.3f}|')


if __name__ == '__main__':
    shifu = preprocess()

    # All:
    shifu_all = shifu
    print('\nAll -> payment experiment:')
    tiaotiao(shifu_all[payment])
    print('\nAll -> personal experiment:')
    tiaotiao(shifu_all[personal_information])
    print('\nAll -> health experiment:')
    tiaotiao(shifu_all[health_state])
    print('\nAll -> all experiment:')
    tiaotiao(shifu_all[all])

    # DIH<=14
    shifu_DIH_leq_14 = shifu[shifu['DIH_day'] <= 14]
    print('\nDIH<=14 -> payment experiment:')
    tiaotiao(shifu_DIH_leq_14[payment])
    print('\nDIH<=14 -> personal experiment:')
    tiaotiao(shifu_DIH_leq_14[personal_information])
    print('\nDIH<=14 -> health experiment:')
    tiaotiao(shifu_DIH_leq_14[health_state])
    print('\nDIH<=14 -> all experiment:')
    tiaotiao(shifu_DIH_leq_14[all])

    # DIH > 14
    shifu_DIH_gt_14 = shifu[shifu['DIH_day'] <= 14]
    print('\nDIH>14 -> payment experiment:')
    tiaotiao(shifu_DIH_gt_14[payment])
    print('\nDIH>14 -> personal experiment:')
    tiaotiao(shifu_DIH_gt_14[personal_information])
    print('\nDIH>14 -> health experiment:')
    tiaotiao(shifu_DIH_gt_14[health_state])
    print('\nDIH>14 -> all experiment:')
    tiaotiao(shifu_DIH_gt_14[all])
