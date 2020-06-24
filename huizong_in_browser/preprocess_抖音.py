import pandas as pd
import numpy as np


def cvt(x):
    if isinstance(x, str):
        if 'w' in x:
            x = float(x[:-1]) * 10000
        elif '亿' in x:
            x = float(x[:-1]) * 1e8
        elif '-' in x:
            x = np.nan
        else:
            x = float(x)
    return float(x)


def cvt_row(row):
    return row.apply(cvt)


if __name__ == '__main__':
    shifu = pd.read_excel('shifu.xlsx')
    not_pre = ['排名', '姓名', '性别', '地区', '分类']
    pre = set(shifu.columns) - set(not_pre)

    # preprocess others
    shifu.loc[:, pre] = shifu.loc[:, pre].apply(cvt_row)

    # for col in pre:
    #     shifu.loc[:, col] = (shifu.loc[:, col] - shifu.loc[:, col].min())/(shifu.loc[:, col].max() - shifu.loc[:, col].min())

    category = list(set(shifu.loc[:, '分类'].tolist()))
    shifu.loc[:, '分类'] = shifu.loc[:, '分类'].apply(lambda x: category.index(x))

    shifu.to_excel('2_shifu.xlsx', index=False)
