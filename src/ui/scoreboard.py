import pygame
import sys
# from snakedb import SnakeDB

def show_scoreboard( screen, cell_number, cell_size):
    # documents = db.get20highestscore()
    # print("Documents fetched from DB:", documents)  # Debug statement

    menu_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 50)
    button_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 30)
    score_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 20)
    
    title_surface = menu_font.render('Scoreboard', True, (56, 74, 12))
    title_rect = title_surface.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 6))
    
    back_surface = button_font.render('Back', True, (56, 74, 12))
    back_rect = back_surface.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 1.1))
    
    screen.fill((175, 215, 70))
    screen.blit(title_surface, title_rect)
    screen.blit(back_surface, back_rect)
    
    y_offset = cell_number * cell_size // 4
    # for document in documents:
    #     print("Rendering document:", document)  # Debug statement
    #     score_surface = score_font.render(f"{document['name']}: {document['score']}", True, (56, 74, 12))
    #     score_rect = score_surface.get_rect(center=(cell_number * cell_size // 2, y_offset))
    #     screen.blit(score_surface, score_rect)
    #     y_offset += 30
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    waiting = False  # Go back to the main menu