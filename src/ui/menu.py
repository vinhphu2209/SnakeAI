import pygame
import sys
from scoreboard import show_scoreboard  # Import scoreboard

pygame.init()

SCREEN = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Menu")

BG = pygame.image.load('assets/Background.png')
BG = pygame.transform.scale(BG, (800, 800))

class Menu_Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        return self.rect.collidepoint(position)

    def changeColor(self, position):
        if self.checkForInput(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

def get_font(size):
    """Hàm tải font từ assets với kích thước tùy chỉnh."""
    return pygame.font.Font("assets/font.ttf", size)

def play():
    """Giả lập bắt đầu chơi."""
    return 'playing'

def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        OPTIONS_TEXT = get_font(75).render("OPTIONS", True, "#b68f40")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(400, 100))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        BFS_BUTTON = Menu_Button(
            image=pygame.image.load("assets/Play Rect.png"), pos=(400, 300),
            text_input="BFS MODE", font=get_font(40),
            base_color="#d7fcd4", hovering_color="White"
        )
        BFS_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        BFS_BUTTON.update(SCREEN)

        A_STAR_BUTTON = Menu_Button(
            image=pygame.image.load("assets/Options Rect.png"), pos=(400, 500),
            text_input="A* SEARCH MODE", font=get_font(40),
            base_color="#d7fcd4", hovering_color="White"
        )
        A_STAR_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        A_STAR_BUTTON.update(SCREEN)

        OPTIONS_BACK = Menu_Button(
            image=pygame.image.load("assets/Quit Rect.png"), pos=(400, 700),
            text_input="BACK", font=get_font(75),
            base_color="#d7fcd4", hovering_color="White"
        )
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BFS_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    global selected_algorithm
                    selected_algorithm = 'bfs'
                    print("Thuật toán đã chọn: BFS")  # Debug

                if A_STAR_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    selected_algorithm = 'a_star'
                    print("Thuật toán đã chọn: A*")  # Debug

                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    return

        pygame.display.update()


def main_menu(game_state):
    """Hiển thị menu chính."""
    while game_state == 'menu':
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Tiêu đề
        MENU_TEXT = get_font(75).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        PLAY_BUTTON = Menu_Button(pygame.image.load("assets/Play Rect.png"), (400, 250),
                                  "PLAY", get_font(40), "#d7fcd4", "White")
        OPTIONS_BUTTON = Menu_Button(pygame.image.load("assets/Options Rect.png"), (400, 400),
                                     "OPTIONS", get_font(40), "#d7fcd4", "White")
        SCOREBOARD_BUTTON = Menu_Button(pygame.image.load("assets/Options Rect.png"), (400, 550),
                                        "SCOREBOARD", get_font(40), "#d7fcd4", "White")
        QUIT_BUTTON = Menu_Button(pygame.image.load("assets/Quit Rect.png"), (400, 700),
                                  "QUIT", get_font(40), "#d7fcd4", "White")

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, SCOREBOARD_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if SCOREBOARD_BUTTON.checkForInput(MENU_MOUSE_POS):
                    show_scoreboard( SCREEN, 20, 40)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
    return game_state
