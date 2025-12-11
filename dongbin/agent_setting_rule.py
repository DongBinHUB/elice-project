import os
import sys
import time
current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.join(current_dir, '..')
sys.path.append(project_root)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from utils.driver_setup import login_driver
from utils.login_module import perform_login

agent_rule = "길 찾기용 에이전트 입니다.  서울 위주 대중교통을 안내합니다"
file_name = "elice_logo.png"
file_path = os.path.join(current_dir, file_name)

USER_EMAIL = "qa3team03@elicer.com"  
USER_PASSWORD = "@qa12345" 
LOGIN_URL = "https://accounts.elice.io/accounts/signin/me?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat%2Fagents&lang=en-US&org=qaproject"

driver = login_driver(LOGIN_URL) 
driver.maximize_window()

# 2. 로그인 실행
perform_login(driver, USER_EMAIL, USER_PASSWORD)
print(f"로그인 후 현재 URL: {driver.current_url}") 
time.sleep(5)

wait = WebDriverWait(driver, 10)
print("--- 에이전트 생성 프로세스 시작 ---")

try:
    agent_make_btn = wait.until(
      EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='만들기']")))
   
    agent_make_btn.click()
    print("[SUCCESS]'만들기'버튼 클릭 성공.")
       
    agent_make_name = wait.until(
        EC.visibility_of_element_located((By.NAME, "name"))
    )        
    time.sleep(1)
   
    agent_make_name.send_keys("동빈")
    print("[SUCCESS] 이름 입력 성공!")
    
    time.sleep(1)
    
    agent_make_name = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='에이전트의 짧은 설명을 입력해보세요']"))
    )
   
    agent_make_name.send_keys("길 찾기 에이전트 입니다")
    print(f"[SUCCESS] 한줄 소개 입력 성공!")
    
    time.sleep(1)
    
    agent_make_rule = driver.find_element(By.NAME ,'systemPrompt') 
    agent_make_rule.send_keys(agent_rule)
    print(f"[SUCCESS] 규칙 입력 성공!")
    
    time.sleep(1)
    
    agent_starter_field = driver.find_element(By.XPATH, '//input[@placeholder="이 에이전트의 시작 대화를 입력하세요"]')
    agent_starter_field.send_keys("대중교통")
    print(f"[SUCCESS] 시작 대화 입력 성공!")
    
    file_upload = driver.find_element(By.XPATH,"//input[@type='file']")
    file_upload.send_keys(file_path)
    
    print(f"[SUCCESS] 파일 업로드 완료: {file_name}")
    
    
    
    
    time.sleep(2) # 최종 결과 확인을 위한 대기
      
except Exception as e:
    print(f"\n[CRITICAL ERROR] 자동화 프로세스 중 오류 발생.")
    print(f"오류 클래스: {e.__class__.__name__}")
    print(f"오류 메시지: {e}")
    
finally:
    if 'driver' in locals() and driver:
        driver.quit()
        print("\n[INFO] 드라이버 종료.")