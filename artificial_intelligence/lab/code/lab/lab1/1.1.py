# 导包
from sklearn import datasets
from sklearn import linear_model
from sklearn.metrics import mean_absolute_error

# 装载数据集
diabetes = datasets.load_diabetes()

# 打印数据集长度 422
print("数据集长度: ", len(diabetes.data))

# 依次切分数据为训练集和测试集
x_train = diabetes.data[:-20]
y_train = diabetes.target[:-20]
x_test = diabetes.data[-20:]
y_test = diabetes.target[-20:]

# 打印训练集的类型
print("数据集类型: ", type(x_train))
# 422,10
print("x_train.shape: ", x_train.shape)
# 422
print("y_train.shapr", y_train.shape)

# 构建线性回归模型，并进行预测
linreg = linear_model.LinearRegression()
linreg.fit(x_train, y_train)
linreg.predict(x_test)

# 训练集标准差差
std_train = mean_absolute_error(y_train, linreg.predict(x_train))
# 验证集标准差
std_test = mean_absolute_error(y_test, linreg.predict(x_test))

# 打印输出最后的结果
print("std_train: ", std_train, "std_test: ", std_test)
