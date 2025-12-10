import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# 기본 설정
BASE_LOGIN_URL = "https://accounts.elice.io/accounts/signin/me?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat&lang=en-US&org=qaproject"


# -----------------------------
# 드라이버 생성
# -----------------------------
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    return driver


# -----------------------------
# 로그인 페이지 이동
# -----------------------------
def navigate_to_login(driver):
    driver.get(BASE_LOGIN_URL)
    time.sleep(2)


# -----------------------------
# 요소 기다리기
# -----------------------------
def wait_clickable(driver, selector, by=By.CSS_SELECTOR, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, selector))
    )


# -----------------------------
# 로그인 기능
# -----------------------------
def login(driver, email, password):
    print("\n▶ 로그인 진행 중...")

    wait_clickable(driver, "[placeholder='Email']").send_keys(email)
    wait_clickable(driver, "[placeholder='Password']").send_keys(password)
    wait_clickable(driver, "[type='submit']").click()

    time.sleep(2)
    print("✔ 로그인 완료")

#재로그인 기능
def relogin(driver,password):
    print("\n▶ 로그인 진행 중...")
    wait_clickable(driver, "[placeholder='Password']").send_keys(password)
    wait_clickable(driver, "[type='submit']").click()

    time.sleep(2)
    print("✔ 재로그인 완료")




# -----------------------------
# 로그아웃 기능
# -----------------------------
def logout(driver):
    print("\n▶ 로그아웃 진행 중...")

    wait_clickable(driver, '[data-testid="PersonIcon"]').click()
    wait_clickable(driver, "//p[contains(text(), '로그아웃')]", by=By.XPATH).click()

    time.sleep(1)
    print("✔ 로그아웃 완료")


# -----------------------------
# URL 출력
# -----------------------------
def print_current_url(driver):
    print(f"현재 URL: {driver.current_url}")

