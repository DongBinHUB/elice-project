from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

from utils.credentials import USER_EMAIL, USER_PASSWORD
from utils.driver_setup import login_driver
from utils.login_module import perform_login
from utils.common_actions import click_make_button

agent_rule = "길 찾기용 에이전트 입니다.  서울 위주 대중교통을 안내합니다"
LOGIN_URL = "https://accounts.elice.io/accounts/signin/me?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat%2Fagents&lang=en-US&org=qaproject"

PRIVATE_BUTTON = (By.XPATH, "//input[@type = 'radio' and @value='private']")
ORG_BUTTON = (By.XPATH,"//input[@type = 'radio' and @value = 'organization']")


#main 스크립트와 동일
CREATE_BUTTON = (By.XPATH, "//button[normalize-space()='만들기']") 
CREATE_SAVE_BUTTON = (By.XPATH,"//button[@type ='submit' and normalize-space() = '저장']")
SYSTEM_PROMPT_SELECTOR = (By.NAME, 'systemPrompt')
NAME = (By.NAME, "name")
SUMMARY_INPUT = (By.XPATH, "//input[@placeholder='에이전트의 짧은 설명을 입력해보세요']")

driver = login_driver(LOGIN_URL) 
driver.maximize_window()

# 2. 로그인 실행
perform_login(driver, USER_EMAIL, USER_PASSWORD)
print(f"로그인 후 현재 URL: {driver.current_url}") 

wait = WebDriverWait(driver, 10)

#만들기 버튼 클릭
try:
    click_make_button(driver, wait_time =10) 
    print("--- 에이전트 생성 프로세스 시작 ---")
    
    agent_make_name = wait.until(
        EC.visibility_of_element_located(NAME)
    )
    
    #이름 입력
    agent_make_name.send_keys("동빈")
    print("[SUCCESS] 이름 입력 성공!")
   
    #한줄 소개 입력
    agent_make_name = wait.until(
        EC.visibility_of_element_located(SUMMARY_INPUT)
    )
   
    agent_make_name.send_keys("길 찾기 에이전트 입니다")
    print("[SUCCESS] 한줄 소개 입력 성공!")
     
    time.sleep(2)
    
    #규칙 입력
    agent_make_rule = wait.until(
        EC.visibility_of_element_located(SYSTEM_PROMPT_SELECTOR)
    )
    agent_make_rule.send_keys(agent_rule)
    print("[SUCCESS] 규칙 입력 성공!")
    
    # 에이전트 작성 만들기 버튼
    upload_btn = wait.until(
        EC.element_to_be_clickable(CREATE_BUTTON)
             )
    upload_btn.click() 
    print("[ACTION] '만들기' 클릭 확인")  
    
    wait_long = WebDriverWait(driver,20)
    
    #나만보기
    private_btn = wait_long.until(EC.element_to_be_clickable(PRIVATE_BUTTON))
    private_btn.click()
    print("[SUCCESS] 나만 보기 선택 완료.")
    
    #완료버튼
    final_save_button = wait_long.until(
        EC.element_to_be_clickable(CREATE_SAVE_BUTTON)
    )
    final_save_button.click()
    print("[SUCCESS] 에이전트 생성 및 최종 '저장' 완료.")
    
    wait_long.until(EC.url_contains("/agents/mine")) 
    print("[INFO] '내 에이전트' 목록 페이지로 이동 확인.")
    
    
except Exception as e:
    print(f"\n[CRITICAL ERROR] 자동화 프로세스 중 예상치 못한 오류 발생.")
    print(f"오류 클래스: {e.__class__.__name__}")
    print(f"오류 메시지: {e}")
    
finally:
    if 'driver' in locals() and driver:
        # 최종 상태 확인을 위해 3초 대기 후 종료
        driver.quit()
        print("\n[INFO] 드라이버 종료.")
