import pandas as pd
from itertools import product
import statsmodels.api as sm

xs = ['粉丝总量', '作品总数', '点赞总数', '平均点赞']
ys = ['销售额(w)', '销量(w)', '音浪收入(w)', '总佣金(w)']

shifu = pd.read_excel('pre_shifu.xlsx')

for x_name, y_name in product(xs, ys):
    X, Y = shifu.loc[:, x_name], shifu.loc[:, y_name]
    X = sm.add_constant(X)
    model = sm.OLS(Y, X).fit()
    print('-'*46)
    print(f'| X: {x_name:8}, Y: {y_name:12} ')
    print(f'| -> 拟合参数: {model.params[0]:15.4f}, {model.params[1]:15.4f}|')
