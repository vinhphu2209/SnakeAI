import pygame, random
from pygame.math import Vector2

cell_number = 20

class FRUIT:
    def __init__(self):
        self.randomize(cell_number)

    def draw_fruit(self, screen, apple, cell_size):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def randomize(self, cell_number):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)
