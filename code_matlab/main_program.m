% 主程序

% 构造输入数据
input_size = 3;
output_size = 2;
num_samples = 100;

% 随机生成输入数据
P = rand(input_size, num_samples);

% 生成目标输出数据
goal = zeros(output_size, num_samples);
goal(1,:) = sin(P(1,:) + P(2,:));  % 第一个输出是前两个输入的正弦
goal(2,:) = round(rand(1, num_samples));  % 第二个输出是随机的0或1

% 生成测试数据
t = rand(input_size, 150);

% 调用神经网络函数
[net, y0, Y1] = nettwork(P, goal, t);

% 显示结果
disp('训练数据的预测结果:');
disp(y0);
disp('测试数据的预测结果:');
disp(Y1);

% 绘制结果
figure;
subplot(2,1,1);
plot(goal(1,:), 'b-', 'LineWidth', 2);
hold on;
plot(y0(1,:), 'r--', 'LineWidth', 2);
title('第一个输出的比较 (训练数据)');
legend('目标', '预测');

subplot(2,1,2);
plot(goal(2,:), 'b-', 'LineWidth', 2);
hold on;
plot(y0(2,:), 'r--', 'LineWidth', 2);
title('第二个输出的比较 (训练数据)');
legend('目标', '预测');