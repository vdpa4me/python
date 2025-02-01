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
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris Game")

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
SPEED = 5  # 기본 게임 속도


def new_piece():
    return {'shape': random.choice(SHAPES), 'color': random.choice(COLORS), 'x': COLUMNS // 2 - 1, 'y': 0}

piece = new_piece()

# 소리 설정
hit_sound = pygame.mixer.Sound("hit.mp3")
clear_sound = pygame.mixer.Sound("clear.mp3")

# 블록 충돌 검사 함수
def check_collision():
    for y, row in enumerate(piece['shape']):
        for x, cell in enumerate(row):
            if cell:
                new_x, new_y = piece['x'] + x, piece['y'] + y
                if new_x < 0 or new_x >= COLUMNS or new_y >= ROWS or (new_y >= 0 and grid[new_y][new_x] != BLACK):
                    return True
    return False

# 블록 회전 함수
def rotate_piece():
    rotated = list(zip(*reversed(piece['shape'])))
    old_x, old_shape = piece['x'], piece['shape']
    piece['shape'] = rotated
    if check_collision():
        piece['shape'] = old_shape
        piece['x'] = old_x

# 그리기 함수
def draw_grid():
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
    
    pygame.display.flip()

# 블록 고정 함수
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

# 라인 제거 함수
def check_lines():
    global grid
    full_rows = [y for y in range(ROWS) if all(cell != BLACK for cell in grid[y])]
    for row in full_rows:
        del grid[row]
        grid.insert(0, [BLACK for _ in range(COLUMNS)])
        clear_sound.play()

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
            if event.key == pygame.K_SPACE:
                rotate_piece()
    
    piece['y'] += 1
    if check_collision():
        piece['y'] -= 1
        lock_piece()
    
    draw_grid()
    clock.tick(SPEED)

pygame.quit()

