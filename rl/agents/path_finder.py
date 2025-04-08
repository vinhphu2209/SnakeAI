import numpy as np
from collections import deque

class PathFinderAgent:
    def __init__(self):
        self.path = []
        self.current_path_index = 0

    def get_action(self, state):
        # Nếu không có đường đi hoặc đã đi hết đường, tìm đường mới
        if not self.path or self.current_path_index >= len(self.path):
            self.find_path(state)
            self.current_path_index = 0

        # Nếu vẫn không tìm được đường, di chuyển ngẫu nhiên
        if not self.path:
            return np.random.randint(0, 4)

        # Lấy hướng đi tiếp theo
        next_pos = self.path[self.current_path_index]
        current_pos = state['snake'][0]  # Vị trí đầu rắn

        # Xác định hướng đi
        dx = next_pos[0] - current_pos[0]
        dy = next_pos[1] - current_pos[1]

        # Chuyển hướng thành action (0: lên, 1: phải, 2: xuống, 3: trái)
        if dx == 1:
            action = 1  # phải
        elif dx == -1:
            action = 3  # trái
        elif dy == 1:
            action = 2  # xuống
        else:
            action = 0  # lên

        self.current_path_index += 1
        return action

    def find_path(self, state):
        # Lấy thông tin từ state
        snake = state['snake']
        food = state['food']
        grid_size = state['grid_size']

        # Tạo ma trận đánh dấu các ô đã thăm
        visited = np.zeros(grid_size, dtype=bool)
        for pos in snake:
            visited[pos[0], pos[1]] = True

        # Khởi tạo queue cho BFS
        queue = deque()
        queue.append((snake[0], []))  # (vị trí hiện tại, đường đi)

        # Các hướng di chuyển có thể
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        while queue:
            current_pos, path = queue.popleft()

            # Nếu đến được thức ăn
            if current_pos == food:
                self.path = path
                return

            # Thử các hướng đi
            for dx, dy in directions:
                next_x = current_pos[0] + dx
                next_y = current_pos[1] + dy

                # Kiểm tra xem có thể đi được không
                if (0 <= next_x < grid_size[0] and 
                    0 <= next_y < grid_size[1] and 
                    not visited[next_x, next_y]):
                    visited[next_x, next_y] = True
                    new_path = path + [(next_x, next_y)]
                    queue.append(((next_x, next_y), new_path))

        # Nếu không tìm được đường, để path rỗng
        self.path = [] 