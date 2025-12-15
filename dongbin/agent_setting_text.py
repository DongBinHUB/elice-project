import os
import sys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from utils.credentials import USER_EMAIL, USER_PASSWORD
from utils.driver_setup import login_driver
from utils.login_module import perform_login
from utils.common_actions import click_make_button

#경로 설정 유지
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
sys.path.append(project_root)

#상수 정의
LONG_TEXT = "0"*301
VALID_TEXT = "길 찾기 에이전트 입니다"
VALIDATION_MESSAGE_TEXT_ONE = "한줄 소개는 최대 300자입니다"
VALIDATION_XPATH = f"//*[contains(text(), '{VALIDATION_MESSAGE_TEXT_ONE}')]"

LOGIN_URL = "https://accounts.elice.io/accounts/signin/me?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat%2Fagents&lang=en-US&org=qaproject"

driver = login_driver(LOGIN_URL) 
driver.maximize_window()

# 2. 로그인 실행
perform_login(driver, USER_EMAIL, USER_PASSWORD)
print(f"로그인 후 현재 URL: {driver.current_url}") 

wait = WebDriverWait(driver, 10)

print("--- 에이전트 생성 프로세스 시작 ---")

try:
    agent_make_btn = wait.until(
      EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='만들기']")))
   
    agent_make_btn.click()
    print("[SUCCESS]'만들기'버튼 클릭 성공.")
          
    agent_make_description= wait.until(
        EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='에이전트의 짧은 설명을 입력해보세요']"))
    )
    # 한줄 소개 정상 입력 과 비정상 입력(301자)
    agent_make_description.send_keys(LONG_TEXT)
    print(f"[SUCCESS] 1차 한줄 소개 입력 성공! ({len(LONG_TEXT)}자 입력 완료)")
    
    
    validation_message = wait.until(
        EC.presence_of_element_located((By.XPATH, VALIDATION_XPATH))
    )
     
    print(f"[VALIDATION SUCCESS] 길이 제한 메시지 확인: '{VALIDATION_MESSAGE_TEXT_ONE}'")
    
    agent_make_description.send_keys(Keys.CONTROL, "a")
    agent_make_description.send_keys(Keys.DELETE)
    
    wait.until(
        EC.invisibility_of_element_located((By.XPATH, VALIDATION_XPATH))
    )
    
    agent_make_description.send_keys(VALID_TEXT)
    print("[SUCCESS] 2차 한줄 소개 입력 성공.")
    
    wait.until(
        EC.invisibility_of_element_located((By.XPATH, VALIDATION_XPATH))
    ) 
    print("[SUCCESS] 유효성 검사 메시지 사라짐 확인 완료.")
    
except Exception as e:
    print(f"\n[CRITICAL ERROR] 자동화 프로세스 중 오류 발생.")
    print(f"오류 클래스: {e.__class__.__name__}")
    print(f"오류 메시지: {e}")
    
finally:
    # 🚨 브라우저를 닫는 명령어입니다.
    if 'driver' in locals() and driver:
        driver.quit()
        print("\n[INFO] 드라이버 종료.")
