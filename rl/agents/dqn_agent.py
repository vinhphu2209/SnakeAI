import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from collections import deque
from .base_agent import BaseAgent

class DQN(nn.Module):
    def __init__(self, input_shape, n_actions):
        super(DQN, self).__init__()
        
        # CNN layers với batch normalization để tăng tốc độ training
        self.conv = nn.Sequential(
            nn.Conv2d(1, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU()
        )
        
        # Fully connected layers
        conv_out_size = self._get_conv_out(input_shape)
        self.fc = nn.Sequential(
            nn.Linear(conv_out_size, 1024),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(512, n_actions)
        )
        
    def _get_conv_out(self, shape):
        o = self.conv(torch.zeros(1, 1, *shape))
        return int(np.prod(o.size()))
        
    def forward(self, x):
        conv_out = self.conv(x).view(x.size()[0], -1)
        return self.fc(conv_out)

class DQNAgent(BaseAgent):
    def __init__(self, state_shape, n_actions, device="cuda"):
        super().__init__(state_shape, n_actions)
        self.device = device
        
        # Khởi tạo mạng neural
        self.policy_net = DQN(state_shape, n_actions).to(device)
        self.target_net = DQN(state_shape, n_actions).to(device)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        
        # Khởi tạo optimizer với learning rate cao hơn
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=0.001)
        
        # Các tham số
        self.gamma = 0.99  # discount factor
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.batch_size = 128  # Tăng batch size để tận dụng GPU
        self.memory = deque(maxlen=100000)  # Tăng memory size
        
    def act(self, state, epsilon=None):
        """
        Chọn hành động dựa trên state hiện tại
        
        Args:
            state: Trạng thái hiện tại
            epsilon: Xác suất chọn hành động ngẫu nhiên
            
        Returns:
            action: Hành động được chọn
        """
        if epsilon is None:
            epsilon = self.epsilon
            
        if random.random() < epsilon:
            return random.randrange(self.n_actions)
            
        with torch.no_grad():
            state = torch.FloatTensor(state).unsqueeze(0).unsqueeze(0).to(self.device)
            q_values = self.policy_net(state)
            return q_values.argmax().item()
            
    def learn(self, state, action, reward, next_state, done):
        """
        Cập nhật policy dựa trên experience
        
        Args:
            state: Trạng thái hiện tại
            action: Hành động đã thực hiện
            reward: Điểm thưởng nhận được
            next_state: Trạng thái tiếp theo
            done: Game kết thúc hay chưa
        """
        # Lưu experience vào memory
        self.memory.append((state, action, reward, next_state, done))
        
        # Nếu chưa đủ batch_size thì không train
        if len(self.memory) < self.batch_size:
            return
            
        # Lấy batch từ memory
        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        
        # Chuyển sang tensor và đưa lên GPU
        states = torch.FloatTensor(states).unsqueeze(1).to(self.device)
        actions = torch.LongTensor(actions).unsqueeze(1).to(self.device)
        rewards = torch.FloatTensor(rewards).unsqueeze(1).to(self.device)
        next_states = torch.FloatTensor(next_states).unsqueeze(1).to(self.device)
        dones = torch.FloatTensor(dones).unsqueeze(1).to(self.device)
        
        # Tính Q(s,a)
        current_q_values = self.policy_net(states).gather(1, actions)
        
        # Tính max Q(s',a')
        with torch.no_grad():
            next_q_values = self.target_net(next_states).max(1)[0].unsqueeze(1)
            target_q_values = rewards + (1 - dones) * self.gamma * next_q_values
            
        # Tính loss và cập nhật weights
        loss = nn.MSELoss()(current_q_values, target_q_values)
        self.optimizer.zero_grad()
        loss.backward()
        # Gradient clipping để tránh exploding gradients
        torch.nn.utils.clip_grad_norm_(self.policy_net.parameters(), 1.0)
        self.optimizer.step()
        
        # Cập nhật epsilon
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
        
    def update_target_network(self):
        """Cập nhật target network"""
        self.target_net.load_state_dict(self.policy_net.state_dict())
        
    def save(self, path):
        """Lưu model vào file"""
        torch.save({
            'policy_net_state_dict': self.policy_net.state_dict(),
            'target_net_state_dict': self.target_net.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'epsilon': self.epsilon
        }, path)
        
    def load(self, path):
        """Load model từ file"""
        checkpoint = torch.load(path, map_location=self.device)
        self.policy_net.load_state_dict(checkpoint['policy_net_state_dict'])
        self.target_net.load_state_dict(checkpoint['target_net_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.epsilon = checkpoint['epsilon'] 