# 导包
import numpy as np
from sklearn import metrics
from sklearn import linear_model
from sklearn.svm import SVR
import dataProcess
from tensorflow.keras import Sequential, layers, optimizers, losses
import matplotlib.pyplot as plt

# Linear Regression Model
class LR(object):
    def __init__(self, FILE):
        self.train_X, self.train_y, self.test_X, self.test_y = dataProcess.read_file(FILE)
        self.linreg = linear_model.LinearRegression()

    def train(self):
        self.linreg.fit(self.train_X, self.train_y)
        print('截距: ', self.linreg.intercept_)
        print('系数: ', self.linreg.coef_)
    def evaluate(self):
        y_pred = self.linreg.predict(self.test_X)
        MSE_score = metrics.mean_squared_error(self.test_y, y_pred)
        RMSE_score = np.sqrt(metrics.mean_squared_error(self.test_y, y_pred))
        print('MSE of LR: ', MSE_score)
        print('RMSE of LR: ', RMSE_score)

# SVM with rbf Model
class SVM_model_rbf(object):
    def __init__(self, FILE):
        self.train_X, self.train_y, self.test_X, self.test_y = dataProcess.read_file(FILE)
        self.train_y = np.squeeze(self.train_y)
        self.rbf_svr = SVR(kernel='rbf')
    def train(self):
        self.rbf_svr.fit(self.train_X, self.train_y)
    def evaluate(self):
        y_pred = self.rbf_svr.predict(self.test_X)
        MSE_score = metrics.mean_squared_error(self.test_y, y_pred)
        RMSE_score = np.sqrt(metrics.mean_squared_error(self.test_y, y_pred))
        print('MSE of rbf:', MSE_score)
        print('RMSE of rbf:', RMSE_score)

# linear SVM Model
class SVM_model_linear(object):
    def __init__(self, FILE):
        self.train_X, self.train_y, self.test_X, self.test_y = dataProcess.read_file(FILE)
        self.train_y = np.squeeze(self.train_y)
        self.linear_svr = SVR(kernel='linear')
    def train(self):
        self.linear_svr.fit(self.train_X, self.train_y)
    def evaluate(self):
        y_pred = self.linear_svr.predict(self.test_X)
        MSE_score = metrics.mean_squared_error(self.test_y, y_pred)
        RMSE_score = np.sqrt(metrics.mean_squared_error(self.test_y, y_pred))
        print('MSE of linear:', MSE_score)
        print('RMSE of linear:', RMSE_score)

# DeepLearning Model
class DeepLearning(object):
    def __init__(self, FILE):
        self.train_X, self.train_y, self.test_X, self.test_y = dataProcess.read_file(FILE)
    def build_model(self, lr=0.1):
        model = Sequential(
            [
                layers.InputLayer(input_shape=(3,)),
                # layers.Dense(64, activation='relu'),
                layers.Dense(32, activation='relu'),
                layers.Dense(1)
            ]
        )
        model.compile(
            optimizer=optimizers.Adam(lr=lr),
            loss=losses.MeanSquaredError(),
            metrics=['mse', 'acc']
        )
        model.summary()
        return model
    def train(self):
        model = self.build_model()
        model.fit(self.train_X, self.train_y, epochs=40, batch_size=16)
        model.evaluate(self.test_X, self.test_y)
        y_pred = model.predict(self.test_X)
        y_pred = np.squeeze(y_pred)
        self.test_y = np.squeeze(self.test_y)
        x = [i for i in range(len(y_pred))]
        plt.figure()
        plt.plot(x, y_pred, label='predict', color='red')
        plt.plot(x, self.test_y, label='true', color='blue')
        plt.legend(loc=2)
        plt.show()


