import pygame
import sys
import torch
from environment.snake_env import SnakeEnv
from agents.dqn_agent import DQNAgent

def play(env, agent, model_path=None):
    """
    Chơi game với agent đã được huấn luyện
    
    Args:
        env: Môi trường
        agent: Agent
        model_path: Đường dẫn đến model đã được huấn luyện
    """
    # Load model nếu có
    if model_path:
        agent.load(model_path)
        agent.epsilon = 0.0  # Không cần exploration khi chơi
        
    # Khởi tạo pygame
    pygame.init()
    screen = pygame.display.set_mode((env.cell_number * env.cell_size, env.cell_number * env.cell_size))
    clock = pygame.time.Clock()
    
    # Reset môi trường
    state = env.reset()
    done = False
    score = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        # Chọn hành động
        action = agent.act(state)
        
        # Thực hiện hành động
        next_state, reward, done, info = env.step(action)
        
        # Cập nhật state và score
        state = next_state
        score += reward
        
        # Vẽ môi trường
        env.render(screen)
        
        # Hiển thị score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        pygame.display.update()
        clock.tick(10)  # 10 FPS
        
        if done:
            print(f"Game Over! Score: {score}")
            break
            
if __name__ == "__main__":
    # Khởi tạo môi trường
    env = SnakeEnv()
    
    # Khởi tạo agent
    state_shape = (env.cell_number, env.cell_number)
    n_actions = 4  # lên, xuống, trái, phải
    agent = DQNAgent(state_shape, n_actions)
    
    # Chơi game
    play(env, agent, model_path="models/snake_dqn_1000.pth")  # Thay đổi đường dẫn model tùy ý 