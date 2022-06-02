# 导包
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.cluster import DBSCAN

# 装载数据
path = 'Data_for_Cluster.npz'
data = np.load(path)
X = data['X']
y = data['labels_true']

# 模型训练
dbscan = DBSCAN(eps=0.34, min_samples=20).fit(X)
y_pre = dbscan.labels_

# 数据可视化
plt.scatter(X[:, 0], X[:, 1], c=y_pre)
plt.show()

# 模型评估
score = metrics.silhouette_score(X, y_pre)
print("平均轮廓系数: ", score)
