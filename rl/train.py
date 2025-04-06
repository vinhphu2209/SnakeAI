import os
import torch
import numpy as np
import matplotlib.pyplot as plt
import sys
import pygame
import time

# Thêm đường dẫn gốc vào sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from rl.environment.snake_env import SnakeEnv
from rl.agents.dqn_agent import DQNAgent

def train(env, agent, n_episodes=5000, target_update=10, save_path="models", render=False, 
          target_score=50, early_stop_episodes=100):
    """
    Huấn luyện agent
    
    Args:
        env: Môi trường
        agent: Agent
        n_episodes: Số episode huấn luyện
        target_update: Tần suất cập nhật target network
        save_path: Đường dẫn lưu model
        render: Có hiển thị giao diện hay không
        target_score: Điểm số mục tiêu để dừng sớm
        early_stop_episodes: Số episodes liên tiếp đạt điểm cao để dừng
    """
    # Tạo thư mục lưu model nếu chưa tồn tại
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        
    # Lưu trữ kết quả
    scores = []
    avg_scores = []
    best_score = -np.inf
    consecutive_high_scores = 0
    
    # Thông tin về GPU
    print("\nThông tin GPU:")
    print(f"GPU có sẵn: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"Tên GPU: {torch.cuda.get_device_name(0)}")
        print(f"Bộ nhớ GPU đã sử dụng: {torch.cuda.memory_allocated(0)/1024**2:.2f} MB")
        print(f"Bộ nhớ GPU tối đa: {torch.cuda.max_memory_allocated(0)/1024**2:.2f} MB")
    
    # Training loop
    start_time = time.time()
    for episode in range(n_episodes):
        state = env.reset()
        done = False
        score = 0
        steps = 0
        episode_start_time = time.time()
        
        while not done:
            # Xử lý sự kiện pygame nếu đang render
            if render:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        env.close()
                        return scores, avg_scores
                        
            # Chọn hành động
            action = agent.act(state)
            
            # Thực hiện hành động
            next_state, reward, done, info = env.step(action)
            
            # Cập nhật agent
            agent.learn(state, action, reward, next_state, done)
            
            state = next_state
            score += reward
            steps += 1
            
            # Cập nhật target network
            if steps % target_update == 0:
                agent.update_target_network()
                
            # Render nếu cần
            if render:
                env.render()
                pygame.time.delay(50)  # Giới hạn tốc độ
                
        # Tính thời gian và tốc độ
        episode_time = time.time() - episode_start_time
        steps_per_second = steps / episode_time if episode_time > 0 else 0
        
        # Lưu kết quả
        scores.append(score)
        avg_score = np.mean(scores[-100:])
        avg_scores.append(avg_score)
        
        # Kiểm tra điều kiện dừng sớm
        if avg_score >= target_score:
            consecutive_high_scores += 1
            if consecutive_high_scores >= early_stop_episodes:
                print(f"\nĐạt điểm số mục tiêu {target_score} trong {early_stop_episodes} episodes liên tiếp!")
                print(f"Dừng huấn luyện sớm ở episode {episode}")
                break
        else:
            consecutive_high_scores = 0
        
        # In thông tin
        print(f"Episode: {episode}, Score: {score:.2f}, Avg Score: {avg_score:.2f}, "
              f"Epsilon: {agent.epsilon:.2f}, Steps: {steps}, "
              f"Time: {episode_time:.2f}s, Steps/s: {steps_per_second:.2f}")
        
        # Lưu model tốt nhất
        if score > best_score:
            best_score = score
            agent.save(os.path.join(save_path, "best_model.pth"))
            
        # Lưu model định kỳ
        if episode % 100 == 0:
            agent.save(os.path.join(save_path, f"snake_dqn_{episode}.pth"))
            
    # Tính tổng thời gian
    total_time = time.time() - start_time
    print(f"\nTổng thời gian huấn luyện: {total_time:.2f}s")
    print(f"Thời gian trung bình mỗi episode: {total_time/n_episodes:.2f}s")
    
    # Vẽ biểu đồ
    plt.figure(figsize=(10, 5))
    plt.plot(scores, alpha=0.3, label='Score')
    plt.plot(avg_scores, label='Average Score')
    plt.title("Training Progress")
    plt.xlabel("Episode")
    plt.ylabel("Score")
    plt.legend()
    plt.savefig(os.path.join(save_path, "training_progress.png"))
    plt.close()
    
    if render:
        env.close()
        
    return scores, avg_scores

if __name__ == "__main__":
    # Kiểm tra GPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # Khởi tạo môi trường
    env = SnakeEnv(render=False)  # Mặc định không render
    
    # Khởi tạo agent
    state_shape = (env.cell_number, env.cell_number)
    n_actions = 4  # lên, xuống, trái, phải
    agent = DQNAgent(state_shape, n_actions, device=device)
    
    # Huấn luyện (set render=True để xem quá trình huấn luyện)
    scores, avg_scores = train(env, agent, 
                             render=False,  # Mặc định không render
                             target_score=50,  # Điểm số mục tiêu
                             early_stop_episodes=100)  # Số episodes liên tiếp đạt điểm cao để dừng 