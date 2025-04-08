import pygame
import sys
from database import GameDB

def save_score(score, agent_type):
    try:
        with open('scores.json', 'r') as f:
            scores = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        scores = []
    
    scores.append({
        'score': score,
        'agent': agent_type,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    
    with open('scores.json', 'w') as f:
        json.dump(scores, f, indent=4)

def show_scoreboard(screen, cell_number, cell_size):
    """Hiển thị bảng điểm"""
    # Khởi tạo font
    pygame.font.init()
    font = pygame.font.Font("assets/fonts/PoetsenOne-Regular.ttf", 32)
    title_font = pygame.font.Font("assets/fonts/PoetsenOne-Regular.ttf", 48)
    
    # Màu sắc
    BG_COLOR = (40, 40, 40)  # Dark gray
    TEXT_COLOR = (215, 252, 212)  # Light green
    TITLE_COLOR = (182, 143, 64)  # Gold
    
    # Lấy điểm từ database
    db = GameDB()
    scores = db.get_top_scores(10)  # Lấy top 10 điểm cao nhất
    db.close()
    
    while True:
        screen.fill(BG_COLOR)
        
        # Vẽ tiêu đề
        title = title_font.render("SCOREBOARD", True, TITLE_COLOR)
        title_rect = title.get_rect(center=(screen.get_width()//2, 50))
        screen.blit(title, title_rect)
        
        # Vẽ các dòng điểm
        y = 150
        for i, (score, agent_type, timestamp) in enumerate(scores, 1):
            # Định dạng thời gian
            time_str = timestamp.strftime("%Y-%m-%d %H:%M")
            
            # Vẽ thứ hạng
            rank_text = font.render(f"{i}.", True, TEXT_COLOR)
            rank_rect = rank_text.get_rect(left=50, centery=y)
            screen.blit(rank_text, rank_rect)
            
            # Vẽ điểm số
            score_text = font.render(f"{score}", True, TEXT_COLOR)
            score_rect = score_text.get_rect(left=150, centery=y)
            screen.blit(score_text, score_rect)
            
            # Vẽ loại agent
            agent_text = font.render(agent_type, True, TEXT_COLOR)
            agent_rect = agent_text.get_rect(left=300, centery=y)
            screen.blit(agent_text, agent_rect)
            
            # Vẽ thời gian
            time_text = font.render(time_str, True, TEXT_COLOR)
            time_rect = time_text.get_rect(left=450, centery=y)
            screen.blit(time_text, time_rect)
            
            y += 50
        
        # Vẽ hướng dẫn
        guide = font.render("Press ESC to return", True, TEXT_COLOR)
        guide_rect = guide.get_rect(center=(screen.get_width()//2, screen.get_height() - 50))
        screen.blit(guide, guide_rect)
        
        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        
        pygame.display.update()