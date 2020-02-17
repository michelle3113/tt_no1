# 0 shifu's turn

def parse_num_0(code):
    return [ord(c) - ord('0') for c in code]


def generate_0(code, key):
    res = []
    idx = 0
    while idx < len(code):
        tmp_list = code[idx:idx + 4]
        for k in key:
            res.append(tmp_list[k])
        idx += 4
    return res


def parse_alpha_0(code):
    return [chr(ord('Z') - c) for c in code]


if __name__ == '__main__':
    code = '****************'
    # print(''.join(['*' for c in code]))
    key = [1, 2, 1, 3, 0, 2, 1, 1, 0]
    mimi = generate_0(parse_num_0(code), key)
    # print(mimi)
    mimi = parse_alpha_0(mimi)
    # print(mimi)
    mimi = ' '.join([''.join(mimi[i:i+9]) for i in range(0, len(mimi), 9)])
    print(mimi)
