import os.path as osp
import pandas as pd
import json
from pre_config import all_cfg
from encoders import diags_encode, encode


def transform_wsw(wsw_raw: pd.DataFrame):
    sample_id_list = list(set(wsw_raw['住院号'].astype('str').str.cat(wsw_raw['住院次数'].astype('str'), sep='_')))
    wsw_list = sorted(list(map(lambda s: s.strip(), set(wsw_raw['检验细项']))))
    wsw_data = pd.DataFrame(index=sample_id_list, columns=wsw_list)
    wsw_data.loc[:, :] = 0
    for sample_id in sample_id_list:
        patient, times = sample_id.split('_')
        tmp_df = wsw_raw[(wsw_raw['住院号'] == int(patient)) & (wsw_raw['住院次数'] == int(times))]
        for row in tmp_df.itertuples():
            item = row.检验细项.strip()
            res = row.结果
            rule = row.参考值
            if pd.isna(rule) or res == '另报' or res == '------':
                continue
            # assert isinstance(rule, str), rule
            if '～' in rule:
                low, high = rule.split('～')
                low, high = float(low), float(high)
                if isinstance(res, str) and '<' in res:
                    res = float(res[1:])
                else:
                    res = float(res)
                if low <= res <= high:  # 达标
                    wsw_data.loc[sample_id, item] = 2
                else:  # 不达标
                    wsw_data.loc[sample_id, item] = 1
            elif rule == '阴性':
                if res == '阴性':  # 达标
                    wsw_data.loc[sample_id, item] = 2
                else:
                    wsw_data.loc[sample_id, item] = 1
            elif rule == '<16':
                if float(res) < 16:  # 达标
                    wsw_data.loc[sample_id, item] = 2
                else:
                    wsw_data.loc[sample_id, item] = 1
            elif rule == '阴性(<1:10)':
                if res == '阴性':  # 达标
                    wsw_data.loc[sample_id, item] = 2
                else:
                    wsw_data.loc[sample_id, item] = 1
            else:  # not a num
                wsw_data.loc[sample_id, item] = 0
    return wsw_data


def transform_diag(main_raw):
    diags = {}
    sample_id_list = list(set(main_raw['patient_admiss']))
    for sample_id in sample_id_list:
        tmp_df = main_raw[main_raw['patient_admiss'] == sample_id]
        diags[sample_id] = {
            'admiss_diag': [],
            'clinic_diag': [],
            'dis_diag_type': [],
            'dis_diag': [],
            'dis_diag_comment': [],
        }
        for row in tmp_df.itertuples():
            diags[sample_id]['admiss_diag'].append(row.admiss_diag)
            diags[sample_id]['clinic_diag'].append(row.clinic_diag)
            diags[sample_id]['dis_diag_type'].append(row.dis_diag_type)
            diags[sample_id]['dis_diag'].append(row.dis_diag)
            diags[sample_id]['dis_diag_comment'].append(row.dis_diag_comment)
        for k, v in diags[sample_id].items():
            diags[sample_id][k] = list(set(v))
    return diags


def transform_others(main_raw):
    # # remove duplicate column
    # unique_col = [col for col in list(main_raw.columns) if not '.' in col]
    # shifu_df = main_raw[unique_col]
    # remove duplicated row according to patient_admiss
    shifu_df = main_raw.drop_duplicates('patient_admiss')
    # remove useless column
    cols = ['patient_admiss', 'admiss_date', 'dis_date']
    for k, v in all_cfg.items():
        for _k, _ in v.items():
            if _k not in ('wsw_norm', 'admiss_diag', 'clinic_diag',
                          'dis_diag', 'dis_diag_type', 'dis_diag_comment'):
                cols.append(_k)
    shifu_df = shifu_df[cols]
    shifu_df = shifu_df.set_index('patient_admiss')

    # trasform date
    shifu_df['admiss_date'] = shifu_df['admiss_date'].apply(
        lambda s: s if s.count(':') == 2 else s[:s.rfind(':')])
    shifu_df['dis_date'] = shifu_df['dis_date'].apply(
        lambda s: s if s.count(':') == 2 else s[:s.rfind(':')])
    shifu_df['birth_date'] = shifu_df['birth_date'].apply(
        lambda s: s if (not isinstance(s, str)) or s.count(':') == 2 else s[:s.rfind(':')])
    shifu_df['diagnosis_date'] = shifu_df['diagnosis_date'].apply(
        lambda s: s if (not isinstance(s, str)) or s.count(':') == 2 else s[:s.rfind(':')])

    shifu_df.loc[shifu_df['birth_date'].isna(), 'birth_date'] = \
        shifu_df.loc[shifu_df['birth_date'].isna(), 'admiss_date']
    shifu_df.loc[shifu_df['diagnosis_date'].isna(), 'diagnosis_date'] = \
        shifu_df.loc[shifu_df['diagnosis_date'].isna(), 'admiss_date']

    return shifu_df


