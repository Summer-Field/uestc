# 导包
import numpy as np
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
import dataProcess
from tensorflow.keras import Sequential, layers, optimizers, losses
from sklearn.model_selection import KFold, StratifiedKFold

# SVM模型搭建、训练、预估
class SVM_model(object):
    def __init__(self, FILE):
        self.train_X, self.train_y, self.test_X, self.test_y = dataProcess.read_file(FILE)
        self.train_X, self.test_X = dataProcess.process(self.train_X, self.test_X)
        self.train_y = np.squeeze(self.train_y)
        self.clf = SVC(gamma=0.01, kernel='rbf')
    def train(self):
        self.clf.fit(self.train_X, self.train_y)
    def evaluate(self):
        y_pred = self.clf.predict(self.test_X)
        Precision = metrics.precision_score(self.test_y, y_pred)
        Recall = metrics.recall_score(self.test_y, y_pred)
        print('Precision of SVC:', Precision)
        print('Recall of SVC:', Recall)

# LR模型搭建、训练、预估
class LR(object):
    def __init__(self, FILE):
        self.train_X, self.train_y, self.test_X, self.test_y = dataProcess.read_file(FILE)
        self.train_X, self.test_X = dataProcess.process(self.train_X, self.test_X)
        self.train_y = np.squeeze(self.train_y)
        self.lr = LogisticRegression(C=10.0, random_state=0)
    def train(self):
        self.lr.fit(self.train_X, self.train_y)
    def evaluate(self):
        y_pred = self.lr.predict(self.test_X)
        Precision = metrics.precision_score(self.test_y, y_pred)
        Recall = metrics.recall_score(self.test_y, y_pred)
        print('Precision of LR:', Precision)
        print('Recall of LR:', Recall)

# 深度学习模型搭建、训练、预估
class DeepLearning(object):
    def __init__(self, FILE):
        self.train_X, self.train_y, self.test_X, self.test_y = dataProcess.read_file(FILE)
        self.train_X, self.test_X = dataProcess.process(self.train_X, self.test_X)

    def build_model(self, lr=0.001):
        model = Sequential(
            [
                layers.InputLayer(input_shape=(4,)),
                layers.Dense(64, activation='relu'),
                layers.Dense(32, activation='relu'),
                layers.Dense(1, activation='sigmoid')
            ]
        )
        model.compile(
            optimizer=optimizers.Adam(lr),
            loss=losses.BinaryCrossentropy(),
            metrics=['Precision', 'Recall']
        )
        # model.summary()
        return model
    def train(self):
        kf = StratifiedKFold(n_splits=5, shuffle=True)
        y_pred_all = []
        for train_idx, test_idx in kf.split(self.train_X, self.train_y):
            x_train, x_dev = self.train_X[train_idx], self.train_X[test_idx]
            y_train, y_dev = self.train_y[train_idx], self.train_y[test_idx]
            model = self.build_model()
            model.fit(x_train, y_train, epochs=5, batch_size=16, validation_data=(x_dev, y_dev))
            y_pred = model.predict(self.test_X)
            # print(y_pred.shape)
            y_pred_all.append(list(np.squeeze(y_pred)))
        print(y_pred_all)
        for preds in y_pred_all:
            for index, num in enumerate(preds):
                preds[index] = 0 if num <= 0.5 else 1
        y_pred_all = np.array(y_pred_all)
        y_pred_vote = []
        for i in range(len(y_pred_all[0])):
            one = np.count_nonzero(y_pred_all[:, i])
            zero = 5 - one
            y_pred_vote.append(1 if one > zero else 0)
        Precision = metrics.precision_score(self.test_y, y_pred_vote)
        Recall = metrics.recall_score(self.test_y, y_pred_vote)
        print('Precision of MLP:', Precision)
        print('Recall of MLP:', Recall)

