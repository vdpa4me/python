import pygame
import sys
from pygame.locals import *

# Pygame 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("벽돌깨기 게임")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 소리 설정
pygame.mixer.init()
hit_sound = pygame.mixer.Sound("1.mp3")  # 효과음 파일 로드

# 공, 패들, 벽돌 설정
ball_speed = [4, -4]
ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
paddle = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 20, 120, 10)
paddle_speed = 15
brick_width = 60
brick_height = 30
bricks = [pygame.Rect(col * (brick_width + 5) + 35, row * (brick_height + 5) + 50, brick_width, brick_height)
          for row in range(5) for col in range(10)]

# 폰트 설정
font = pygame.font.Font(None, 36)

# 게임 루프 변수
running = True
score = 0

# 게임 루프
while running:
    screen.fill(BLACK)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # 패들 이동
    keys = pygame.key.get_pressed()
    if keys[K_LEFT] and paddle.left > 0:
        paddle.move_ip(-paddle_speed, 0)
    if keys[K_RIGHT] and paddle.right < WIDTH:
        paddle.move_ip(paddle_speed, 0)

    # 공 이동
    ball.left += ball_speed[0]
    ball.top += ball_speed[1]

    # 벽에 충돌
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed[0] = -ball_speed[0]
        hit_sound.play()  # 소리 재생
    if ball.top <= 0:
        ball_speed[1] = -ball_speed[1]
        hit_sound.play()  # 소리 재생

    # 패들에 충돌
    if ball.colliderect(paddle):
        ball_speed[1] = -ball_speed[1]
        hit_sound.play()  # 소리 재생

    # 벽돌에 충돌
    for brick in bricks[:]:
        if ball.colliderect(brick):
            ball_speed[1] = -ball_speed[1]
            bricks.remove(brick)
            score += 10
            hit_sound.play()  # 소리 재생
            break

    # 공이 바닥에 닿으면 게임 종료
    if ball.bottom >= HEIGHT:
        running = False

    # 객체 그리기
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.rect(screen, BLUE, paddle)
    for brick in bricks:
        pygame.draw.rect(screen, RED, brick)

    # 점수 표시
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # 화면 업데이트
    pygame.display.flip()
    pygame.time.delay(20)

pygame.quit()
sys.exit()
