import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from utils.credentials import USER_EMAIL, USER_PASSWORD
from utils.driver_setup import login_driver
from utils.login_module import perform_login



LOGIN_URL = "https://accounts.elice.io/accounts/signin/me?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat%2Fagents&lang=en-US&org=qaproject"
MY_AGENTS_BUTTON = (By.XPATH, "//a[@href='/ai-helpy-chat/agents/mine']")
MAKE_BUTTON = (By.XPATH, "//a[normalize-space()='만들기']")
EDIT_BUTTON = (By.XPATH, "//button[.//svg[@data-icon='pen']]")


driver = login_driver(LOGIN_URL) 
driver.maximize_window()

#에이전트 수정

try:
# 로그인 실행
    perform_login(driver, USER_EMAIL, USER_PASSWORD)
    print(f"로그인 후 현재 URL: {driver.current_url}") 

    # 대기 시간을 15초로 늘립니다.
    wait = WebDriverWait(driver, 15) 

    print("--- 에이전트 생성 프로세스 시작 ---")

    # 내 에이전트 버튼 클릭 (성공 확인)
    agent_btn = wait.until(EC.element_to_be_clickable(MY_AGENTS_BUTTON))
    agent_btn.click()
    print("[SUCCESS] 내 에이전트 클릭 완료")

    wait.until(EC.url_to_be("https://qaproject.elice.io/ai-helpy-chat/agents/mine"))
    print("[INFO] '/mine' 페이지로 이동 확인.")
    
    time.sleep(1)
    
    edit_btn = wait.until(EC.element_to_be_clickable(EDIT_BUTTON))
    edit_btn.click()
    print("[SUCCESS] 내 에이전트 클릭 완료")
    
    

except Exception as e:
    print(f"\n[CRITICAL ERROR] 자동화 프로세스 중 예상치 못한 오류 발생.")
    print(f"오류 클래스: {e.__class__.__name__}")
    print(f"오류 메시지: {e}")
    
finally:
    if 'driver' in locals() and driver:
        # 최종 상태 확인을 위해 3초 대기 후 종료
        time.sleep(3) 
        driver.quit()
        print("\n[INFO] 드라이버 종료.")

