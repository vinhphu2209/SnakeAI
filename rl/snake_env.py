import pygame
import numpy as np
from pygame.math import Vector2
import random
import sys
import os

class SnakeEnv:
    def __init__(self, render_mode=None):
        # Khởi tạo các tham số cấu hình cơ bản
        self.render_mode = render_mode
        self.cell_size = 40
        self.cell_number = 20
        
        # Khởi tạo pygame nếu cần render
        if self.render_mode is not None:
            pygame.mixer.pre_init(44100, -16, 2, 512)
            pygame.init()
            pygame.font.init()
            
            # Các tham số cấu hình cho render
            self.screen = pygame.display.set_mode((self.cell_number * self.cell_size, self.cell_number * self.cell_size))
            pygame.display.set_caption('Snake RL')
            
            # Khởi tạo clock
            self.clock = pygame.time.Clock()
            
            # Timer cho việc cập nhật màn hình
            self.SCREEN_UPDATE = pygame.USEREVENT
            pygame.time.set_timer(self.SCREEN_UPDATE, 100)
            
            # Load graphics
            self._load_graphics()
        
        # Khởi tạo rắn
        self.reset()
        
        # Định nghĩa action space
        self.action_space = 3  # Straight, Right, Left
        
        # Trạng thái game
        self.game_over = False
        
    def _load_graphics(self):
        # Đường dẫn đến thư mục graphics
        graphics_path = os.path.join('assets', 'graphics')
        
        # Load hình ảnh rắn
        self.head_up = pygame.image.load(os.path.join(graphics_path, 'head_up.png')).convert_alpha()
        self.head_down = pygame.image.load(os.path.join(graphics_path, 'head_down.png')).convert_alpha()
        self.head_right = pygame.image.load(os.path.join(graphics_path, 'head_right.png')).convert_alpha()
        self.head_left = pygame.image.load(os.path.join(graphics_path, 'head_left.png')).convert_alpha()
        
        self.body_vertical = pygame.image.load(os.path.join(graphics_path, 'body_vertical.png')).convert_alpha()
        self.body_horizontal = pygame.image.load(os.path.join(graphics_path, 'body_horizontal.png')).convert_alpha()
        
        self.body_tr = pygame.image.load(os.path.join(graphics_path, 'body_tr.png')).convert_alpha()
        self.body_tl = pygame.image.load(os.path.join(graphics_path, 'body_tl.png')).convert_alpha()
        self.body_br = pygame.image.load(os.path.join(graphics_path, 'body_br.png')).convert_alpha()
        self.body_bl = pygame.image.load(os.path.join(graphics_path, 'body_bl.png')).convert_alpha()
        
        self.tail_up = pygame.image.load(os.path.join(graphics_path, 'tail_up.png')).convert_alpha()
        self.tail_down = pygame.image.load(os.path.join(graphics_path, 'tail_down.png')).convert_alpha()
        self.tail_right = pygame.image.load(os.path.join(graphics_path, 'tail_right.png')).convert_alpha()
        self.tail_left = pygame.image.load(os.path.join(graphics_path, 'tail_left.png')).convert_alpha()
        
        # Load hình ảnh táo
        self.apple = pygame.image.load(os.path.join(graphics_path, 'apple.png')).convert_alpha()
        
    def reset(self):
        # Khởi tạo rắn ở vị trí ngẫu nhiên
        while True:
            # Tạo vị trí đầu rắn ngẫu nhiên
            head_x = random.randint(1, self.cell_number - 2)
            head_y = random.randint(1, self.cell_number - 2)
            head = Vector2(head_x, head_y)
            
            # Tạo thân rắn (2 phần)
            body1 = Vector2(head_x - 1, head_y)
            body2 = Vector2(head_x - 2, head_y)
            
            # Kiểm tra xem vị trí có hợp lệ không (không trùng với tường)
            if (0 < head_x < self.cell_number - 1 and 
                0 < head_y < self.cell_number - 1 and
                0 < body1.x < self.cell_number - 1 and
                0 < body2.x < self.cell_number - 1):
                self.snake_body = [head, body1, body2]
                self.direction = Vector2(1, 0)
                break
        
        self.new_block = False
        
        # Khởi tạo fruit
        self.fruit = self._generate_fruit()
        
        # Khởi tạo điểm
        self.score = 0
        
        # Reset trạng thái game
        self.game_over = False
        
        # Trả về state hiện tại
        return self._get_state()
    
    def _generate_fruit(self):
        # Tạo danh sách tất cả các vị trí có thể đặt fruit
        available_positions = []
        for x in range(self.cell_number):
            for y in range(self.cell_number):
                pos = Vector2(x, y)
                if pos not in self.snake_body:
                    available_positions.append(pos)
        
        # Nếu không còn vị trí trống, reset game
        if not available_positions:
            self.game_over = True
            return Vector2(-1, -1)  # Vị trí không hợp lệ
        
        # Chọn ngẫu nhiên một vị trí từ danh sách các vị trí có thể
        return random.choice(available_positions)
    
    def _get_state(self):
        # Lấy vị trí đầu rắn
        head = self.snake_body[0]
        
        # Tính toán các trạng thái nguy hiểm
        danger_straight = self._is_collision(head + self.direction)
        danger_right = self._is_collision(head + self.direction.rotate(90))
        danger_left = self._is_collision(head + self.direction.rotate(-90))
        
        # Xác định hướng di chuyển
        dir_left = self.direction == Vector2(-1, 0)
        dir_right = self.direction == Vector2(1, 0)
        dir_up = self.direction == Vector2(0, -1)
        dir_down = self.direction == Vector2(0, 1)
        
        # Xác định vị trí fruit
        fruit_left = self.fruit.x < head.x
        fruit_right = self.fruit.x > head.x
        fruit_up = self.fruit.y < head.y
        fruit_down = self.fruit.y > head.y
        
        state = [
            danger_straight,
            danger_right,
            danger_left,
            dir_left,
            dir_right,
            dir_up,
            dir_down,
            fruit_left,
            fruit_right,
            fruit_up,
            fruit_down
        ]
        
        return np.array(state, dtype=int)
    
    def _is_collision(self, point):
        # Kiểm tra va chạm với tường dựa trên hướng di chuyển
        if self.direction == Vector2(1, 0):  # Di chuyển sang phải
            if point.x >= self.cell_number:
                return True
        elif self.direction == Vector2(-1, 0):  # Di chuyển sang trái
            if point.x < 0:
                return True
        elif self.direction == Vector2(0, 1):  # Di chuyển xuống
            if point.y >= self.cell_number:
                return True
        elif self.direction == Vector2(0, -1):  # Di chuyển lên
            if point.y < 0:
                return True
                
        # Kiểm tra va chạm với thân rắn
        if point in self.snake_body[1:]:
            return True
            
        return False
    
    def step(self, action):
        # Xử lý sự kiện pygame nếu đang render
        if self.render_mode is not None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None, 0, True, {}
        
        # Nếu game đã kết thúc, trả về
        if self.game_over:
            return self._get_state(), -10, True, {}
        
        # Cập nhật hướng di chuyển dựa trên action
        clock_wise = [Vector2(1, 0), Vector2(0, 1), Vector2(-1, 0), Vector2(0, -1)]
        idx = clock_wise.index(self.direction)
        
        if action == 0:  # Straight
            new_direction = clock_wise[idx]
        elif action == 1:  # Right
            new_direction = clock_wise[(idx + 1) % 4]
        else:  # Left
            new_direction = clock_wise[(idx - 1) % 4]
            
        self.direction = new_direction
        
        # Kiểm tra va chạm trước khi di chuyển
        next_position = self.snake_body[0] + self.direction
        if self._is_collision(next_position):
            self.game_over = True
            return self._get_state(), -10, True, {}
        
        # Di chuyển rắn
        if self.new_block:
            self.snake_body.insert(0, next_position)
            self.new_block = False
        else:
            self.snake_body.pop()
            self.snake_body.insert(0, next_position)
        
        # Kiểm tra ăn fruit
        reward = -0.1  # Penalty cho mỗi bước để khuyến khích tìm đường ngắn nhất
        if self.snake_body[0] == self.fruit:
            self.fruit = self._generate_fruit()
            self.new_block = True
            self.score += 1
            reward = 10
        
        return self._get_state(), reward, False, {}
    
    def render(self):
        # Chỉ render nếu render_mode được bật
        if self.render_mode is None:
            return True
            
        # Xử lý sự kiện pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == self.SCREEN_UPDATE:
                self._update()
        
        # Vẽ game
        self._draw()
        return True
    
    def _update(self):
        # Nếu game đã kết thúc, không cập nhật
        if self.game_over:
            return
            
        # Kiểm tra va chạm trước khi di chuyển
        next_position = self.snake_body[0] + self.direction
        if self._is_collision(next_position):
            self.game_over = True
            return
            
        # Cập nhật vị trí rắn
        if self.new_block:
            self.snake_body.insert(0, next_position)
            self.new_block = False
        else:
            self.snake_body.pop()
            self.snake_body.insert(0, next_position)
    
    def _draw(self):
        # Vẽ background
        self.screen.fill((175, 215, 70))
        
        # Vẽ grass
        self._draw_grass()
        
        # Vẽ fruit
        fruit_rect = pygame.Rect(int(self.fruit.x * self.cell_size), int(self.fruit.y * self.cell_size), self.cell_size, self.cell_size)
        self.screen.blit(self.apple, fruit_rect)
        
        # Vẽ rắn
        for i, block in enumerate(self.snake_body):
            # Tạo rect cho mỗi phần của rắn
            block_rect = pygame.Rect(int(block.x * self.cell_size), int(block.y * self.cell_size), self.cell_size, self.cell_size)
            
            # Xác định hình ảnh phù hợp dựa trên vị trí trong thân rắn
            if i == 0:  # Đầu rắn
                if self.direction == Vector2(0, -1):
                    self.screen.blit(self.head_up, block_rect)
                elif self.direction == Vector2(0, 1):
                    self.screen.blit(self.head_down, block_rect)
                elif self.direction == Vector2(1, 0):
                    self.screen.blit(self.head_right, block_rect)
                elif self.direction == Vector2(-1, 0):
                    self.screen.blit(self.head_left, block_rect)
            elif i == len(self.snake_body) - 1:  # Đuôi rắn
                # Xác định hướng của đuôi
                if self.snake_body[i-1].y < block.y:
                    self.screen.blit(self.tail_down, block_rect)
                elif self.snake_body[i-1].y > block.y:
                    self.screen.blit(self.tail_up, block_rect)
                elif self.snake_body[i-1].x < block.x:
                    self.screen.blit(self.tail_right, block_rect)
                elif self.snake_body[i-1].x > block.x:
                    self.screen.blit(self.tail_left, block_rect)
            else:  # Thân rắn
                # Xác định hướng của thân
                prev_block = self.snake_body[i-1]
                next_block = self.snake_body[i+1]
                
                # Nếu thân nằm ngang
                if prev_block.y == block.y and next_block.y == block.y:
                    self.screen.blit(self.body_horizontal, block_rect)
                # Nếu thân nằm dọc
                elif prev_block.x == block.x and next_block.x == block.x:
                    self.screen.blit(self.body_vertical, block_rect)
                # Nếu thân là góc
                else:
                    # Góc trên phải
                    if (prev_block.y < block.y and next_block.x > block.x) or (prev_block.x > block.x and next_block.y < block.y):
                        self.screen.blit(self.body_tr, block_rect)
                    # Góc trên trái
                    elif (prev_block.y < block.y and next_block.x < block.x) or (prev_block.x < block.x and next_block.y < block.y):
                        self.screen.blit(self.body_tl, block_rect)
                    # Góc dưới phải
                    elif (prev_block.y > block.y and next_block.x > block.x) or (prev_block.x > block.x and next_block.y > block.y):
                        self.screen.blit(self.body_br, block_rect)
                    # Góc dưới trái
                    elif (prev_block.y > block.y and next_block.x < block.x) or (prev_block.x < block.x and next_block.y > block.y):
                        self.screen.blit(self.body_bl, block_rect)
        
        # Vẽ score
        score_text = pygame.font.Font(None, 36).render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        
        # Vẽ Game Over nếu game đã kết thúc
        if self.game_over:
            game_over_text = pygame.font.Font(None, 72).render('Game Over!', True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(400, 300))
            self.screen.blit(game_over_text, text_rect)
        
        pygame.display.update()
        self.clock.tick(10)
    
    def _draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(self.cell_number):
            for col in range(self.cell_number):
                if (row + col) % 2 == 0:
                    grass_rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                    pygame.draw.rect(self.screen, grass_color, grass_rect)
    
    def close(self):
        """Đóng môi trường và giải phóng tài nguyên"""
        if self.render_mode is not None:
            pygame.quit()
            self.render_mode = None
            self.screen = None
            self.clock = None
            self.head_up = None
            self.head_down = None
            self.head_right = None
            self.head_left = None
            self.body_vertical = None
            self.body_horizontal = None
            self.body_tr = None
            self.body_tl = None
            self.body_br = None
            self.body_bl = None
            self.tail_up = None
            self.tail_down = None
            self.tail_right = None
            self.tail_left = None
            self.apple = None
            self.grass = None 