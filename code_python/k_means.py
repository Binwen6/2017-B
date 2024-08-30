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
kmeans = KMeans(n_clusters=4)
df['cluster'] = kmeans.fit_predict(data)

centers = kmeans.cluster_centers_
# Inverse transform the cluster centers to the original scale
centers = scaler.inverse_transform(centers)
print(centers)

# Plot the clusters
fig, ax = plt.subplots()
colors = ['red', 'green', 'blue', 'yellow']
for i in range(4):
    points = df[df['cluster'] == i]
    ax.scatter(points['任务gps经度'], points['任务gps 纬度'], c=colors[i])
    ax.scatter(centers[i][0], centers[i][1], c='black', marker='x')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('K-means Clustering of Task Data')
plt.show()

# Save the plot
fig.savefig('../fig/k_means.png')

# 对于每个任务, 根据他的经纬度和他所属cluster的经纬度计算，一个距离存到新的一列distance中
df['distance'] = 0
for i in range(4):
    points = df[df['cluster'] == i]
    center = centers[i]
    for index, row in points.iterrows():
        distance = ((row['任务gps经度'] - center[0]) ** 2 + (row['任务gps 纬度'] - center[1]) ** 2) ** 0.5
        df.loc[index, 'distance'] = distance
        

# 将每个任务所属的簇保存到文件data/有效已结束项目任务位置数据.xlsx
df.to_excel('../data/有效已结束项目任务位置数据.xlsx', index=False)
