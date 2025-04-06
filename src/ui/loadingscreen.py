import pygame
import sys

def show_loading_screen(screen, cell_number, cell_size):
    loading_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 50)
    loading_surface = loading_font.render('Loading...', True, (56, 74, 12))
    loading_rect = loading_surface.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 2))

    screen.fill((175, 215, 70))
    screen.blit(loading_surface, loading_rect)
    pygame.display.update()

    # Simulate loading time
    pygame.time.delay(2000)