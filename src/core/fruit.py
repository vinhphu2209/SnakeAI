import pygame, random
from pygame.math import Vector2

cell_number = 20

class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self, screen, cell_size):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        pygame.draw.rect(screen, (126, 166, 114), fruit_rect)

    def randomize(self, cell_number=20):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)
