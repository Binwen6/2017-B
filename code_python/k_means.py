from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import pandas as pd

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

# Save the plt
fig.savefig('../fig/k_means.png')

# 将每个任务所属的簇保存到文件data/有效已结束项目任务位置数据.xlsx
df.to_excel('../data/有效已结束项目任务位置数据.xlsx', index=False)

# 根据每个任务的经纬度计算该任务点与其所属簇的中心点的距离
df['distance'] = 0
for i in range(4):
    df['distance'] = df.apply(lambda x: (x['任务gps经度'] - centers[i][0]) ** 2 + (x['任务gps 纬度'] - centers[i][1]) ** 2, axis=1)
df.to_excel('../data/有效已结束项目任务位置数据.xlsx', index=False)

