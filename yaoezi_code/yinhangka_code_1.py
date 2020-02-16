# 2020.2.16 银行卡难题1

import numpy as np


def revise_parse(s: str):
    return [25 - (ord(c.lower()) - ord('a')) for c in s]


def cvt_by_mat_dot(code, key_mat):
    res = []
    idx = 0
    while idx + 9 < len(code):
        tmp_mat = np.mat(code[idx: idx + 9]).reshape(3, 3)
        tar_mat = key_mat * tmp_mat
        res.extend(tar_mat.reshape(-1).tolist()[0])
        idx += 9
    res.extend(code[idx:])
    return res


if __name__ == '__main__':
    code = 'OFRNHVTNVWTZNCVCMBZZZ'
    key_mat = np.mat([
        [1, 2, 1],
        [3, 0, 2],
        [1, 1, 0],
    ])
    code = revise_parse(code)
    code = cvt_by_mat_dot(code, key_mat)
    print(code)