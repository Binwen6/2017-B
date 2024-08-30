import pandas as pd


df = pd.read_excel('../data/附件二：会员信息数据.xlsx')
print(df)


# 假设df是你的DataFrame

# 清理“会员位置(GPS)”列，移除多余的空格或逗号
df['会员位置(GPS)'] = df['会员位置(GPS)'].str.strip().str.replace(r'\s+', ' ', regex=True).str.replace(',', '')

# 检查清理后的每一行是否都能正确拆分成两列
df['拆分'] = df['会员位置(GPS)'].str.split(' ')

# 筛选出那些拆分后没有得到两列的行
invalid_rows = df[df['拆分'].apply(len) != 2]

if not invalid_rows.empty:
    print("清理后仍发现格式异常的行:")
    print(invalid_rows)
else:
    # 将'会员位置(GPS)'列拆分为两个新列：'纬度'和'经度'
    df[['纬度', '经度']] = pd.DataFrame(df['拆分'].tolist(), index=df.index)

    # 将新列的数据类型转换为浮点型
    df['纬度'] = df['纬度'].astype(float)
    df['经度'] = df['经度'].astype(float)

    # 删除临时列
    df.drop(columns=['拆分'], inplace=True)

    print(df)


# 对dataframe中的其中标签为“经度”“纬度”两列数据依据3sigma准则进行剔除进行异常值剔除（似的剔除异常值后对dataframe不再包括异常值所在行），并打印出异常值
# Calculate mean and standard deviation for longitude and latitude columns

# df中的“会员位置(GPS)”一列数据格式为“纬度（空格）经度”，请提取为两个数列


mean_latitude = df['纬度'].mean()
mean_longitude = df['经度'].mean()
std_latitude = df['纬度'].std()
std_longitude = df['经度'].std()


# Identify outliers using 3-sigma rule for longitude column
outliers_longitude = df[(df['经度'] - mean_longitude) > 3 * std_longitude]
# Remove outliers from longitude column
df = df[(df['经度'] - mean_longitude) <= 3 * std_longitude]

# Identify outliers using 3-sigma rule for latitude column
outliers_latitude = df[(df['纬度'] - mean_latitude) > 3 * std_latitude]
# Remove outliers from latitude column
df = df[(df['纬度'] - mean_latitude) <= 3 * std_latitude]

# Print outliers
print("Outliers in longitude column:")
print(outliers_longitude)
print("Outliers in latitude column:")
print(outliers_latitude)
# 将剩余的df重新编号
df.reset_index(drop=True, inplace=True)
print(df)
# Create a new dataframe with only longitude and latitude columns
new_df = df[['会员编号', '经度', '纬度', '预订任务限额', '预订任务开始时间']].copy()
new_df.to_excel('../data/有效会员信息数据.xlsx', index=False)

