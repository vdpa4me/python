import pygame

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Two-Player Tennis Game")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 패들 및 공 설정
paddle_width, paddle_height = 15, 100
ball_radius = 10

player1_x, player1_y = 50, HEIGHT // 2 - paddle_height // 2
player2_x, player2_y = WIDTH - 50 - paddle_width, HEIGHT // 2 - paddle_height // 2
ball_x, ball_y = WIDTH // 2, HEIGHT // 2

player_speed = 15
ball_speed_x, ball_speed_y = 5, 5

# 점수
score1, score2 = 0, 0
font = pygame.font.SysFont("Arial", 36)

# 소리 로드
hit_sound = pygame.mixer.Sound("hit.mp3")


def draw_objects():
    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, (player1_x, player1_y, paddle_width, paddle_height))
    pygame.draw.rect(screen, BLUE, (player2_x, player2_y, paddle_width, paddle_height))
    pygame.draw.circle(screen, BLACK, (ball_x, ball_y), ball_radius)
    score_text = font.render(f"{score1} - {score2}", True, BLACK)
    screen.blit(score_text, (WIDTH // 2 - 40, 20))
    pygame.display.flip()

# 게임 루프
clock = pygame.time.Clock()
while True:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1_y > 0:
        player1_y -= player_speed
    if keys[pygame.K_s] and player1_y < HEIGHT - paddle_height:
        player1_y += player_speed
    if keys[pygame.K_UP] and player2_y > 0:
        player2_y -= player_speed
    if keys[pygame.K_DOWN] and player2_y < HEIGHT - paddle_height:
        player2_y += player_speed
    
    # 공 이동
    ball_x += ball_speed_x
    ball_y += ball_speed_y
    
    # 벽 충돌
    if ball_y - ball_radius <= 0 or ball_y + ball_radius >= HEIGHT:
        ball_speed_y *= -1
        hit_sound.play()
    
    # 패들 충돌
    if (player1_x < ball_x < player1_x + paddle_width and player1_y < ball_y < player1_y + paddle_height) or \
       (player2_x < ball_x < player2_x + paddle_width and player2_y < ball_y < player2_y + paddle_height):
        ball_speed_x *= -1
        hit_sound.play()
    
    # 득점 판정
    if ball_x < 0:
        score2 += 1
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        ball_speed_x *= -1
    if ball_x > WIDTH:
        score1 += 1
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        ball_speed_x *= -1
    
    draw_objects()
    clock.tick(60)
