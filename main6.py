import os
import time
import random
import keyboard

# 1. 게임 화면 크기 설정
WIDTH = 15
HEIGHT = 10

# 2. 게임 상태 초기화
player_x = WIDTH // 2 - 1  # 방패의 시작 X 좌표 (중앙)
score = 0
game_over = False

# 발사체 목록 (각 요소는 [x_좌표, y_좌표, 발사체_타입] 형태)
# 타입 종류 -> 1: 화살(↓), 2: 총알(*)
projectiles = []

def clear_screen():
    """터미널 화면을 깨끗하게 지워주는 함수"""
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_game():
    """텍스트로 게임 화면을 그리는 함수"""
    clear_screen()
    print("=== 방패로 막기 게임 ===")
    print(f"점수: {score}  |  [A]: 왼쪽 이동  [D]: 오른쪽 이동")
    print("-" * (WIDTH + 2))

    # 빈 화면 매트릭스 생성 (공백으로 채움)
    grid = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

    # 화면에 발사체 배치
    for p in projectiles:
        px, py, p_type = p
        if 0 <= py < HEIGHT:
            grid[py][px] = "↓" if p_type == 1 else "*"

    # 화면 맨 아래 줄에 방패(■■■) 배치 (총 3칸 크기)
    for i in range(3):
        shield_pos = player_x + i
        if 0 <= shield_pos < WIDTH:
            grid[HEIGHT - 1][shield_pos] = "■"

    # 테두리와 함께 화면 출력
    for row in grid:
        print("|" + "".join(row) + "|")
        
    print("-" * (WIDTH + 2))

# --- 게임 시작 준비 ---
print("게임 준비 중... 터미널 창을 활성화하고 잠시만 기다려주세요!")
time.sleep(1.5)

loop_count = 0

# --- 메인 게임 루프 ---
while not game_over:
    # 1. 키보드 입력 감지 및 방패 이동
    if keyboard.is_pressed('a') or keyboard.is_pressed('left'):
        if player_x > 0:
            player_x -= 1
    if keyboard.is_pressed('d') or keyboard.is_pressed('right'):
        if player_x < WIDTH - 3:
            player_x += 1

    # 2. 발사체 생성 (루프가 돌 때마다 확률/주기별로 스폰)
    spawn_rate = max(2, 6 - (score // 5))
    if loop_count % spawn_rate == 0:
        p_type = 1 if random.random() > 0.4 else 2
        projectiles.append([random.randint(0, WIDTH - 1), 0, p_type])

    # 3. 발사체 이동 및 충돌(막기) 검사
    next_projectiles = []
    for p in projectiles:
        px, py, p_type = p
        
        # 총알(2)은 화살보다 빠른 속도로 내려오도록 2칸씩 이동
        move_dist = 2 if p_type == 2 else 1
        py += move_dist

        # 방패가 있는 맨 아래 라인에 도달했거나 넘어섰을 때
        if py >= HEIGHT - 1:
            if player_x <= px <= player_x + 2:
                score += 1  # 성공적으로 막음
                continue    # 삭제 처리
            else:
                game_over = True  # 막지 못함 -> 게임 종료
                break
        
        next_projectiles.append([px, py, p_type])
        
    projectiles = next_projectiles

    # 4. 화면 갱신 및 프레임 속도 조절
    draw_game()
    loop_count += 1
    time.sleep(0.12)

# --- 게임 오버 화면 ---
clear_screen()
print("=======================")
print("      GAME OVER!       ")
print(f"    최종 점수: {score} 점   ")
print("=======================")