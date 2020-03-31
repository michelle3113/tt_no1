import pandas as pd


def transform_wsw(wsw_raw: pd.DataFrame):
    wsw_raw['res'] = 0
    patient_no_list = sorted(list(set(wsw_raw['住院号'])))
    wsw_list = sorted(list(set(wsw_raw['检验细项'])))
    wsw_data = pd.DataFrame(index=patient_no_list, columns=wsw_list)
    wsw_data.loc[:, :] = 0
    for patient_no in patient_no_list:
        tmp_df = wsw_raw[wsw_raw['住院号'] == patient_no]
        for row in tmp_df.itertuples():
            item = row.检验细项
            res = row.结果
            rule = row.参考值
            if '～' in rule:
                low, high = rule.split('～')
                low, high, res = float(low), float(high), float(res)
                if low <= res <= high:  # 达标
                    wsw_data.loc[patient_no, item] = 2
                else:  # 不达标
                    wsw_data.loc[patient_no, item] = 1
            elif rule == '阴性':
                if res == '阴性':  # 达标
                    wsw_data.loc[patient_no, item] = 2
                else:
                    wsw_data.loc[patient_no, item] = 1
            elif rule == '<16':
                if float(res) < 16:  # 达标
                    wsw_data.loc[patient_no, item] = 2
                else:
                    wsw_data.loc[patient_no, item] = 1
            elif rule == '阴性(<1:10)':
                if res == '阴性':  # 达标
                    wsw_data.loc[patient_no, item] = 2
                else:
                    wsw_data.loc[patient_no, item] = 1
            else:  # not a num
                wsw_data.loc[patient_no, item] = 0
    return wsw_data


def preprocess(data_root):
    wsw_df = pd.read_excel(f'{data_root}/有细项名称的检验病人结果_s.xlsx',
                           sheet_name='常规结果', index=False)
    wsw_np = transform_wsw(wsw_df)

    shifu = pd.read_excel(f'{data_root}/儿科路径病人明细_s.xlsx', index=False)
    # shifu = shifu.iloc[:20]

    # remove duplicate column
    unique_col = [col for col in list(shifu.columns) if not '.' in col]
    shifu = shifu[unique_col]

    return shifu


def spilt_train_test(data):
    train_ft, train_lbl, test_ft, test_lbl = [], [], [], []
    return train_ft, train_lbl, test_ft, test_lbl


def train_test_model(train_ft, train_lbl, test_ft, test_lbl, model_name):
    predict, target = [], []
    return predict, target


def eval(pred, targ, metrics=None):
    pass


def _main(data_root):
    data = preprocess(data_root)

    train_ft, train_lbl, test_ft, test_lbl = spilt_train_test(data)

    pred, targ = train_test_model(train_ft, train_lbl, test_ft, test_lbl, 'randomforest')

    eval(pred, targ)


if __name__ == '__main__':
    data_root = '../../tt_data/zhuang/all_data'
    _main(data_root)
