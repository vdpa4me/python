import pygame
import random
import sys

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (187, 173, 160)
COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

GRID_SIZE = 4
CELL_SIZE = 100
MARGIN = 10
WIDTH = HEIGHT = GRID_SIZE * (CELL_SIZE + MARGIN) + MARGIN
FONT_SIZE = 40

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 - Mouse Controlled")
font = pygame.font.Font(None, FONT_SIZE)

def init_board():
    """ 초기 보드 생성 """
    board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    add_new_number(board)
    add_new_number(board)
    return board

def add_new_number(board):
    """ 현재 보드에서 가장 큰 숫자까지 랜덤하게 새로운 숫자를 추가 """
    empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if board[r][c] == 0]
    if empty_cells:
        r, c = random.choice(empty_cells)

        # 현재 보드에서 가장 큰 숫자 찾기
        max_value = max(max(row) for row in board)

        # 가능한 숫자 리스트 만들기 (2부터 max_value까지, 2의 배수)
        possible_numbers = [2]
        while possible_numbers[-1] < max_value:
            possible_numbers.append(possible_numbers[-1] * 2)

        # 확률적으로 낮은 숫자가 더 자주 등장하도록 가중치 적용
        weights = [1 / (2 ** i) for i in range(len(possible_numbers))]  # 확률: 1, 1/2, 1/4, 1/8 ...
        total_weight = sum(weights)
        probabilities = [w / total_weight for w in weights]  # 정규화

        # 확률적으로 새로운 숫자 선택
        board[r][c] = random.choices(possible_numbers, probabilities)[0]

def draw_board(board, selected_cell=None):
    """ 보드 화면 그리기 """
    screen.fill(GRAY)
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            value = board[r][c]
            color = COLORS.get(value, BLACK)
            rect = pygame.Rect(c * (CELL_SIZE + MARGIN) + MARGIN, r * (CELL_SIZE + MARGIN) + MARGIN, CELL_SIZE, CELL_SIZE)
            
            pygame.draw.rect(screen, color, rect, border_radius=10)
            if value != 0:
                text = font.render(str(value), True, BLACK if value < 8 else WHITE)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
    
    # 선택된 블록 강조
    if selected_cell:
        r, c = selected_cell
        highlight_rect = pygame.Rect(c * (CELL_SIZE + MARGIN) + MARGIN, r * (CELL_SIZE + MARGIN) + MARGIN, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, (255, 255, 0), highlight_rect, 3)  # 노란색 테두리

    pygame.display.update()

def move_single_tile(board, r, c, direction):
    """ 선택한 블록을 직선 방향으로 이동 (여러 칸 가능) """
    if board[r][c] == 0:
        return False  # 빈 칸이면 이동 불가능

    dr, dc = 0, 0
    if direction == "UP": dr = -1
    elif direction == "DOWN": dr = 1
    elif direction == "LEFT": dc = -1
    elif direction == "RIGHT": dc = 1

    new_r, new_c = r, c

    while True:
        next_r, next_c = new_r + dr, new_c + dc

        # 보드 범위를 벗어나면 멈춤
        if not (0 <= next_r < GRID_SIZE and 0 <= next_c < GRID_SIZE):
            break

        # 빈 칸이면 이동 가능
        if board[next_r][next_c] == 0:
            new_r, new_c = next_r, next_c
        # 같은 숫자면 합칠 수 있음
        elif board[next_r][next_c] == board[r][c]:
            new_r, new_c = next_r, next_c
            board[new_r][new_c] *= 2  # 합침
            board[r][c] = 0
            return True
        else:
            break  # 다른 숫자가 있으면 이동 불가능

    # 이동한 경우에만 처리
    if (new_r, new_c) != (r, c):
        board[new_r][new_c] = board[r][c]
        board[r][c] = 0
        return True

    return False  # 이동하지 않은 경우

def get_cell_from_mouse(pos):
    """ 마우스 클릭 위치를 보드 좌표로 변환 """
    x, y = pos
    c = x // (CELL_SIZE + MARGIN)
    r = y // (CELL_SIZE + MARGIN)
    if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
        return (r, c)
    return None

def is_game_over(board):
    """ 게임 종료 조건 확인 """
    # 빈 칸이 하나라도 있으면 게임 오버 아님
    for row in board:
        if 0 in row:
            return False
    
    # 같은 숫자가 인접해 있으면 게임 오버 아님
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if c < GRID_SIZE - 1 and board[r][c] == board[r][c + 1]:  # 오른쪽 비교
                return False
            if r < GRID_SIZE - 1 and board[r][c] == board[r + 1][c]:  # 아래 비교
                return False

    # 이동할 공간이 없으면 게임 오버
    return True

def main():
    board = init_board()
    selected_cell = None  # 선택된 블록 좌표
    running = True

    while running:
        draw_board(board, selected_cell)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                clicked_cell = get_cell_from_mouse(mouse_pos)
                
                if clicked_cell:
                    if selected_cell is None:  # 블록 선택
                        selected_cell = clicked_cell
                    else:  # 이동 처리
                        r, c = selected_cell
                        nr, nc = clicked_cell

                        direction = None
                        if nr == r and nc < c: direction = "LEFT"
                        elif nr == r and nc > c: direction = "RIGHT"
                        elif nc == c and nr < r: direction = "UP"
                        elif nc == c and nr > r: direction = "DOWN"

                        if direction:
                            moved = move_single_tile(board, r, c, direction)
                            if moved:
                                add_new_number(board)  # 이동 후 새로운 숫자 추가

                        selected_cell = None  # 선택 해제

            # 게임 오버 확인
            if is_game_over(board):
                print("Game Over!")
                pygame.quit()
                sys.exit()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
