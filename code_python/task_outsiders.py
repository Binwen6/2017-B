import numpy as np
import pandas as pd
from scipy.stats import kstest
from scipy.special import boxcox1p
from scipy.stats import boxcox_normmax
from scipy.special import inv_boxcox

# 将附件一.xlsx中的数据读取到dataframe中
df = pd.read_excel('../data/附件一：已结束项目任务数据.xls')
print(df)

# 对dataframe中的其中标签为“经度”“纬度”两列数据依据3sigma准则进行剔除进行异常值剔除（似的剔除异常值后对dataframe不再包括异常值所在行），并打印出异常值
# Calculate mean and standard deviation for longitude and latitude columns
mean_longitude = df['任务gps经度'].mean()
std_longitude = df['任务gps经度'].std()
mean_latitude = df['任务gps 纬度'].mean()
std_latitude = df['任务gps 纬度'].std()

# Identify outliers using 3-sigma rule for longitude column
outliers_longitude = df[(df['任务gps经度'] - mean_longitude) > 3 * std_longitude]
# Remove outliers from longitude column
df = df[(df['任务gps经度'] - mean_longitude) <= 3 * std_longitude]

# Identify outliers using 3-sigma rule for latitude column
outliers_latitude = df[(df['任务gps 纬度'] - mean_latitude) > 3 * std_latitude]
# Remove outliers from latitude column
df = df[(df['任务gps 纬度'] - mean_latitude) <= 3 * std_latitude]

# Print outliers
print("Outliers in longitude column:")
print(outliers_longitude)
print("Outliers in latitude column:")
print(outliers_latitude)
# 将剩余的df重新编号
df.reset_index(drop=True, inplace=True)
print(df)


# 主要是高纬异常值
# 将df除制定标签外的多余列删去
df.drop(['任务号码','任务标价','任务执行情况'], axis=1, inplace=True)
# 将df导出为excel
df.to_excel('../data/已结束项目任务数据(精简版).xlsx', index=False)