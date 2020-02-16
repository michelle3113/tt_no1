# 2020.2.16 银行卡难题1

import numpy as np


def revise_parse(s: str):
    return [25 - (ord(c.lower()) - ord('a')) for c in s]


def cvt_by_mat_dot(source, key_mat):
    res = []
    idx = 0
    while idx + 9 < len(source):
        tmp_mat = np.mat(source[idx: idx + 9]).reshape(3, 3)
        tar_mat = tmp_mat * key_mat
        res.extend(tar_mat.reshape(-1).tolist()[0])
        idx += 9
    res.extend(source[idx:])
    return res


if __name__ == '__main__':
    source_str = 'OFRNHVTNVWTZNCVCMBZZZ'
    key_mat = np.mat([
        [1, 2, 1],
        [3, 0, 2],
        [1, 1, 0],
    ])
    target = revise_parse(source_str)
    target = cvt_by_mat_dot(target, key_mat)
    print(target)
