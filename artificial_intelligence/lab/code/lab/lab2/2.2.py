# 导包
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
from sklearn.svm import SVC
import numpy as np

# 装载数据集
iris = load_iris()
X = iris.data[:, 0:2]
y = iris.target[:]

# 划分数据集
X_train = X[:130, :]
y_train = y[:130]
X_test = X[130:, :]
y_test = y[130:]

print("y_train.shape: ", y_train.shape)

# 数据可视化 - 作散点图
plt.scatter(X[:, 0], X[:, 1], c=y)
plt.show()

# 模型搭建
svc = SVC(kernel='rbf')

# 训练模型
svc.fit(X_train, y_train)
y_predict = svc.predict(X_train)
print("y_predict.shape: ", y_predict.shape)
print('The acc is', svc.score(X_train, y_train))

# 分类边界可视化
assert isinstance(y, object)
plt.scatter(X[:, 0], X[:, 1], c=y)

def plot_hyperplane(clf, X, y, h=0.02, draw_sv=True, title='hyperplane'):
    x_min, x_max = X[:, 0].min() - 0.1, X[:, 0].max() + 0.1
    y_min, y_max = X[:, 1].min() - 0.1, X[:, 1].max() + 0.1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))

    plt.title(title)
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.xticks(())
    plt.yticks(())

    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])  # SVM的分割超平面

    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, cmap='hot', alpha=0.5)
    plt.scatter(X[:, 0], X[:, 1], c=y)

    if draw_sv:
        sv = clf.support_vectors_
        plt.scatter(sv[:, 0], sv[:, 1], c='r', marker='.', s=1)

    plt.show()


plot_hyperplane(svc, X_train, y_train)
