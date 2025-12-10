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


driver.get("https://accounts.elice.io/accounts/signup/form?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat%2Fagents&lang=en-US&org=qaproject")
time.sleep(2)

#Create account 누르기
driver.find_element(By.CSS_SELECTOR, "[type='button']").click()

#회원가입 창에서 이메일, 비번, 이름 입력
driver.find_element(By.XPATH, "//input[@placeholder='Email']").send_keys("go3897@naver.com")
driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys("12345")
driver.find_element(By.XPATH, "//input[@placeholder='Name']").send_keys("김성호")

#Agree all 누르기
driver.find_element(By.CSS_SELECTOR, "[type='checkbox']").click()
time.sleep(1)

#Agree all 해제
driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']").click()

time.sleep(5)

