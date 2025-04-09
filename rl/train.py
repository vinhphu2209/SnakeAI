import os
import torch
from snake_env import SnakeEnv
from dqn_agent import DQNAgent

def train():
    # Khởi tạo môi trường và agent
    env = SnakeEnv()
    state_size = 11  # Số lượng state features
    action_size = 3  # Straight, Right, Left
    agent = DQNAgent(state_size, action_size)
    
    # Các tham số huấn luyện
    episodes = 5000
    batch_size = 64
    save_interval = 250
    best_score = 0
    
    # Tạo thư mục models nếu chưa tồn tại
    if not os.path.exists('models'):
        os.makedirs('models')
    
    # Huấn luyện
    for episode in range(episodes):
        state = env.reset()
        total_reward = 0
        done = False
        
        while not done:
            # Chọn hành động
            action = agent.act(state)
            
            # Thực hiện hành động
            next_state, reward, done, _ = env.step(action)
            
            # Lưu experience vào memory
            agent.remember(state, action, reward, next_state, done)
            
            # Cập nhật state
            state = next_state
            total_reward += reward
            
            # Render game
            env.render()
            
            # Huấn luyện model
            agent.replay(batch_size)
        
        # In thông tin episode
        print(f"Episode: {episode + 1}/{episodes}, Score: {env.score}, Total Reward: {total_reward:.2f}, Epsilon: {agent.epsilon:.2f}")
        
        # Lưu model mỗi save_interval episodes
        if (episode + 1) % save_interval == 0:
            agent.save(f'models/model_{episode + 1}.pth')
            print(f"Model saved at episode {episode + 1}")
        
        # Lưu best model
        if env.score > best_score:
            best_score = env.score
            agent.save('models/best_model.pth')
            print(f"New best model saved with score {best_score}")
    
    # Đóng môi trường
    env.close()

if __name__ == "__main__":
    train() 