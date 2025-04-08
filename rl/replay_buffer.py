import numpy as np
from collections import deque
import random

class ReplayBuffer:
    def __init__(self, max_size=10000):
        """
        Khởi tạo replay buffer
        
        Args:
            max_size: Kích thước tối đa của buffer
        """
        self.buffer = deque(maxlen=max_size)
        
    def push(self, state, action, reward, next_state, done):
        """
        Thêm experience vào buffer
        
        Args:
            state: Trạng thái hiện tại
            action: Hành động đã thực hiện
            reward: Điểm thưởng nhận được
            next_state: Trạng thái tiếp theo
            done: Game kết thúc hay chưa
        """
        self.buffer.append((state, action, reward, next_state, done))
        
    def sample(self, batch_size):
        """
        Lấy ngẫu nhiên một batch experience từ buffer
        
        Args:
            batch_size: Kích thước batch
            
        Returns:
            states: Mảng các trạng thái
            actions: Mảng các hành động
            rewards: Mảng các điểm thưởng
            next_states: Mảng các trạng thái tiếp theo
            dones: Mảng các trạng thái kết thúc
        """
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        return np.array(states), np.array(actions), np.array(rewards), np.array(next_states), np.array(dones)
        
    def __len__(self):
        """Trả về số lượng experience trong buffer"""
        return len(self.buffer) 