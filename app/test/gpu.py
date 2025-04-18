# -*- coding: utf-8 -*-
# @Time    : 2024/12/26 09:45
# @Author  : Wu WanJie
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import time
from torch.cuda.amp import autocast, GradScaler  # 用于混合精度训练

# 定义一个更大的神经网络模型
class LargeModel(nn.Module):
    """
    large model with increased size for maxing out GPU memory
    """
    def __init__(self):
        super(LargeModel, self).__init__()
        self.layer1 = nn.Linear(784, 8192*2)  # 增大隐藏层大小
        self.layer2 = nn.Linear(8192*2, 8192*2)
        self.layer3 = nn.Linear(8192*2, 8192*2)
        self.layer4 = nn.Linear(8192*2, 8192)
        self.output = nn.Linear(8192, 128)  # 假设是一个10分类问题

    def forward(self, x):
        x = torch.relu(self.layer1(x))
        x = torch.relu(self.layer2(x))
        x = torch.relu(self.layer3(x))
        x = torch.relu(self.layer4(x))
        x = self.output(x)
        return x


# 生成一些假的数据来进行训练
def generate_fake_data():
    # 假设数据为28x28的图像，展平后为784个特征
    X = torch.randn(50000, 784)  # 增加样本数量以增加训练负载
    y = torch.randint(0, 128, (50000,))  # 10个类别
    return X, y


# 创建数据加载器
X, y = generate_fake_data()
dataset = TensorDataset(X, y)
train_loader = DataLoader(dataset, batch_size=512, shuffle=True)  # 增大批处理大小

# 初始化模型、损失函数和优化器
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = LargeModel().to(device)

# 使用数据并行以利用两个GPU
model = nn.DataParallel(model)

# 损失函数和优化器
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 初始化混合精度训练的Scaler
scaler = GradScaler()

# 用于记录训练时间
start_time = time.time()

# 训练模型
num_epochs = 1000000  # 设置一个非常长的训练时间
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for i, (inputs, labels) in enumerate(train_loader):
        inputs, labels = inputs.to(device), labels.to(device)

        # 混合精度训练
        optimizer.zero_grad()
        with autocast():  # 开启自动混合精度
            outputs = model(inputs)
            loss = criterion(outputs, labels)

        # 反向传播和优化
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()

        running_loss += loss.item()

    # 每隔一定的epoch打印一次损失和训练时间
    if (epoch + 1) % 10 == 0:
        print(f"Epoch [{epoch + 1}/{num_epochs}], Loss: {running_loss / len(train_loader):.4f}")

    # 每100个epoch后输出训练时间，观察是否稳定
    if (epoch + 1) % 100 == 0:
        elapsed_time = time.time() - start_time
        print(f"Elapsed time: {elapsed_time / 60:.2f} minutes")

    # 你可以在这里加入GPU温度监测的逻辑

print("Finished Training!")
