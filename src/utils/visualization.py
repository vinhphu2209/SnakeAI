import matplotlib.pyplot as plt
import numpy as np

def plot_training_results(scores, avg_scores, title="Training Results"):
    """
    Vẽ đồ thị kết quả training
    
    Args:
        scores: Danh sách điểm số sau mỗi episode
        avg_scores: Danh sách điểm trung bình
        title: Tiêu đề đồ thị
    """
    plt.figure(figsize=(10, 6))
    plt.plot(scores, label='Score')
    plt.plot(avg_scores, label='Average Score')
    plt.title(title)
    plt.xlabel('Episode')
    plt.ylabel('Score')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_agent_performance(agent_scores, title="Agent Performance Comparison"):
    """
    Vẽ đồ thị so sánh hiệu suất giữa các agent
    
    Args:
        agent_scores: Dictionary chứa điểm số của các agent
        title: Tiêu đề đồ thị
    """
    plt.figure(figsize=(10, 6))
    
    for agent_name, scores in agent_scores.items():
        plt.plot(scores, label=agent_name)
    
    plt.title(title)
    plt.xlabel('Episode')
    plt.ylabel('Score')
    plt.legend()
    plt.grid(True)
    plt.show()

def visualize_game_state(snake, food, grid_size):
    """
    Hiển thị trạng thái game
    
    Args:
        snake: Danh sách các vị trí của rắn
        food: Vị trí của thức ăn
        grid_size: Kích thước lưới game
    """
    plt.figure(figsize=(8, 8))
    
    # Vẽ lưới
    plt.grid(True)
    plt.xlim(0, grid_size)
    plt.ylim(0, grid_size)
    
    # Vẽ rắn
    snake_x = [pos[0] for pos in snake]
    snake_y = [pos[1] for pos in snake]
    plt.plot(snake_x, snake_y, 'b-', linewidth=2)
    plt.plot(snake_x[0], snake_y[0], 'bo', markersize=10)  # Đầu rắn
    
    # Vẽ thức ăn
    plt.plot(food[0], food[1], 'ro', markersize=10)
    
    plt.title('Game State')
    plt.show() 