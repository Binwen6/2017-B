% 读取 CSV 文件
data = readtable('task_data_for_matlab.csv');

% 提取数据
x = data.lng;
y = data.lat;
z = data.price;

% 打开 CFTOOL
cftool(x, y, z)

ft = fittype('a*x^2 + b*y^2 + c*x*y + d*x + e*y + f');
[fitresult, gof] = fit([x, y], z, ft);