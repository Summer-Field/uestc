# 导包
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import metrics

# 装载数据集
path = 'Data_for_Cluster.npz'
data = np.load(path)
X = data['X']
y = data['labels_true']
print("X.shape: ", X.shape)
print("y.shape: ", y.shape)

# 数据可视化 - 数据散点图
plt.scatter(X[:, 0], X[:, 1], c=y)
plt.show()

# 搭建数据集
n_clusters = 3
cls = KMeans(n_clusters).fit(X)

# 模型训练
y_pre = cls.predict(X)
n_samples, n_features = X.shape  # 总样本量，总特征数
inertias = cls.inertia_  # 获取聚类准则的总和
silhouette_s = metrics.silhouette_score(X, y_pre, metric='euclidean')  # 平均轮廓系数
print("平均轮廓系数: ", silhouette_s)
centers = cls.cluster_centers_  # 各类别中心
print("centers: ", centers)

# 结果可视化
colors = ['b', 'g', 'r']
plt.figure()  # 建立画布
for i in range(n_clusters):  # 循环读取类别
    index_sets = np.where(y_pre == i)  # 找到相同类的索引集合、
    cluster = X[index_sets]  # 将相同类的数据划分为一个聚类子集
    plt.scatter(cluster[:, 0], cluster[:, 1], c=colors[i], marker='.')  # 展示聚类子集内的样本点
    plt.plot(centers[i][0], centers[i][1], '*', markerfacecolor=colors[i], markeredgecolor='k', markersize=6)
plt.show()