import pygame
import random

# 초기화
pygame.init()

# 배경 음악 설정
pygame.mixer.music.load("background.mp3")
pygame.mixer.music.play(-1)  # 무한 반복 재생

# 화면 설정
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
COLUMNS = WIDTH // BLOCK_SIZE
ROWS = HEIGHT // BLOCK_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT + 50))  # 상단 공간 추가
pygame.display.set_caption("LV:1, Remain:5")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(0, 255, 255), (0, 0, 255), (255, 165, 0), (255, 255, 0), (0, 255, 0), (128, 0, 128), (255, 0, 0)]

# 블록 형태 정의
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

# 게임 변수
grid = [[BLACK for _ in range(COLUMNS)] for _ in range(ROWS)]
level = 1
lines_cleared = 0
clear_goal = {1: 5, 2: 6, 3: 7, 4: 8, 5: 9, 6: 10, 7: 11, 8: 12, 9: 13, 10: 14}
SPEED = 3  # 기본 게임 속도

font = pygame.font.Font(None, 36)

def new_piece():
    return {'shape': random.choice(SHAPES), 'color': random.choice(COLORS), 'x': COLUMNS // 2 - 1, 'y': 0}

piece = new_piece()

# 소리 설정
hit_sound = pygame.mixer.Sound("hit.mp3")
clear_sound = pygame.mixer.Sound("clear.mp3")
level_up_sound = pygame.mixer.Sound("level_up.mp3")

def check_collision():
    for y, row in enumerate(piece['shape']):
        for x, cell in enumerate(row):
            if cell:
                new_x, new_y = piece['x'] + x, piece['y'] + y
                if new_x < 0 or new_x >= COLUMNS or new_y >= ROWS or (new_y >= 0 and grid[new_y][new_x] != BLACK):
                    return True
    return False


def rotate_piece():
    rotated = list(zip(*reversed(piece['shape'])))
    old_x, old_shape = piece['x'], piece['shape']
    piece['shape'] = rotated
    if check_collision():
        piece['shape'] = old_shape
        piece['x'] = old_x


def draw_grid():
    global level, lines_cleared, clear_goal, font
    screen.fill(WHITE)
    for y in range(ROWS):
        for x in range(COLUMNS):
            pygame.draw.rect(screen, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
            pygame.draw.rect(screen, BLACK, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
    
    for y, row in enumerate(piece['shape']):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, piece['color'], ((piece['x'] + x) * BLOCK_SIZE, (piece['y'] + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
                pygame.draw.rect(screen, BLACK, ((piece['x'] + x) * BLOCK_SIZE, (piece['y'] + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
    
        text = font.render(f'Level: {level}', True, (0, 0, 0))
    screen.blit(text, (10, 10))
    remaining = clear_goal[level] - lines_cleared
    remaining_text = font.render(f'Lines to Next Level: {remaining}', True, (0, 0, 0))
    #screen.blit(remaining_text, (10, 40))
    pygame.display.set_caption(f"LV: {level}, Rmain: {clear_goal[level] - lines_cleared}")
    pygame.display.flip()


def lock_piece():
    global piece
    for y, row in enumerate(piece['shape']):
        for x, cell in enumerate(row):
            if cell and piece['y'] + y < ROWS:
                grid[piece['y'] + y][piece['x'] + x] = piece['color']
    hit_sound.play()
    check_lines()
    piece = new_piece()
    if check_collision():
        pygame.quit()
        exit()


def check_lines():
    global grid, lines_cleared, level, SPEED
    full_rows = [y for y in range(ROWS) if all(cell != BLACK for cell in grid[y])]
    lines_cleared += len(full_rows)
    for row in full_rows:
        del grid[row]
        grid.insert(0, [BLACK for _ in range(COLUMNS)])
        clear_sound.play()
    
    if level in clear_goal and lines_cleared >= clear_goal[level] and level < 10:
        level += 1
        SPEED += 0.5
        lines_cleared = 0  # 레벨이 올라가면 속도 증가
        grid = [[BLACK for _ in range(COLUMNS)] for _ in range(ROWS)]  # 모든 블록 초기화
        level_up_sound.play()
        screen.fill(WHITE)
        text = font.render(f"Level {level}!", True, (0, 0, 0))
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
        pygame.display.flip()
        pygame.time.delay(2000)
        print(f"레벨 {level}로 상승!")

# 게임 루프
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and piece['x'] > 0:
                piece['x'] -= 1
                if check_collision():
                    piece['x'] += 1
            if event.key == pygame.K_RIGHT and piece['x'] < COLUMNS - len(piece['shape'][0]):
                piece['x'] += 1
                if check_collision():
                    piece['x'] -= 1
            if event.key == pygame.K_DOWN:
                piece['y'] += 1
                if check_collision():
                    piece['y'] -= 1
                    lock_piece()
            if event.key == pygame.K_UP:
                rotate_piece()
    
    piece['y'] += 1
    if check_collision():
        piece['y'] -= 1
        lock_piece()
    
    draw_grid()
    clock.tick(SPEED)

pygame.quit()
