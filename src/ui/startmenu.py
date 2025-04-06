import pygame
import sys

def show_start_menu(screen, cell_number, cell_size):
    menu_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 50)
    button_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 30)
    
    title_surface = menu_font.render('Snake Game', True, (56, 74, 12))
    title_rect = title_surface.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 3))
    
    start_surface = button_font.render('Start', True, (56, 74, 12))
    start_rect = start_surface.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 1.5))
    
    scoreboard_surface = button_font.render('Scoreboard', True, (56, 74, 12))
    scoreboard_rect = scoreboard_surface.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 1.3))
    
    quit_surface = button_font.render('Quit', True, (56, 74, 12))
    quit_rect = quit_surface.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 1.1))
    
    screen.fill((175, 215, 70))
    screen.blit(title_surface, title_rect)
    screen.blit(start_surface, start_rect)
    screen.blit(scoreboard_surface, scoreboard_rect)
    screen.blit(quit_surface, quit_rect)
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    waiting = False  # Start the game
                if quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
            # if event.type == pygame.KEYDOWN:
            #     waiting = False  # Start the game if any key is pressed