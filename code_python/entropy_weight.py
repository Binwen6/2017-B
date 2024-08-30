import pandas as pd
import numpy as np
import math

data = pd.read_excel('../data/有效会员信息数据.xlsx')
data = data.dropna()
data = data.reset_index(drop=True)

# 计算指标1
x_1 = data['预订任务限额'].values

# 计算指标2
x_21 = data['预订任务开始时间'].values
x_2 = []
for i in range(len(x_21)):
    time_parts = x_21[i].split(':')
    minutes = int(time_parts[0]) * 60 + int(time_parts[1]) + int(time_parts[2]) / 60
    x_2.append(minutes)
x_2 = np.array(x_2) - 390


# 更新指标2
for i in range(len(x_2)):
    if x_2[i] != 0:
        x_2[i] = 1 / x_2[i]
    else:
        x_2[i] = 0.5

# 用以上计算出的指标生成一份新的表格
data_new = pd.DataFrame()
data_new['会员编号'] = data['会员编号']
data_new['指标1'] = x_1
data_new['指标2'] = x_2
data_new.to_excel('../data/会员完成能力指标.xlsx', index=False)


# 采用Min-Max标准化方法对../data/会员完成能力指标.xlsx中的指标1和指标2分别进行归一化处理， 并把处理后的数据更新到原表格中
data = pd.read_excel('../data/会员完成能力指标.xlsx')
data = data.dropna()
data = data.reset_index(drop=True)

# 归一化处理
data['指标1'] = (data['指标1'] - data['指标1'].min()) / (data['指标1'].max() - data['指标1'].min())
data['指标2'] = (data['指标2'] - data['指标2'].min()) / (data['指标2'].max() - data['指标2'].min())
data.to_excel('../data/会员完成能力指标.xlsx', index=False)

# 分别计算每位会员指标1和指标2占所有会员的比重，并根据比重计算每个指标的熵值，从而得到信息熵冗余度，最终得到各指标的权值
data = pd.read_excel('../data/会员完成能力指标.xlsx')
data = data.dropna()
data = data.reset_index(drop=True)

# 计算指标1和指标2的比重
p_1 = data['指标1'].values / data['指标1'].sum()
p_2 = data['指标2'].values / data['指标2'].sum()

# 遍历会员编号进行比重计算操作
for i in range(len(data)):
    member_id = data.loc[i, '会员编号']
    data.loc[i, '指标1比重'] = p_1[i]
    data.loc[i, '指标2比重'] = p_2[i]

print(data)
# 存储比重数据
data.to_excel('../data/会员完成能力指标.xlsx', index=False)



# Ensure correct normalization
data['指标1'] = (data['指标1'] - data['指标1'].min()) / (data['指标1'].max() - data['指标1'].min())
data['指标2'] = (data['指标2'] - data['指标2'].min()) / (data['指标2'].max() - data['指标2'].min())

# Calculate proportions
p_1 = data['指标1'] / data['指标1'].sum()
p_2 = data['指标2'] / data['指标2'].sum()

# Calculate entropy
K = 1 / np.log(len(data))
e_1 = -K * np.sum(p_1 * np.log(p_1 + 1e-10))  # Adding a tiny value to avoid log(0)
e_2 = -K * np.sum(p_2 * np.log(p_2 + 1e-10))

# Calculate redundancy and weights
r_1 = 1 - e_1
r_2 = 1 - e_2
w_1 = r_1 / (r_1 + r_2)
w_2 = r_2 / (r_1 + r_2)

print('指标1的权值为:', w_2)
print('指标2的权值为:', w_1)

# 新建一列数据
w_1 = 0.6507
w_2 = 0.3493
data['cp'] = w_1 * data['指标1'] + w_2 * data['指标2']
data.to_excel('../data/会员完成能力指标.xlsx', index=False)