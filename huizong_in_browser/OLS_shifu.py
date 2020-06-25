import pandas as pd
import numpy as np
from itertools import product
import statsmodels.api as sm


def deal(shifu, x, y, out_file):
    cols = ['y', 'model', *x, 'rsquared', 'rsquared_adj', 'fvalue', 'f_pvalue']
    difei = None

    for idx, (y_name, x_name) in enumerate(product(y, x)):
        X, Y = shifu.loc[:, x_name], shifu.loc[:, y_name]
        X = sm.add_constant(X)
        model = sm.OLS(Y, X).fit()
        print('-' * 46)
        print(f'| X: {x_name:8}, Y: {y_name:12} ')
        print(f'| -> 拟合参数: {model.params[0]:15.4f}, {model.params[1]:15.4f}|')

        row = pd.DataFrame({k: [np.nan] for k in cols})
        row.loc[0, 'y'] = y_name
        row.loc[0, 'model'] = f'model {idx+1}'
        row.loc[0, x_name] = f'{model.params[0]:.4f}\n{model.params[1]:.4f}**'
        row.loc[0, 'fvalue'] = model.fvalue
        row.loc[0, 'f_pvalue'] = model.f_pvalue
        row.loc[0, 'rsquared'] = model.rsquared
        row.loc[0, 'rsquared_adj'] = model.rsquared_adj

        difei = difei.append(row) if difei is not None else row
    difei = difei.set_index(['y', 'model'])
    difei.to_excel(out_file, index=True)


if __name__ == '__main__':
    x1 = ['销量', '销售额', ]
    x2 = ['粉丝总量', '点赞总数', '平均评论', '平均转发', '音浪收入']
    ys = ['观看总人数', '峰值人数', '粉丝增量', '点赞增量', '评论增量', '转发增量', '关注增量', '粉丝团增量', '送礼UV']

    shifu = pd.read_excel('data/pre_shifu.xlsx')
    deal(shifu, x1, ys, 'data/销售.xlsx')
    deal(shifu, x2, ys, 'data/其他.xlsx')

    # model.rsquared
    # model.rsquared_adj
    # model.fvalue
    # model.f_pvalue