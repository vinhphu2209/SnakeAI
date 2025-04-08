import numpy as np

def preprocess_state(state):
    """
    Tiền xử lý trạng thái game để phù hợp với input của neural network
    
    Args:
        state: Trạng thái game hiện tại
        
    Returns:
        processed_state: Trạng thái đã được xử lý
    """
    # Chuyển đổi state thành numpy array
    state_array = np.array(state)
    
    # Chuẩn hóa giá trị về khoảng [0, 1]
    processed_state = state_array / 255.0
    
    return processed_state

def get_state_features(snake, food, grid_size):
    """
    Trích xuất các đặc trưng từ trạng thái game
    
    Args:
        snake: Danh sách các vị trí của rắn
        food: Vị trí của thức ăn
        grid_size: Kích thước lưới game
        
    Returns:
        features: Dictionary chứa các đặc trưng
    """
    head = snake[0]
    
    # Tính khoảng cách từ đầu rắn đến thức ăn
    food_distance = np.sqrt((head[0] - food[0])**2 + (head[1] - food[1])**2)
    
    # Kiểm tra va chạm với tường
    wall_collision = (
        head[0] <= 0 or 
        head[0] >= grid_size - 1 or 
        head[1] <= 0 or 
        head[1] >= grid_size - 1
    )
    
    # Kiểm tra va chạm với thân rắn
    body_collision = head in snake[1:]
    
    return {
        'food_distance': food_distance,
        'wall_collision': wall_collision,
        'body_collision': body_collision,
        'snake_length': len(snake)
    } 