import pygame
import sys
import random
from pygame.math import Vector2
from collections import deque
from rl.environment.snake_env import SnakeEnv
from src.ui.menu import main_menu, play, options, SCREEN, BG
from src.ui.gameover import show_gameover_screen, show_save_score_screen
from src.ui.loadingscreen import show_loading_screen
from src.ui.scoreboard import show_scoreboard

# Khởi tạo pygame
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# Các tham số cấu hình
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

# Khởi tạo môi trường
env = SnakeEnv(cell_size, cell_number)

# Hiển thị màn hình loading
show_loading_screen(screen, cell_number, cell_size)

# Timer cho việc cập nhật màn hình
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 100)

# Trạng thái game
game_state = 'menu'

while True:
    if game_state == 'menu':
        game_state = main_menu(game_state)
    elif game_state == 'playing':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                # Lấy hành động từ người chơi hoặc AI
                action = None  # TODO: Implement action selection
                if action is not None:
                    state, reward, done, info = env.step(action)
                    if done:
                        game_state = 'gameover'
                        break

        # Vẽ môi trường
        env.render(screen)
        pygame.display.update()
        clock.tick(120)
    elif game_state == 'gameover':
        game_state = show_gameover_screen(screen, env.score, cell_number, cell_size)
    elif game_state == 'save_score':
        game_state = show_save_score_screen(screen, env.score, cell_number, cell_size)
    elif game_state == 'scoreboard':
        show_scoreboard(screen, cell_number, cell_size)
        game_state = 'menu'