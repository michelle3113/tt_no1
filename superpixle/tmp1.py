import pickle as pkl


def load(filename):
    with open(filename, 'rb') as fp:
        data = pkl.load(fp)
    return data


if __name__ == '__main__':
    train_file = f'D:\\data\\SuperPixel\\mnist_75sp_train.pkl'
    train_data = load(train_file)
    pass
