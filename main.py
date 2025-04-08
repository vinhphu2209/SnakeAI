import pygame
import sys
from src.core.snake_ai import SNAKE, a_star_search, bfs
from src.db.manager import GameDB
from pygame.math import Vector2
import random

# Khởi tạo pygame
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# Các tham số cấu hình
cell_size = 40
cell_number = 20
clock = pygame.time.Clock()

# Khởi tạo màn hình pygame
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Snake AI")

# Khởi tạo rắn AI và database
snake = SNAKE()
db = GameDB()

# Timer cho việc cập nhật màn hình
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 100)

# Trạng thái game
game_state = 'menu'
score = 0
fruit_pos = Vector2(5, 5)

def save_score(score, agent_type):
    """Lưu điểm vào MongoDB"""
    db.save_score(score, agent_type)

def show_scoreboard(screen, cell_number, cell_size):
    """Hiển thị bảng điểm từ MongoDB"""
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)
    
    # Thay đổi kích thước màn hình cho scoreboard
    scoreboard_screen = pygame.display.set_mode((800, 600))
    scoreboard_screen.fill(BLACK)
    
    # Vẽ tiêu đề
    title = font.render("Scoreboard", True, WHITE)
    scoreboard_screen.blit(title, (cell_number * cell_size // 2 - 100, 50))
    
    # Lấy top 5 điểm cho mỗi loại agent
    bfs_scores = db.get_top_scores(limit=5, agent_type='BFS')
    astar_scores = db.get_top_scores(limit=5, agent_type='A*')
    
    # Vẽ điểm BFS
    bfs_title = font.render("BFS Scores:", True, WHITE)
    scoreboard_screen.blit(bfs_title, (50, 150))
    
    # Vẽ điểm và thời gian cho BFS
    for i, score_doc in enumerate(bfs_scores):
        # Vẽ điểm
        score_text = font.render(f"{score_doc['score']}", True, WHITE)
        scoreboard_screen.blit(score_text, (50, 200 + i * 60))
        
        # Vẽ thời gian
        if 'date' in score_doc:
            date_str = score_doc['date'].strftime("%Y-%m-%d %H:%M")
            date_text = small_font.render(date_str, True, WHITE)
            scoreboard_screen.blit(date_text, (50, 230 + i * 60))
        
        # Vẽ nút xóa
        delete_text = small_font.render("Delete", True, RED)
        delete_rect = delete_text.get_rect(topleft=(200, 200 + i * 60))
        scoreboard_screen.blit(delete_text, delete_rect)
    
    # Vẽ điểm A*
    astar_title = font.render("A* Scores:", True, WHITE)
    scoreboard_screen.blit(astar_title, (400, 150))
    
    # Vẽ điểm và thời gian cho A*
    for i, score_doc in enumerate(astar_scores):
        # Vẽ điểm
        score_text = font.render(f"{score_doc['score']}", True, WHITE)
        scoreboard_screen.blit(score_text, (400, 200 + i * 60))
        
        # Vẽ thời gian
        if 'date' in score_doc:
            date_str = score_doc['date'].strftime("%Y-%m-%d %H:%M")
            date_text = small_font.render(date_str, True, WHITE)
            scoreboard_screen.blit(date_text, (400, 230 + i * 60))
        
        # Vẽ nút xóa
        delete_text = small_font.render("Delete", True, RED)
        delete_rect = delete_text.get_rect(topleft=(550, 200 + i * 60))
        scoreboard_screen.blit(delete_text, delete_rect)
    
    # Vẽ nút Back
    back_button = font.render("Back to Menu (ESC)", True, WHITE)
    back_rect = back_button.get_rect(center=(400, 550))
    scoreboard_screen.blit(back_button, back_rect)
    
    pygame.display.update()
    
    # Đợi người dùng nhấn ESC hoặc click
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting = False
                    # Khôi phục lại màn hình menu
                    pygame.display.set_mode((800, 600))
                    pygame.display.set_caption("Snake AI Menu")
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Kiểm tra click vào nút xóa BFS
                for i, score_doc in enumerate(bfs_scores):
                    delete_rect = pygame.Rect(200, 200 + i * 60, 50, 20)
                    if delete_rect.collidepoint(event.pos):
                        # Xóa điểm
                        db.delete_score(score_doc['_id'])
                        # Cập nhật lại màn hình
                        return show_scoreboard(screen, cell_number, cell_size)
                
                # Kiểm tra click vào nút xóa A*
                for i, score_doc in enumerate(astar_scores):
                    delete_rect = pygame.Rect(550, 200 + i * 60, 50, 20)
                    if delete_rect.collidepoint(event.pos):
                        # Xóa điểm
                        db.delete_score(score_doc['_id'])
                        # Cập nhật lại màn hình
                        return show_scoreboard(screen, cell_number, cell_size)

def ai_menu(state):
    """Hiển thị menu chính"""
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    
    # Sử dụng màn hình đã khởi tạo
    pygame.display.set_caption("Snake AI Menu")
    
    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 48)
    
    options = [
        "Watch BFS Pathfinding",
        "Watch A* Pathfinding",
        "Train RL Agent",
        "View Scoreboard",
        "Exit"
    ]
    
    selected_option = 0
    
    while True:
        screen.fill(BLACK)
        
        # Vẽ tiêu đề
        title = title_font.render("Snake AI Menu", True, WHITE)
        title_rect = title.get_rect(center=(400, 100))
        screen.blit(title, title_rect)
        
        # Vẽ các tùy chọn
        for i, option in enumerate(options):
            color = GREEN if i == selected_option else WHITE
            text = font.render(option, True, color)
            rect = text.get_rect(center=(400, 250 + i * 50))
            screen.blit(text, rect)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        return 'watch_bfs'
                    elif selected_option == 1:
                        return 'watch_astar'
                    elif selected_option == 2:
                        return 'train_ai'
                    elif selected_option == 3:
                        return 'scoreboard'
                    elif selected_option == 4:
                        pygame.quit()
                        sys.exit()
        
        clock.tick(60)

def run_ai_game(algorithm):
    """Chạy game với thuật toán được chọn"""
    global game_state, score, fruit_pos
    
    # Thay đổi kích thước màn hình cho game
    game_screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
    pygame.display.set_caption(f"Snake AI - {algorithm}")
    
    # Load hình ảnh quả táo
    apple_surface = pygame.image.load('assets/graphics/apple.png').convert_alpha()
    apple_surface = pygame.transform.scale(apple_surface, (cell_size, cell_size))
    
    # Reset game state
    snake.reset()
    score = 0
    fruit_pos = Vector2(5, 5)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Lưu điểm trước khi thoát
                    save_score(score, algorithm)
                    game_state = 'menu'
                    return
            if event.type == SCREEN_UPDATE:
                # Di chuyển rắn theo thuật toán được chọn
                snake.move_snake(fruit_pos, cell_number, algorithm)
                
                # Kiểm tra va chạm với quả
                if snake.body[0] == fruit_pos:
                    snake.add_block()
                    snake.play_crunch_sound()
                    score += 1
                    # Tạo quả mới ở vị trí ngẫu nhiên
                    while True:
                        fruit_pos = Vector2(
                            random.randint(0, cell_number - 1),
                            random.randint(0, cell_number - 1)
                        )
                        if fruit_pos not in snake.body:
                            break
                
                # Kiểm tra va chạm với tường hoặc thân
                if (snake.body[0].x < 0 or snake.body[0].x >= cell_number or
                    snake.body[0].y < 0 or snake.body[0].y >= cell_number or
                    snake.body[0] in snake.body[1:]):
                    # Lưu điểm khi game over
                    save_score(score, algorithm)
                    game_state = 'menu'
                    return
        
        # Vẽ game
        game_screen.fill((175, 215, 70))  # Màu nền chung
        
        # Vẽ mẫu bàn cờ caro
        for row in range(cell_number):
            for col in range(cell_number):
                # Tính toán màu dựa trên vị trí (row + col) để tạo mẫu xen kẽ
                if (row + col) % 2 == 0:
                    color = (175, 215, 70)  # Xanh nhạt
                else:
                    color = (150, 190, 50)  # Xanh đậm
                
                # Vẽ ô vuông
                cell_rect = pygame.Rect(
                    col * cell_size,
                    row * cell_size,
                    cell_size,
                    cell_size
                )
                pygame.draw.rect(game_screen, color, cell_rect)
        
        snake.draw_snake(game_screen, cell_size)
        
        # Vẽ quả táo
        apple_rect = pygame.Rect(
            int(fruit_pos.x * cell_size),
            int(fruit_pos.y * cell_size),
            cell_size,
            cell_size
        )
        game_screen.blit(apple_surface, apple_rect)
        
        # Vẽ điểm
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        game_screen.blit(score_text, (10, 10))
        
        pygame.display.update()
        clock.tick(10)

# Main game loop
while True:
    if game_state == 'menu':
        game_state = ai_menu(game_state)
    elif game_state == 'watch_bfs':
        run_ai_game('BFS')
    elif game_state == 'watch_astar':
        run_ai_game('A*')
    elif game_state == 'train_ai':
        # Huấn luyện agent RL
        from src.rl.train import train_agent
        train_agent(snake)
        game_state = 'menu'
    elif game_state == 'scoreboard':
        show_scoreboard(screen, cell_number, cell_size)
        game_state = 'menu'

# Đóng kết nối database khi thoát
db.close()
