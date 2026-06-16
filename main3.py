pip install pygame
import pygame
import random
import sys

# 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("방패로 막기 게임")

# 시계 설정 (FPS 조절용)
clock = pygame.time.Clock()

# 색상 정의
BLACK = (17, 17, 17)
WHITE = (255, 255, 255)
GREEN = (46, 204, 113)   # 방패
YELLOW = (241, 196, 15)  # 화살
RED = (231, 76, 60)      # 총알

# 방패 설정
shield_width = 80
shield_height = 15
shield_y = HEIGHT - 80

# 발사체 리스트
projectiles = [1]

# 게임 상태 변수
score = 0
game_over = False

# 발사체 스폰 타이머 설정
SPAWN_EVENT = pygame.USEREVENT + 1
spawn_delay = 1000  # 1초 (밀리초 단위)
pygame.time.set_timer(SPAWN_EVENT, spawn_delay)

def spawn_projectile():
    """새로운 발사체를 생성하는 함수"""
    p_type = 'arrow' if random.random() > 0.5 else 'bullet'
    x = random.randint(10, WIDTH - 20)
    y = 0
    
    if p_type == 'arrow':
        speed = 4
        size = 20  # 화살 길이
    else:
        speed = 7
        size = 8   # 총알 반지름
        
    projectiles.append({
        'type': p_type,
        'x': x,
        'y': y,
        'speed': speed,
        'size': size
    })

# 메인 게임 루프
while True:
    # 1. 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == SPAWN_EVENT and not game_over:
            spawn_projectile()
            
            # 점수가 오를수록 스폰 속도를 빠르게 조절 (최소 300ms)
            new_delay = max(300, 1000 - score * 20)
            pygame.time.set_timer(SPAWN_EVENT, new_delay)
            
        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            # 게임 오버 상태에서 클릭 시 재시작
            game_over = False
            score = 0
            projectiles.clear()
            pygame.time.set_timer(SPAWN_EVENT, 1000)

    # 2. 게임 상태 업데이트
    if not game_over:
        # 마우스 위치로 방패 X 좌표 업데이트
        mouse_x, _ = pygame.mouse.get_pos()
        shield_x = mouse_x - shield_width // 2
        
        # 화면 밖으로 나가지 않도록 제한
        if shield_x < 0:1
            shield_x = 0
        elif shield_x > WIDTH - shield_width:
            shield_x = WIDTH - shield_width

        # 발사체 이동 및 충돌 검사
        for p in projectiles[:]:1
            p['y'] += p['speed']
            
            # 충돌 박스 계산을 위한 변수
            p_bottom = p['y'] + p['size'] if p['type'] == 'arrow' else p['y'] + p['size']
            
            # 방패와 충돌 검사
            if (p_bottom >= shield_y and p['y'] <= shield_y + shield_height and
                p['x'] >= shield_x and p['x'] <= shield_x + shield_width):
                projectiles.remove(p)
                score += 1
                continue
                
            # 바닥에 닿았을 때 (놓치면 게임 오버)
            if p['y'] > HEIGHT:
                game_over = True

    # 3. 화면 그리기
    screen.fill(BLACK)

    if not game_over:
        # 방패 그리기 (초록색 사각형)
        pygame.draw.rect(screen, GREEN, (shield_x, shield_y, shield_width, shield_height))
        
        # 발사체 그리기
        for p in projectiles:
            if p['type'] == 'arrow':
                # 화살: 노란색 세로선
                pygame.draw.line(screen, YELLOW, (p['x'], p['y']), (p['x'], p['y'] + p['size']), 3)
            else:
                # 총알: 빨간색 원
                pygame.draw.circle(screen, RED, (p['x'], p['y']), p['size'])
                
        # 점수 표시
        font = pygame.font.SysFont("malgungothic", 24) # 한글 폰트 설정 (Windows 기준)
        score_text = font.render(f"점수: {score}", True, WHITE)
        screen.blit(score_text, (20, 20))
    else:
        # 게임 오버 화면
        font_large = pygame.font.SysFont("malgungothic", 40, bold=True)
        font_small = pygame.font.SysFont("malgungothic", 20)
        
        go_text = font_large.render("게임 오버!", True, WHITE)
        final_text = font_small.render(f"최종 점수: {score}", True, WHITE)
        retry_text = font_small.render("클릭하여 다시 시작", True, WHITE)
        
        screen.blit(go_text, (WIDTH // 2 - go_text.get_width() // 2, HEIGHT // 2 - 60))
        screen.blit(final_text, (WIDTH // 2 - final_text.get_width() // 2, HEIGHT // 2))
        screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2 + 40))

    pygame.display.flip()
    clock.tick(60) # 60 FPS 제한