import pygame
import sys
import random
from pygame.math import Vector2
from collections import deque
from src.core.player import PLAYER
from src.core.fruit import FRUIT
from src.core.snake import SNAKE
# from snakedb import SnakeDB
from src.ui.menu import main_menu, play, options, SCREEN, BG
from src.ui.gameover import show_gameover_screen, show_save_score_screen
from src.ui.loadingscreen import show_loading_screen
from src.ui.scoreboard import show_scoreboard


selected_algorithm = 'a_star'
player_moved = False

class MAIN:
    def __init__(self):
        print("Initializing...")
        self.previous_score = 0
        self.snake = SNAKE()
        # self.player = PLAYER()
        self.fruit = FRUIT()
        # self.db = SnakeDB()

    def update(self):
        # self.previous_score = len(self.player.body) - 3
        # print("Previous score:", self.previous_score)
        # print("Updating...")

        self.snake.move_snake(self.fruit.pos, cell_number, selected_algorithm)
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        print("Drawing elements...")
        self.draw_grass()
        self.fruit.draw_fruit(screen, apple, cell_size)
        self.snake.draw_snake(screen, cell_size)

    def check_collision(self):
        print("Checking for collision...")
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize(cell_number)
            self.snake.add_block()
            self.snake.play_crunch_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize(cell_number)


    def check_fail(self):        
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            print("Player thang")
            self.game_over()
        
    def game_over(self):
        print("Game over!")
        global game_state
        game_state = 'gameover'
        self.snake.reset()

    def draw_grass(self):
        print("Drawing grass...")
        grass_color = (167,209,61)
        for row in range(cell_number):
            if row % 2 == 0: 
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)    

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

show_loading_screen(screen, cell_number, cell_size)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 100)

main_game = MAIN()
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
                main_game.update()

        screen.fill((175, 215, 70))
        main_game.draw_elements()
        pygame.display.update()
        clock.tick(120)
    elif game_state == 'gameover':
        player_moved = False
        game_state = show_gameover_screen(screen, main_game.previous_score, cell_number, cell_size)
    elif game_state == 'save_score':
        game_state = show_save_score_screen(main_game.db, screen, main_game.previous_score, cell_number, cell_size)
    elif game_state == 'scoreboard':
        show_scoreboard(main_game.db, screen, cell_number, cell_size)
        game_state = 'menu'