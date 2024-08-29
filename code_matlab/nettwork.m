function [net, y0, Y1] = nettwork(P, goal, t)
% BP 神经网络算法

% 创建神经网络
input_size = size(P, 1);
output_size = size(goal, 1);
net = newff(minmax(P), [10, output_size], {'tansig', 'purelin'}, 'trainlm');

% 设置训练参数
net.trainParam.show = 10;
net.trainParam.lr = 0.05;
net.trainParam.goal = 1e-10;
net.trainParam.epochs = 5000;

% 训练网络
net = train(net, P, goal);

% 使用训练好的网络进行预测
y0 = sim(net, P);

% 对测试数据进行预测
Y1 = sim(net, t);

% 对第二个输出进行二值化处理
for i = 1:size(Y1, 2)
    if abs(Y1(2,i) - 0) < abs(Y1(2,i) - 1)
        Y1(2,i) = 0;
    else
        Y1(2,i) = 1;
    end
end

% 转置结果矩阵
Y1 = Y1';
end