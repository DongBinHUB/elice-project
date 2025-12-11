import os
import sys
import time
current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.join(current_dir, '..')
sys.path.append(project_root)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException # TimeoutException 임포트

from utils.driver_setup import login_driver
from utils.login_module import perform_login

BUTTON_SELECTOR_XPATH = (By.XPATH, "//a[normalize-space()='만들기']")
BUTTON_SELECTOR_CSS = (By.CSS_SELECTOR, "a.MuiButton-containedPrimary")

# 🚨 테스트용 상수
NORMAL_WIDTH = 1250
BUG_WIDTH = 700 
TEST_HEIGHT = 800

USER_EMAIL = "qa3team03@elicer.com"  
USER_PASSWORD = "@qa12345" 
LOGIN_URL = "https://accounts.elice.io/accounts/signin/me?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat%2Fagents&lang=en-US&org=qaproject"

# 드라이버 및 로그인
driver = login_driver(LOGIN_URL) 
driver.maximize_window() 

perform_login(driver, USER_EMAIL, USER_PASSWORD)
print(f"로그인 후 현재 URL: {driver.current_url}") 
time.sleep(5)

# 🚨 대기 시간을 20초로 증가
wait = WebDriverWait(driver, 20) 
print("--- [크리티컬 버그 테스트] 브라우저 크기별 버튼 가시성 확인 시작 ---")

# 🚨 식별자: CSS Selector로 통일 (가장 안정적이었던 것을 최종 선택)
BUTTON_SELECTOR = (By.CSS_SELECTOR, "a.MuiButton-containedPrimary")

try:
    # 1. 초기 설정: 일반 크기로 설정
    driver.set_window_size(NORMAL_WIDTH, TEST_HEIGHT) 
    print(f"[CHECK 1] 브라우저 크기 설정: {NORMAL_WIDTH}x{TEST_HEIGHT}")
    
    # 2. iframe 전환 시도
    try:
        iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        driver.switch_to.frame(iframe)
        print("[INFO] iframe으로 컨텍스트 전환 성공.")
        time.sleep(3) # 강제 대기
    except Exception:
        print("[INFO] iframe을 찾지 못함. 메인 컨텍스트 유지.")
        pass

    # 3. 버튼 확보 (가시성/클릭 가능 조건을 DOM 존재 조건으로 완화)
    print("[INFO] 3-1. DOM 존재 여부만 확인 후 JavaScript로 강제 클릭 시도...")
    
    # 🚨 presence_of_element_located를 사용하여 요소를 확보합니다.
    agent_make_btn = wait.until(
        EC.presence_of_element_located(BUTTON_SELECTOR)
    )
    
    # 🚨 JavaScript Executor를 사용하여 강제 클릭
    driver.execute_script("arguments[0].click();", agent_make_btn)
    
    print("[SUCCESS] 정상 크기에서 '만들기' 버튼 (JavaScript) 클릭 완료.")
    
    # ----------------------------------------------------
    # 4. 버그 재현 및 검증 로직 시작
    # ----------------------------------------------------
    
    # 모달 내부 요소의 가시성 테스트를 위해 '모달 내부의 만들기 버튼' 식별자 필요
    MODAL_CREATE_BTN_SELECTOR = (By.XPATH, "//button[normalize-space()='만들기']")
    
    # iframe에서 메인 컨텍스트로 복귀 (크기 조정을 위해 필수)
    driver.switch_to.default_content() 
    
    # 모달이 뜬 상태에서 크기 조정
    driver.set_window_size(BUG_WIDTH, TEST_HEIGHT)
    print(f"[ACTION] 브라우저 크기 축소: {BUG_WIDTH}x{TEST_HEIGHT}")
    
    time.sleep(2) # 화면 렌더링 대기 시간을 2초로 증가
    
    # 5. 다시 iframe으로 전환하여 모달 버튼 확보
    try:
        iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        driver.switch_to.frame(iframe)
    except Exception:
        pass 

    # 6. 모달 내부의 '만들기' 버튼 가시성 검증 (버그 포착 시도)
    try:
        # 축소된 크기에서 모달 내부의 '만들기' 버튼이 보이는지 확인 (버튼은 <button> 태그라고 가정)
        wait.until(EC.visibility_of_element_located(MODAL_CREATE_BTN_SELECTOR))
        
        print("[TEST FAILED] 버그가 재현되지 않았습니다. 모달 버튼이 축소된 크기에서도 보입니다.")
        
    except TimeoutException:
        print("\n[CRITICAL BUG REPRODUCED!]")
        print(f"[{BUG_WIDTH}x{TEST_HEIGHT} 크기에서] 모달 내부의 '만들기' 버튼이 화면에서 사라져 찾을 수 없습니다.")
        print("➡️ 예상 결과: 모달 버튼이 항상 보여야 함. / 실제 결과: 모달 버튼이 사라짐.")
        
except Exception as e:
    print(f"\n[UNEXPECTED ERROR] 테스트 초기화 또는 설정 중 오류 발생.")
    print(f"오류 클래스: {e.__class__.__name__}")
    print(f"오류 메시지: {e}")
    
finally:
    if 'driver' in locals() and driver:
        driver.quit()
        print("\n[INFO] 드라이버 종료.")