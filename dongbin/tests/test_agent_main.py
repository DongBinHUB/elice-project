import pytest
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.common_actions import click_make_button

# --- 선택자 설정 ---
NAME_INPUT = (By.NAME, "name")
SUMMARY_INPUT = (By.XPATH, "//input[@placeholder='에이전트의 짧은 설명을 입력해보세요']")
SYSTEM_PROMPT_SELECTOR = (By.NAME, 'systemPrompt')
STARTER_FIELD_XPATH = (By.XPATH, '//input[@placeholder="이 에이전트의 시작 대화를 입력하세요"]')
FILE_INPUT = (By.XPATH, "//input[@type='file']")
ALL_CHECKBOXES = (By.CSS_SELECTOR, 'input[name="toolIds"][type="checkbox"]')
CREATE_BUTTON = (By.XPATH, "//button[normalize-space()='만들기']")
CREATE_SAVE_BUTTON = (By.XPATH, "//button[@type='submit' and normalize-space()='저장']")

def test_full_agent_creation_with_file_and_tools(driver):
    """파일 업로드 및 도구 다중 선택을 포함한 에이전트 생성 전체 테스트"""
    wait = WebDriverWait(driver, 15)
    
    # 1. 파일 경로 설정 (테스트 파일이 있는 위치 기준)
    # dongbin/tests/elice_logo.png 파일이 있다고 가정합니다.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "elice_logo.png")
    
    # 2. 에이전트 만들기 진입
    driver.get("https://qaproject.elice.io/ai-helpy-chat/agents/mine")
    click_make_button(driver, wait_time=10)
    print("\n[INFO] 에이전트 생성 프로세스 시작")

    # 3. 기본 정보 입력
    wait.until(EC.visibility_of_element_located(NAME_INPUT)).send_keys("동빈_풀테스트")
    wait.until(EC.visibility_of_element_located(SUMMARY_INPUT)).send_keys("전체 기능 테스트용 에이전트")
    wait.until(EC.visibility_of_element_located(SYSTEM_PROMPT_SELECTOR)).send_keys("길 찾기 규칙입니다.")
    wait.until(EC.visibility_of_element_located(STARTER_FIELD_XPATH)).send_keys("대중교통")
    print("[SUCCESS] 기본 정보 입력 완료")

    # 4. 파일 업로드
    # 파일이 실제로 존재하는지 체크 후 진행
    if os.path.exists(file_path):
        driver.find_element(*FILE_INPUT).send_keys(file_path)
        print(f"[SUCCESS] 파일 업로드 완료: {file_path}")
    else:
        print(f"[WARNING] 업로드할 파일을 찾을 수 없습니다: {file_path}")

    # 5. 도구(체크박스) 다중 선택 테스트
    try:
        checkboxes = wait.until(EC.presence_of_all_elements_located(ALL_CHECKBOXES))
        print(f"[INFO] 발견된 체크박스: {len(checkboxes)}개")
        
        for i, box in enumerate(checkboxes):
            if not box.is_selected():
                # 일반 클릭이 안될 경우를 대비해 JS 클릭 사용
                driver.execute_script("arguments[0].click();", box)
                print(f"[{i+1}]번째 도구 선택 완료")
        
        # 모든 체크박스가 선택되었는지 검증
        is_all_checked = all(box.is_selected() for box in checkboxes)
        assert is_all_checked, "일부 도구가 선택되지 않았습니다."
        
    except Exception as e:
        print(f"[ERROR] 체크박스 선택 중 오류: {e}")

    # 6. 만들기 및 최종 저장
    wait.until(EC.element_to_be_clickable(CREATE_BUTTON)).click()
    
    final_save_btn = wait.until(EC.element_to_be_clickable(CREATE_SAVE_BUTTON))
    driver.execute_script("arguments[0].click();", final_save_btn)
    print("[SUCCESS] 에이전트 생성 완료")

    # 7. 최종 목록 이동 확인
    wait.until(EC.url_contains("/agents/mine"))
    assert "/mine" in driver.current_url
    print("[PASS] 전체 생성 시나리오 성공")