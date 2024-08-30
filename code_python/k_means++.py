from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

# Set the random seed for reproducibility
np.random.seed(42)

df = pd.read_excel('../data/有效已结束项目任务位置数据.xlsx')
# Standardize the data
scaler = StandardScaler()
data = df[['任务gps经度', '任务gps 纬度']]
data = scaler.fit_transform(data)

# Perform K-means clustering
kmeans = KMeans(n_clusters=150)
df['cluster'] = kmeans.fit_predict(data)

centers = kmeans.cluster_centers_
# Inverse transform the cluster centers to the original scale
centers = scaler.inverse_transform(centers)
print(centers)

# Plot the clusters
fig, ax = plt.subplots()
for i in range(150):
    points = df[df['cluster'] == i]
    ax.scatter(points['任务gps经度'], points['任务gps 纬度'])
    ax.scatter(centers[i][0], centers[i][1], c='black', marker='x')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('K-means Clustering of Task Data')
plt.show()

# 绘制每一聚类簇中所包含任务数量的条形统计图
cluster_counts = df['cluster'].value_counts()
plt.bar(cluster_counts.index, cluster_counts.values)
plt.xlabel('Cluster')
plt.ylabel('Number of Tasks')
plt.title('Task Count per Cluster')
# save the bar
plt.savefig('../fig/k_means++_bar.png')
plt.show()

# Save the plot
fig.savefig('../fig/k_means++.png')





