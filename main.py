# AI 활용 자유 주제 파이썬 미니 프로젝트
# 이름 또는 학번: 20415 임세진
# 프로젝트 주제:텍스트기반 젅투게임
import random

# 1. 캐릭터 도감 (2차원 리스트) - [이름, 체력, 공격력, 방어력]
character_pool = [
    ["전사", 150, 25, 10],
    ["궁수", 120, 30, 5],
    ["마법사", 90, 40, 2]
]

# 2. 기능별 함수 분리
def show_characters():
    """선택할 수 있는 캐릭터 목록을 보여주는 함수"""
    print("\n=== 선택 가능한 캐릭터 목록 ===")
    for i in range(len(character_pool)):
        char = character_pool[i]
        print(f"[{i}] {char[0]} - 체력: {char[1]}, 공격력: {char[2]}, 방어력: {char[3]}")
    print("===============================\n")

def calculate_damage(attacker_atk, defender_def):
    """데미지를 계산하는 함수 (공격력 - 방어력)"""
    damage = attacker_atk - defender_def
    # 만약 방어력이 너무 높아 데미지가 0 이하가 되면 최소 5의 데미지를 줍니다.
    if damage <= 0:
        damage = 5
    return damage


# 3. 메인 게임 흐름
def main():
    print("--- 워프렌즈 미니 텍스트 전투 게임 ---")
    
    # 캐릭터 목록 보여주기 (함수 호출)
    show_characters()
    
    # 플레이어 캐릭터 선택
    player_choice = int(input("원하는 캐릭터 번호를 선택하세요 (0~2): "))
    
    # 플레이어 능력치 설정 (2차원 리스트 활용)
    p_name = character_pool[player_choice][0]
    p_hp = character_pool[player_choice][1]
    p_atk = character_pool[player_choice][2]
    p_def = character_pool[player_choice][3]
    
    # AI(컴퓨터) 캐릭터 무작위 선택
    ai_choice = random.randint(0, 2)
    ai_name = character_pool[ai_choice][0]
    ai_hp = character_pool[ai_choice][1]
    ai_atk = character_pool[ai_choice][2]
    ai_def = character_pool[ai_choice][3]
    
    print(f"\n📢 [게임 시작] 플레이어({p_name}) VS 컴퓨터({ai_name})")
    
    round_count = 1
    
    # 4. 반복문: 두 플레이어의 체력이 모두 0보다 클 때 계속 싸움
    while p_hp > 0 and ai_hp > 0:
        print(f"\n--- 라운드 {round_count} ---")
        print(f"나의 HP: {p_hp} | 컴퓨터의 HP: {ai_hp}")
        
        # [플레이어의 턴] 행동 선택
        print("1. 공격하기 | 2. 방어자세 (이번 턴 방어력 +10)")
        action = input("행동을 선택하세요 (1 또는 2): ")
        
        # 임시 방어력 변수 (방어자세를 취하면 이번 턴에만 방어력이 올라감)
        current_p_def = p_def
        current_ai_def = ai_def
        
        # 5. 조건문: 플레이어의 행동 처리
        if action == "1":
            damage = calculate_damage(p_atk, current_ai_def)
            ai_hp -= damage
            print(f"⚔️ 내가 컴퓨터({ai_name})에게 {damage}의 데미지를 입혔습니다!")
        elif action == "2":
            current_p_def += 10
            print("🛡️ 방어 자세를 취해 이번 턴 방어력이 10 증가합니다!")
        
        # 컴퓨터의 체력이 0 이하가 되면 즉시 루프 종료
        if ai_hp <= 0:
            break
            
        # [AI의 턴] 무작위로 1(공격) 또는 2(방어) 선택
        ai_action = random.choice(["1", "2"])
        
        # 6. # 6. AI의 행동(공격 또는 방어)을 처리하는 조건문
        if ai_action == "1":
            # 플레이어가 입을 데미지를 계산합니다. (AI 공격력 - 플레이어 방어력)
            damage = calculate_damage(ai_atk, current_p_def)
            
            # [빈칸 미션 1] 플레이어의 체력(p_hp)에서 데미지(damage)만큼 빼주세요!
            p_hp -= ________
            
            print(f"💥 컴퓨터({ai_name})가 나에게 {damage}의 데미지를 입혔습니다!")
            
        elif ai_action == "2":
            # [빈칸 미션 2] AI의 임시 방어력(current_ai_def)을 10만큼 더해주세요!
            current_ai_def += ________
            
            print(f"🛡️ 컴퓨터({ai_name})가 방어 자세를 취해 이번 턴 방어력이 10 증가합니다!")
        # [힌트] 플레이어가 했던 방식과 비슷하게 하되, 대상만 바꾸면 돼요.
        # AI가 1을 선택하면 -> 플레이어의 p_hp를 (ai_atk - current_p_def)만큼 깎기
        # AI가 2를 선택하면 -> current_ai_def를 10 늘리기
        
        # -----------------------------------------------
        # (여기에 코드를 채워보세요!)
        
        
        # -----------------------------------------------
        
        round_count += 1
        
    # 7. 최종 결과 출력 (누가 이겼는지 판정하는 조건문)
    print("\n============= 게임 종료 =============")
    if p_hp > 0:
        print(f"🎉 승리! 컴퓨터({ai_name})를 쓰러뜨렸습니다.")
    else:
        print(f"💀 패배! 컴퓨터({ai_name})에게 졌습니다.")

# 프로그램 시작
if __name__ == "__main__":
    main()
