# 导包
from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC
import matplotlib.pyplot as plt

# 生成数据集，数据量为1000，特征为2，标签值为2
X, y = make_blobs(n_samples=1000, n_features=2, centers=2)

# 分割数据集，训练集和测试集的比例为4:1
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8)
print("X.shape: ", X.shape)  # 100,2
print("y.shapr: ", y.shape)  # 100,

# 数据可视化
plt.scatter(X[:, 0], X[:, 1], c=y)
plt.show()

# 获取数据值均值和方差，并进行数据标准化
standardScaler = StandardScaler()
standardScaler.fit(X_train)
X_train = standardScaler.transform(X_train)
X_test = standardScaler.transform(X_test)

# 模型SVM模型搭建，并训练该模型
svc = LinearSVC(C=1)

# 训练模型
svc.fit(X_train, y_train)
y_predict = svc.predict(X_test)

print('The acc is', svc.score(X_test, y_test))

# 调整参数
for i in range(1, 4):
    svc = LinearSVC(C=10**i)
    svc.fit(X_train, y_train)
    y_predict = svc.predict(X_test)
    print('The acc with C={} is {}'.format(10**i, svc.score(X_test, y_test)))
