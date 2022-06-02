# 导包
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import numpy as np

# 装载数据集
iris = load_iris()
# 打印数据shape
print("iris.data.shape: ", iris.data.shape)
print("iris.target.shape: ", iris.target.shape)

# 切分数据集
x = iris.data
y = iris.target
x = StandardScaler().fit_transform(x)

# 构建逻辑回归模型，并训练模型
lr = LogisticRegression()
lr.fit(x, y.ravel())

# 计算acc
y_hat = lr.predict(x)
print("y_hat.shape: ", y_hat.shape)
result = y_hat == y
acc = np.mean(result)
print('准确度: %.2f%%' % (100 * acc))