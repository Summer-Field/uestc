# 导包
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import seaborn as sns

# 读取文件并预处理数据
def read_file(file):
    X = []
    y = []
    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip().split(',')
            data_x = [float(line[i]) for i in range(len(line) - 1)]
            data_y = [float(line[-1])]
            X.append(data_x)
            y.append(data_y)
    train_X = X[:2000]
    train_y = y[:2000]
    test_X  = X[2000:]
    test_y  = y[2000:]
    train_X = np.array(train_X)
    train_y = np.array(train_y)
    test_X  = np.array(test_X)
    test_y  = np.array(test_y)
    return train_X, train_y, test_X, test_y

# 数据处理
def dataAnalyze(train_X, train_y):
    plt.figure(figsize=(16, 10), dpi=150)
    features = ['Focal_depth', 'Latitude', 'Longitude']
    train_y = list(np.squeeze(train_y))
    frows, fcols = 2, 2
    for i in range(3):
        x = list(train_X[:, i])
        ax = plt.subplot(frows, fcols, i + 1)
        sns.regplot(x=x,
                    y=train_y,
                    ax=ax,
                    scatter_kws={
                        'marker': '.',
                        's': 3,
                        'alpha': 0.3
                    },
                    line_kws={'color': 'k'})
        plt.xlabel(features[i])
        plt.ylabel('Richter')
    plt.show()


# 数据处理
def process(train_X, test_X):
    ss = StandardScaler()
    train_X = ss.fit_transform(train_X)
    test_X = ss.fit_transform(test_X)
    return train_X, test_X

# 主函数
if __name__ == '__main__':
    FILE = '../quake.dat'
    X, y, _, _ = read_file(FILE)
    print("X.shape", X.shape)
    print("y.shape", y.shape)
    dataAnalyze(X, y)
