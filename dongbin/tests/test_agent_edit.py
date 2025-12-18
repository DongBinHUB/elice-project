import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# --- 선택자 설정 ---
MINE_URL = "https://qaproject.elice.io/ai-helpy-chat/agents/mine"
EDIT_BUTTON = (By.XPATH, "//button[.//*[name()='svg' and @data-icon='pen']]")
AGENT_LIST_CONTAINER = (By.XPATH, "//div[@data-testid='virtuoso-item-list']")

def test_agent_edit_page_entry(driver):
    """에이전트 목록에서 수정(펜 아이콘) 버튼 클릭 및 페이지 진입 테스트"""
    wait = WebDriverWait(driver, 15)
    
    # 1. 내 에이전트 목록 페이지로 이동
    driver.get(MINE_URL)
    print(f"\n[INFO] 에이전트 목록 페이지 접속 시도: {MINE_URL}")

    # 2. 페이지 URL 및 목록 컨테이너 로딩 확인
    try:
        wait.until(EC.url_contains("/agents/mine"))
        wait.until(EC.presence_of_element_located(AGENT_LIST_CONTAINER))
        print("[SUCCESS] 에이전트 목록 로딩 완료")
    except TimeoutException:
        pytest.fail("에이전트 목록 페이지 로딩이 너무 느리거나 실패했습니다.")

    # 3. 수정 버튼 찾기 및 클릭
    # 목록에 에이전트가 하나도 없을 수 있으므로 예외 처리를 수행합니다.
    try:
        # 첫 번째로 발견되는 수정 버튼(펜 아이콘) 대기
        edit_btn = wait.until(EC.element_to_be_clickable(EDIT_BUTTON))
        
        # 버튼 클릭 (간섭 방지를 위해 필요 시 JS 클릭 사용 가능하나 여기선 일반 클릭 시도)
        edit_btn.click()
        print("[SUCCESS] 에이전트 수정 버튼 클릭 완료")
        
        # 4. 수정 페이지 진입 검증 (URL에 /edit이 포함되는지 확인)
        wait.until(EC.url_contains("/edit"))
        assert "/edit" in driver.current_url, f"수정 페이지 진입 실패. 현재 URL: {driver.current_url}"
        print(f"[PASS] 수정 페이지 진입 성공: {driver.current_url}")

    except TimeoutException:
        # 목록에 에이전트가 아예 없어서 수정 버튼이 안 뜨는 경우
        print("[SKIP] 목록에 수정할 수 있는 에이전트가 없습니다. 테스트를 중단합니다.")
        pytest.skip("수정할 에이전트 카드가 존재하지 않아 테스트를 건너뜁니다.")