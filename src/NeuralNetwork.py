import torch.nn as nn 
import torch.nn.functional as F

# class NN(nn.Module):
#     def __init__(self, input_size, ouput_size):
#         super(NN, self).__init__()
#         self.fc1 = nn.Linear(input_size, 64)
#         self.fc2 = nn.Linear(64, 64)
#         self.fc3 = nn.Linear(64, 64)
#         self.fc4 = nn.Linear(64, ouput_size)
#         self._create_weights()
#     def _create_weights(self):
#         for m in self.modules():
#             if isinstance(m, nn.Linear):
#                 nn.init.xavier_uniform_(m.weight)
#                 nn.init.constant_(m.bias, 0)
#     def forward(self, x):
#         x = F.relu(self.ln1(self.fc1(x)))
#         x = F.relu(self.ln2(self.fc2(x)))
#         x = F.relu(self.ln3(self.fc3(x)))
#         return self.fc4(x)

class NN(nn.Module):
    def __init__(self, input_size, output_size):
        super(NN, self).__init__()
        self.conv1 = nn.Sequential(nn.Linear(input_size, 64), nn.ReLU(inplace=True))
        self.conv2 = nn.Sequential(nn.Linear(64, 64), nn.ReLU(inplace=True))
        self.conv3 = nn.Sequential(nn.Linear(64, output_size))
        self._create_weights()
    def _create_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                nn.init.constant_(m.bias, 0)
    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)

        return x

