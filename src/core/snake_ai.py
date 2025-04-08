import pygame
from pygame.math import Vector2
from collections import deque
import heapq

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) # Tinh gia tri Manhattan. La tong khoang cach ngang doc cua 2 diem a,b

def a_star_search(snake_body, start, goal, grid_size):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    open_list = []
    heapq.heappush(open_list, (0, start)) # Khoi tao open la hang doi uu tien (heap), voi diem start va chi phi 0
    came_from = {start: None} # Theo doi o da di qua va khoi tao voi o start (gia tri none nghia la o nay khong co cha)
    cost_so_far = {start: 0} # Luu tru chi phi di chuyen

    while open_list: # Ham nay chay cho den khi hang doi uu tien trong (current = goal)
        _, current = heapq.heappop(open_list) # Lay o co uu tien thap nhat ra khoi hang doi

        if current == goal: # khi diem xet trung voi goal thi break
            break

        for direction in directions: # Kiem tra 4 o lan can theo cac huong len, xuong, trai, phai
            neighbor = (current[0] + direction[0], current[1] + direction[1]) #Cong toa do hien tai voi huong di chuyen de tinh toa do cua o lan can
            if (0 <= neighbor[0] < grid_size and 0 <= neighbor[1] < grid_size and # Kiem tra o lan can co nam trong luoi(grid) khong
                neighbor not in snake_body): # kiem tra o lan can co thuoc than ran hoac than nguoi choi khong
                new_cost = cost_so_far[current] + 1 # Tinh chi phi moi den o lan can. Chi phi nay bang chi phi de den o hien tai + them 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]: #Kiem tra neu o lan can chua dc kham pha hoac chi phi den o nay thap hon chi phi dc luu trc do
                    cost_so_far[neighbor] = new_cost # Neu dung thi cap nhat chi phi moi
                    priority = new_cost + heuristic(neighbor, goal) # Tinh toan do uu tien cho o lan can
                    heapq.heappush(open_list, (priority, neighbor)) # Day o lan can vao hang doi cung voi do uu tien cua no
                    came_from[neighbor] = current # Ghi lai o den tu dau

    path = []
    if goal in came_from: # Kiem tra xem muc tieu co nam trong came_from hay khong (tuc la tim dc duong di)
        current = goal
        while current != start: # Vong lap nay bat dau tu o muc tieu (goal) va lan nguoc lai cac o ma ta da di qua
            path.append(current) # Them ho hien tai vao path
            current = came_from[current]  # Di chuyen tu o hien tai den o ma no den tu
        path.reverse() # Dao nguoc lai de co duoc duong di
    return path

def bfs(snake_body, start, goal, grid_size, player_body=None):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  
    queue = deque([start])
    came_from = {start: None}
    visited = {start}

    while queue:
        current = queue.popleft()

        if current == goal:
            break

        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if (0 <= neighbor[0] < grid_size and 0 <= neighbor[1] < grid_size and 
                neighbor not in visited and neighbor not in snake_body and 
                (player_body is None or neighbor not in player_body)):
                queue.append(neighbor)
                visited.add(neighbor)
                came_from[neighbor] = current

    path = []
    if goal in came_from:
        current = goal
        while current != start:
            path.append(current)
            current = came_from[current]
        path.reverse()  
    return path

class SNAKE:
    def __init__(self):
        self.body = [Vector2(15, 10), Vector2(14, 10), Vector2(13, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        # Load graphics for AI snake
        self.head_up = pygame.image.load('assets/graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('assets/graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('assets/graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('assets/graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('assets/graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('assets/graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('assets/graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('assets/graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('assets/graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('assets/graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('assets/graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('assets/graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('assets/graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('assets/graphics/body_bl.png').convert_alpha()

        self.crunch_sound = pygame.mixer.Sound('assets/sound/crunch.wav')

    def move_snake(self, fruit_pos, cell_number, selected_algorithm='a_star', player_body=None):
        """Di chuyển rắn AI sử dụng thuật toán được chọn"""
        snake_head = self.body[0]
        snake_body_set = set((block.x, block.y) for block in self.body[1:])
        player_body_set = set((block.x, block.y) for block in player_body) if player_body else None

        if selected_algorithm == 'a_star':
            path = a_star_search(snake_body_set,
                               (snake_head.x, snake_head.y),
                               (fruit_pos.x, fruit_pos.y),
                               cell_number)
        else:  # BFS
            path = bfs(snake_body_set,
                      (snake_head.x, snake_head.y),
                      (fruit_pos.x, fruit_pos.y),
                      cell_number,
                      player_body_set)

        if path:
            next_move = Vector2(path[0][0], path[0][1]) - snake_head
            if abs(next_move.x) <= 1 and abs(next_move.y) <= 1:
                self.direction = next_move

        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def draw_snake(self, screen, cell_size):
        self.update_head_graphics()
        self.update_tail_graphics()
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0): self.head = self.head_left
        elif head_relation == Vector2(-1, 0): self.head = self.head_right
        elif head_relation == Vector2(0, 1): self.head = self.head_up
        elif head_relation == Vector2(0, -1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0): self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1): self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1): self.tail = self.tail_down

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(15, 10), Vector2(14, 10), Vector2(13, 10)]
        self.direction = Vector2(0, 0)
