import numpy as np
import pygame
from pygame.math import Vector2
import sys
import os

# Thêm đường dẫn gốc vào sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(root_dir)

from src.core.snake import SNAKE
from src.core.fruit import FRUIT

class SnakeEnv:
    def __init__(self, cell_size=40, cell_number=20, render=False):
        self.cell_size = cell_size
        self.cell_number = cell_number
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.render = render
        if render:
            pygame.init()
            self.screen = pygame.display.set_mode((cell_number * cell_size, 
                                                cell_number * cell_size))
            pygame.display.set_caption('Snake Game')
        self.reset()
        
    def reset(self):
        """Reset môi trường về trạng thái ban đầu"""
        self.snake.reset()
        self.fruit.randomize(self.cell_number)
        self.score = 0
        self.steps = 0
        return self._get_state()
    
    def step(self, action):
        """
        Thực hiện một bước trong môi trường
        
        Args:
            action: Hành động (0: lên, 1: xuống, 2: trái, 3: phải)
            
        Returns:
            state: Trạng thái mới
            reward: Điểm thưởng
            done: Game kết thúc hay chưa
            info: Thông tin bổ sung
        """
        self.steps += 1
        
        # Thực hiện hành động
        if action == 0:  # lên
            self.snake.direction = Vector2(0, -1)
        elif action == 1:  # xuống
            self.snake.direction = Vector2(0, 1)
        elif action == 2:  # trái
            self.snake.direction = Vector2(-1, 0)
        elif action == 3:  # phải
            self.snake.direction = Vector2(1, 0)
            
        # Di chuyển rắn
        self.snake.move_snake()
        
        # Kiểm tra va chạm với thức ăn
        reward = 0
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize(self.cell_number)
            self.snake.add_block()
            self.score += 1
            reward = 10
            
        # Kiểm tra va chạm với tường hoặc thân rắn
        done = False
        if (not 0 <= self.snake.body[0].x < self.cell_number or 
            not 0 <= self.snake.body[0].y < self.cell_number or
            self.snake.body[0] in self.snake.body[1:]):
            done = True
            reward = -10
            
        # Thưởng cho mỗi bước sống sót
        reward += 0.1
        
        return self._get_state(), reward, done, {"score": self.score, "steps": self.steps}
    
    def _get_state(self):
        """
        Lấy trạng thái hiện tại của môi trường
        
        Returns:
            state: Mảng numpy biểu diễn trạng thái
        """
        # Tạo grid trạng thái
        state = np.zeros((self.cell_number, self.cell_number))
        
        # Đánh dấu vị trí rắn
        for i, pos in enumerate(self.snake.body):
            if i == 0:  # đầu rắn
                state[int(pos.y)][int(pos.x)] = 2
            else:  # thân rắn
                state[int(pos.y)][int(pos.x)] = 1
                
        # Đánh dấu vị trí thức ăn
        state[int(self.fruit.pos.y)][int(self.fruit.pos.x)] = 3
        
        return state
    
    def render(self, screen=None):
        """Vẽ môi trường lên màn hình"""
        if not self.render:
            return
            
        if screen is None:
            screen = self.screen
            
        # Vẽ nền
        screen.fill((175, 215, 70))
        self._draw_grass(screen)
        
        # Vẽ rắn và thức ăn
        self.snake.draw_snake(screen, self.cell_size)
        self.fruit.draw_fruit(screen, self.cell_size)
        
        pygame.display.flip()
        
    def _draw_grass(self, screen):
        """Vẽ nền cỏ"""
        grass_color = (167, 209, 61)
        for row in range(self.cell_number):
            if row % 2 == 0:
                for col in range(self.cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * self.cell_size, row * self.cell_size,
                                               self.cell_size, self.cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(self.cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * self.cell_size, row * self.cell_size,
                                               self.cell_size, self.cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
                        
    def close(self):
        """Đóng môi trường"""
        if self.render:
            pygame.quit() 