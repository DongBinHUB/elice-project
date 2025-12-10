import os
import sys
import time
current_dir = os.path.dirname(os.path.abspath(__file__))

# 상위 디렉토리 (프로젝트 루트)를 PATH에 추가
project_root = os.path.join(current_dir, '..')
sys.path.append(project_root)

# 필요한 기본 Selenium 모듈
from selenium.webdriver.support.ui import WebDriverWait
from utils.driver_setup import login_driver
from utils.login_module import perform_login

# 🚨 사용자 정의 상수 (테스트마다 동일)
USER_EMAIL = "qa3team03@elicer.com"  
USER_PASSWORD = "@qa12345" 
LOGIN_URL = "https://accounts.elice.io/accounts/signin/me?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat%2Fagents&lang=en-US&org=qaproject"

# 1. 브라우저 초기화 및 창 최대화 (가장 중요한 안정화 조치)
driver = login_driver(LOGIN_URL) 
driver.maximize_window()

# 2. 로그인 실행
perform_login(driver, USER_EMAIL, USER_PASSWORD)
print(f"[INFO] 로그인 후 현재 URL: {driver.current_url}") 

# 3. 페이지 로드 대기 (안정성을 위해 5초 대기)
time.sleep(5) 

# 4. WebDriverWait 객체 생성 (다음 테스트 로직에서 사용)
# 대부분의 요소 찾기 대기에 사용되므로 15초 정도로 설정하는 것이 안전합니다.
wait = WebDriverWait(driver, 15) 

print("--- 자동 로그인 및 초기 설정 완료. 테스트 로직을 여기에 추가하세요. ---")

# 🚨 [여기에 새로운 테스트 로직을 추가하세요] 🚨
# 예를 들어:
# from selenium.webdriver.common.by import By
# agent_make_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='만들기']")))
# agent_make_btn.click()


# 5. 테스트 종료 및 드라이버 종료 (항상 finally 블록 사용 권장)
try:
    pass # 실제 테스트 로직이 들어가는 곳
    
except Exception as e:
    print(f"\n[CRITICAL ERROR] 자동화 프로세스 중 오류 발생.")
    print(f"오류 클래스: {e.__class__.__name__}")
    print(f"오류 메시지: {e}")
    
finally:
    if 'driver' in locals() and driver:
        # 드라이버 객체가 존재할 경우에만 종료합니다.
        driver.quit()
        print("\n[INFO] 드라이버 종료.")