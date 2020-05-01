import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder


def diags_encode(diags: dict, cur):
    # statistics all diagnosis type
    all_diag = []
    for _id, _diag in diags.items():
        all_diag.extend(_diag[cur])
    all_diag = list(sorted(list(set(all_diag))))
    cur_df = pd.DataFrame(index=list(diags.keys()), columns=all_diag)
    cur_df.loc[:] = 0
    for _id, _diag in diags.items():
        for d in _diag[cur]:
            cur_df.loc[_id, d] = 1
    return cur_df


def encode(df: pd.DataFrame, cur, encoder_cfg):
    encoder_type, fill_nan = encoder_cfg['app'], encoder_cfg['fill_nan']
    assert encoder_type in ('one_hot', 'order', 'sub', 'raw', 'norm')
    cur_df = df[cur]
    # process nan
    if fill_nan == 'mean':
        mean_val = cur_df.loc[((cur_df.notna()) & (cur_df != '-'))].astype(float).mean()
        # cur_df.fillna(mean_val)
        cur_df.loc[cur_df == '-'] = mean_val
        cur_df = cur_df.fillna(mean_val)
    elif fill_nan == 'start':
        # has done in transform
        pass
    else:
        cur_df = cur_df.fillna(fill_nan)

    # encode
    # print(f'processing {cur}')
    if encoder_type == 'raw':
        cur_df = cur_df.astype(float)
        data = cur_df
        return data
    elif encoder_type == 'order':
        data = cur_df.astype(float)
        return data
    elif encoder_type == 'norm':
        cur_df = cur_df.astype(float)
        data = cur_df / (cur_df.max() - cur_df.min())
        return data
    elif encoder_type == 'one_hot':
        if cur == 'occupation_code':
            print()
        data = one_hot_encode(cur_df)
        return pd.DataFrame(data, index=df.index)
    elif encoder_type == 'sub':
        if cur == 'birth_date':
            data = (df['admiss_date'] - df['birth_date']).apply(lambda d: d.days)
            return pd.DataFrame(data, index=df.index)
        elif cur == 'diagnosis_date':
            data = (df['diagnosis_date'] - df['admiss_date']).apply(lambda d: d.days)
            return pd.DataFrame(data, index=df.index)
    else:
        raise NotImplementedError


def one_hot_encode(data: pd.DataFrame):
    data = np.array(data).reshape(-1, 1).tolist()
    ohe = OneHotEncoder()
    ohe.fit(data)
    encoded = ohe.transform(data).toarray()
    return encoded
