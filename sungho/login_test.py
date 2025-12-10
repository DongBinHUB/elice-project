from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

# 크롬 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# 드라이버 생성
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.implicitly_wait(10)

#로그인 홈페이지 접속
driver.get("https://accounts.elice.io/accounts/signin/me?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat&lang=en-US&org=qaproject")
time.sleep(2)

#로그인 이메일 ,비번 입력 후 login 버튼 누르기 
driver.find_element(By.CSS_SELECTOR, "[placeholder='Email']").send_keys("qa3team03@elicer.com")
driver.find_element(By.CSS_SELECTOR, "[placeholder='Password']").send_keys("@qa12345")
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, "[type='submit']").click()
time.sleep(5)
print("로그인 완료")

#올바르게 접속됐는지 주소 확인
current_url = driver.current_url
print(f"\n현재 URL: {current_url}")
time.sleep(2)

#로그아웃
driver.find_element(By.CSS_SELECTOR, '[data-testid="PersonIcon"]').click()
time.sleep(1)
driver.find_element(By.XPATH, "//p[contains(text(), '로그아웃')]").click()
time.sleep(2)

current_url = driver.current_url
print(f"\n현재 URL: {current_url}")
time.sleep(2)
print("로그아웃 완료")

#로그아웃 후 재 로그인
driver.find_element(By.CSS_SELECTOR, "[placeholder='Password']").send_keys("@qa12345")
driver.find_element(By.CSS_SELECTOR, "[type='submit']").click()
time.sleep(2)
print("재로그인 정상적 완료")
