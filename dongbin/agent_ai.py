#대화로 ai에이전트 생성

import time
import json
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from utils.chat_utils import get_latest_ai_answer #chat_utils 모듈
from utils.credentials import USER_EMAIL, USER_PASSWORD
from utils.driver_setup import login_driver
from utils.login_module import perform_login

LOGIN_URL = "https://accounts.elice.io/accounts/signin/me?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat%2Fagents&lang=en-US&org=qaproject"
MAKE_BUTTON = (By.XPATH, "//a[normalize-space()='만들기']")

CHAT_CREATE_BUTTON = (By.CSS_SELECTOR, "button[value='chat']") #대화로 버튼
MESSAGE_TEXTAREA = (By.NAME, "input") #ai챗 입력

driver = login_driver(LOGIN_URL) 
driver.maximize_window()

try:
    #로그인 실행
    perform_login(driver, USER_EMAIL, USER_PASSWORD)
    print(f"로그인 후 현재 URL: {driver.current_url}") 

    wait = WebDriverWait(driver, 10)

    print("--- 에이전트 생성 프로세스 시작 ---")

    #만들기 버튼 클릭
    make_btn = wait.until(EC.element_to_be_clickable(MAKE_BUTTON))
    make_btn.click()
    print("[SUCCESS] 내 에이전트 클릭 완료")
    
    print("\n--- AI 에이전트 대화 생성 시작 ---")
    
    #대화로 만들기 클릭
    
    ai_chat_make = wait.until(EC.element_to_be_clickable(CHAT_CREATE_BUTTON))
    ai_chat_make.click()
    print("[SUCCESS] 대화로 만들기 클릭 완료")
    
    input_box = wait.until(EC.presence_of_element_located(MESSAGE_TEXTAREA))
    
    agent_prompt = "길 찾기" #챗 입력
    
    input_box.click()
    input_box.send_keys(agent_prompt)
    print(f"[ACTION] 메시지 입력 완료: {agent_prompt}")
    
    input_box.send_keys(Keys.ENTER)
    
    time.sleep(2)
    
    answer = get_latest_ai_answer(driver, wait)
    print(f"AI 답변: {answer}")
   

    
    

except Exception as e:
  
        print(f"\n[CRITICAL ERROR] 자동화 프로세스 중 예상치 못한 오류 발생.")
        print(f"오류 클래스: {e.__class__.__name__}")
        print(f"오류 메시지: {e}")



# finally:
#         if 'driver' in locals() and driver:
#          time.sleep(3) 
#          driver.quit()
#          print("\n[INFO] 드라이버 종료.")