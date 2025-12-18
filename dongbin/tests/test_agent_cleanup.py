import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (TimeoutException, StaleElementReferenceException, NoSuchElementException)

# --- 선택자 설정 ---
MINE_URL = "https://qaproject.elice.io/ai-helpy-chat/agents/mine"
AGENT_CARDS = (By.XPATH, "//a[contains(@class, 'MuiCard-root')]")
# 삭제 대상 상태 정의 (초안, 나만보기, 기관 공개)
DRAFT_STATUS = (By.XPATH, ".//span[normalize-space()='초안' or normalize-space()='나만보기' or normalize-space()='기관 공개']")
DELETE_ICON = (By.XPATH, ".//*[@data-testid='trashIcon'] | .//*[contains(@data-icon, 'trash')]")
CONFIRM_DELETE_BUTTON = (By.XPATH, "//button[normalize-space()='삭제' or contains(text(), '삭제')]")

def test_cleanup_test_agents(driver):
    """생성된 테스트용 에이전트들을 상태별로 필터링하여 일괄 삭제"""
    wait = WebDriverWait(driver, 10)
    wait_short = WebDriverWait(driver, 3)
    
    driver.get(MINE_URL)
    print(f"\n[INFO] 클린업 페이지 접속: {MINE_URL}")

    deleted_count = 0

    # 무한 루프를 통해 페이지 내 삭제 대상이 없을 때까지 반복
    while True:
        try:
            # 매 반복마다 카드 목록을 새로고침 (DOM 변화 대응)
            wait.until(EC.presence_of_element_located(AGENT_CARDS))
            all_cards = driver.find_elements(*AGENT_CARDS)
            
            target_found = False
            
            for card in all_cards:
                try:
                    # 1. 상태 체크 (초안/나만보기/기관공개 중 하나인지)
                    status_tags = card.find_elements(*DRAFT_STATUS)
                    
                    if status_tags:
                        target_found = True
                        # 2. 휴지통 아이콘 클릭
                        delete_btn = card.find_element(*DELETE_ICON)
                        driver.execute_script("arguments[0].click();", delete_btn)
                        
                        # 3. 삭제 확인 팝업 클릭
                        confirm_btn = wait_short.until(EC.element_to_be_clickable(CONFIRM_DELETE_BUTTON))
                        confirm_btn.click()
                        
                        deleted_count += 1
                        print(f"[SUCCESS] {deleted_count}번째 에이전트 삭제 완료")
                        
                        # 삭제 후 DOM 갱신을 위해 잠시 대기 후 for문 탈출 (상위 while문에서 다시 시작)
                        time.sleep(1.5)
                        break 
                        
                except (StaleElementReferenceException, NoSuchElementException):
                    # 루프 도중 요소가 바뀌면 다시 처음부터 찾기 위함
                    break
            
            # 더 이상 삭제할 타겟 카드가 없으면 종료
            if not target_found:
                print(f"[INFO] 더 이상 삭제할 대상 에이전트가 없습니다.")
                break
                
        except TimeoutException:
            print("[INFO] 목록이 비어있거나 에이전트 카드를 찾을 수 없습니다.")
            break

    print(f"\n[PASS] 총 {deleted_count}개의 에이전트 정리 완료.")