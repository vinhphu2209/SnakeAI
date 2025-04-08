import pygame
import sys
from src.db.manager import GameDB

pygame.init()

SCREEN = None

# Colors
BG_COLOR = (40, 40, 40)  # Dark gray
BUTTON_COLOR = (60, 60, 60)  # Light gray
TEXT_COLOR = (215, 252, 212)  # Light green
HOVER_COLOR = (255, 255, 255)  # White
TITLE_COLOR = (182, 143, 64)  # Gold

class Menu_Button():
    def __init__(self, pos, text_input, font, base_color, hovering_color):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.rect = pygame.Rect(0, 0, 300, 60)  # Button size
        self.rect.center = (self.x_pos, self.y_pos)
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        pygame.draw.rect(screen, BUTTON_COLOR, self.rect, border_radius=12)
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
    return pygame.font.Font("assets/fonts/PoetsenOne-Regular.ttf", size)

def save_score(score, agent_type, metadata=None):
    db = GameDB()
    db.save_score(score, agent_type, metadata)
    db.close()

def ai_menu(game_state):
    # Khởi tạo màn hình nếu chưa có
    global SCREEN
    if SCREEN is None:
        SCREEN = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Snake AI")

    while True:
        SCREEN.fill(BG_COLOR)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("SNAKE AI", True, TITLE_COLOR)
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        WATCH_BFS_BUTTON = Menu_Button(
            pos=(400, 250),
            text_input="WATCH BFS", font=get_font(40),
            base_color=TEXT_COLOR, hovering_color=HOVER_COLOR
        )

        WATCH_ASTAR_BUTTON = Menu_Button(
            pos=(400, 400),
            text_input="WATCH A*", font=get_font(40),
            base_color=TEXT_COLOR, hovering_color=HOVER_COLOR
        )

        TRAIN_AI_BUTTON = Menu_Button(
            pos=(400, 550),
            text_input="TRAIN RL", font=get_font(40),
            base_color=TEXT_COLOR, hovering_color=HOVER_COLOR
        )

        SCOREBOARD_BUTTON = Menu_Button(
            pos=(400, 700),
            text_input="SCOREBOARD", font=get_font(40),
            base_color=TEXT_COLOR, hovering_color=HOVER_COLOR
        )

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [WATCH_BFS_BUTTON, WATCH_ASTAR_BUTTON, TRAIN_AI_BUTTON, SCOREBOARD_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if WATCH_BFS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return 'watch_bfs'
                if WATCH_ASTAR_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return 'watch_astar'
                if TRAIN_AI_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return 'train_ai'
                if SCOREBOARD_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return 'scoreboard'

        pygame.display.update()
