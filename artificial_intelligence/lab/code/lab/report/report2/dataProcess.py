# 导包
import numpy as np
from sklearn.preprocessing import StandardScaler

# 读文件 预处理数据
def read_file(file):
    X = []
    y = []
    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip().split(',')
            data_x = [float(line[i]) for i in range(len(line)-1)]
            data_y = [float(line[-1])]
            X.append(data_x)
            y.append(data_y)
    train_X = X[:1200]
    train_y = y[:1200]
    test_X = X[1200:]
    test_y = y[1200:]
    train_X = np.array(train_X)
    train_y = np.array(train_y)
    test_X = np.array(test_X)
    test_y = np.array(test_y)
    return train_X, train_y, test_X, test_y

# 数据处理
def process(train_X, test_X):
    ss = StandardScaler()
    train_X = ss.fit_transform(train_X)
    test_X = ss.fit_transform(test_X)
    return train_X, test_X

# 数据分析
def dataAnalysis(train_y):
    print('0:', np.count_nonzero(train_y))
    print('1:', train_y.shape[0]-np.count_nonzero(train_y))


if __name__ == '__main__':
    FILE = '../data_banknote_authentication.txt'
    X, y, testX, _ = read_file(FILE)
    m, n = process(X, testX)
    print(m.shape)
    print(y)
    dataAnalysis(y)