def preprocess(data_root, res_root):
    res_wsw_file = osp.join(res_root, '微生物检验.xlsx')
    res_main_file = osp.join(res_root, '病人明细.xlsx')
    res_diag_file = osp.join(res_root, 'diag.json')

    if not osp.exists(res_wsw_file):
        wsw_df = pd.read_excel(f'{data_root}/有细项名称的检验病人结果_s.xlsx',
                               sheet_name='常规结果', index=False)
        # wsw_df = wsw_df.loc[:100]
        wsw_df = transform_wsw(wsw_df)
        wsw_df.to_excel(res_wsw_file)
    else:
        wsw_df = pd.read_excel(res_wsw_file, index_col=0)

    if not osp.exists(res_main_file) or not osp.exists(res_diag_file):
        shifu_df = pd.read_excel(f'{data_root}/儿科路径病人明细_s.xlsx', index=False)
        # shifu = shifu.iloc[:20]

        if not osp.exists(res_diag_file):
            diags = transform_diag(shifu_df)
            with open(res_diag_file, 'w') as fp:
                json.dump(diags, fp)
        else:
            with open(res_diag_file, 'r') as fp:
                diags = json.load(fp)

        if not osp.exists(res_main_file):
            main_df = transform_others(shifu_df)
            main_df.to_excel(res_main_file)
        else:
            main_df = pd.read_excel(res_main_file, index_col=0)
    else:
        with open(res_diag_file, 'r') as fp:
            diags = json.load(fp)
        main_df = pd.read_excel(res_main_file, index_col=0)

    # convert data type
    main_df['admiss_date'] = pd.to_datetime(main_df['admiss_date'])
    main_df['dis_date'] = pd.to_datetime(main_df['dis_date'])
    main_df['birth_date'] = pd.to_datetime(main_df['birth_date'])
    main_df['diagnosis_date'] = pd.to_datetime(main_df['diagnosis_date'])

    # encode data
    # init
    sample_id_list = main_df.index
    pre_data = {}

    # for wsw data
    pre_wsw = pd.DataFrame(index=sample_id_list, columns=wsw_df.columns)
    for _id in sample_id_list:
        if _id in wsw_df.index:
            pre_wsw.loc[_id] = wsw_df.loc[_id]
    pre_data['wsw_norm'] = pre_wsw

    # for diag data:
    # 'admiss_diag', 'clinic_diag', 'dis_diag', 'dis_diag_type',
    for _cur in ('admiss_diag', 'clinic_diag', 'dis_diag', 'dis_diag_type'):
        pre_data[_cur] = diags_encode(diags, _cur)
    # 'dis_diag_comment'
    pre_data['dis_diag_comment'] = pd.DataFrame(index=sample_id_list, columns=['dis_diag_type'])
    pre_data['dis_diag_comment'].loc[:] = 0

    # for common data
    # get encoder type for each attribute
    decode_cfg = {}
    for _k, _v in all_cfg.items():
        for _kk, _vv in _v.items():
            decode_cfg[_kk] = {
                'app': _vv['app'],
                'fill_nan': _vv['fill_nan'],
            }
    for _cur in main_df.columns:
        if _cur in decode_cfg.keys():
            pre_data[_cur] = encode(main_df, _cur, decode_cfg[_cur])

    # generate target
    target = (main_df['dis_date'] - main_df['admiss_date']).apply(lambda d: d.days)
    pre_data['target'] = pd.DataFrame(target, index=main_df.index)

    return pre_data


def spilt_train_test(data, selected_attrs):
    # concat and generate all table

    # random spilt it
    train_ft, train_lbl, test_ft, test_lbl = [], [], [], []
    return train_ft, train_lbl, test_ft, test_lbl


def train_test_model(train_ft, train_lbl, test_ft, test_lbl, model_name):
    predict, target = [], []
    return predict, target


def eval(pred, targ, metrics=None):
    pass


def _main(data_root, res_root):
    data = preprocess(data_root, res_root)

    train_ft, train_lbl, test_ft, test_lbl = spilt_train_test(data)

    pred, targ = train_test_model(train_ft, train_lbl, test_ft, test_lbl, 'randomforest')

    eval(pred, targ)


if __name__ == '__main__':
    data_root = '../../tt_data/zhuang/all_data'
    res_root = '../../tt_res/all_res'
    _main(data_root, res_root)
