import pygame
import sys
# from snakedb import SnakeDB

pygame.init()

def show_gameover_screen(screen, score, cell_number, cell_size):
    gameover_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 50)
    button_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 30)

    gameover_surface = gameover_font.render('Game Over', True, (56, 74, 12))
    gameover_rect = gameover_surface.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 4))

    retry_surface = button_font.render('Retry', True, (56, 74, 12))
    retry_rect = retry_surface.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 2))

    back_surface = button_font.render('Back to main menu', True, (56, 74, 12))
    back_rect = back_surface.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 1.5))

    save_surface = button_font.render('Save your score', True, (56, 74, 12))
    save_rect = save_surface.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 1.2))

    score_surface = gameover_font.render(f'Score: {score}', True, (56, 74, 12))
    score_rect = score_surface.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 3))

    screen.fill((175, 215, 70))
    screen.blit(gameover_surface, gameover_rect)
    screen.blit(retry_surface, retry_rect)
    screen.blit(back_surface, back_rect)
    screen.blit(save_surface, save_rect)
    screen.blit(score_surface, score_rect)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_rect.collidepoint(event.pos):
                    return 'playing'
                if back_rect.collidepoint(event.pos):
                    return 'menu'
                if save_rect.collidepoint(event.pos):
                    return 'save_score'

def show_save_score_screen(db, screen, score, cell_number, cell_size):
    button_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 30)
    input_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

    input_active = False
    input_text = ''
    input_rect = pygame.Rect(cell_number * cell_size // 4, cell_number * cell_size // 2, cell_number * cell_size // 2, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive

    save_surface = button_font.render('Save', True, (56, 74, 12))
    save_rect = save_surface.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 1.5))

    screen.fill((175, 215, 70))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if save_rect.collidepoint(event.pos):
                    db.insert_document(input_text, score)
                    return 'menu'
                if input_rect.collidepoint(event.pos):
                    input_active = not input_active
                    color = color_active if input_active else color_inactive
            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        db.insert_document(input_text, score)
                        return 'menu'
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

        screen.fill((175, 215, 70))
        txt_surface = input_font.render(input_text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_rect.w = width
        screen.blit(txt_surface, (input_rect.x + 5, input_rect.y + 5))
        pygame.draw.rect(screen, color, input_rect, 2)
        screen.blit(save_surface, save_rect)

        pygame.display.flip()