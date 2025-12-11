import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException


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
def wait_for_element(driver, selector,by=By.CSS_SELECTOR,timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, f"[placeholder='{selector}']"))
        )

def wait_clickable(driver, selector, by=By.CSS_SELECTOR, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by,selector))
    )

def click_element(driver, selector: str):
    """Click element with data-testid."""
    element = wait_clickable(driver, selector)
    element.click()
    return element


def type_text(driver, selector: str, text: str):
    """Type text into element with data-testid."""
    element = wait_for_element(driver, selector)
    element.clear()
    element.send_keys(text)
    return element

# -----------------------------
# 로그인 기능
# -----------------------------
def login(driver):

    print("\n▶ 가입된 계정 로그인 진행 중...")


    type_text(driver,"Email","qa3team03@elicer.com")
    type_text(driver,"Password","@qa12345")
    click_element(driver,"[type='submit']")
    time.sleep(2)


    # 로그인 후 화면에 나타나는 요소를 기다리기
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[data-testid="PersonIcon"]')
        )
    )
    print("✔ 로그인 성공(메인 화면 로딩 확인됨)")



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
    driver.quit()


# -----------------------------
# URL 출력
# -----------------------------
def print_current_url(driver):
    print(f"현재 URL: {driver.current_url}")

#로그인 창에서 유효하지 않은 아이디,ps 입력 시
def test_wrong_password(driver, email):
    print("\n▶ 잘못된 비밀번호 테스트 시작")

    navigate_to_login(driver)

    wait_clickable(driver, "[placeholder='Email']").send_keys(email)
    wait_clickable(driver, "[placeholder='Password']").send_keys("wrong_password!")
    wait_clickable(driver, "[type='submit']").click()

    try:
        error_element = driver.find_element(
            By.XPATH, "//p[contains(text(), 'Email or password does not match')]"
        )
        print("✔ 오류 메시지 확인됨:", error_element.text)
        assert "Email or password does not match" in error_element.text
        time.sleep(2)
        print("✔ 테스트 통과!")
    except NoSuchElementException:
        print("❌ 오류 메시지를 찾지 못했음")
        assert False, "Wrong password test failed - error message not found"

#8글자 이하 password 입력
def test_short_password(driver, email):
    print("\n▶ 짧은 비밀번호 테스트 시작")

    navigate_to_login(driver)

    wait_clickable(driver, "[placeholder='Email']").send_keys(email)
    wait_clickable(driver, "[placeholder='Password']").send_keys("12345")
    wait_clickable(driver, "[type='submit']").click()

    try:
        error_element = driver.find_element(
            By.XPATH, "//p[contains(text(), '8') or contains(text(), 'password')]"
        )
        print("✔ 짧은 비밀번호 오류 메시지 확인:", error_element.text)
        assert "8" in error_element.text or "password" in error_element.text
        time.sleep(2)
        print("✔ 테스트 통과!")
    except NoSuchElementException:
        print("❌ 짧은 비밀번호 오류 메시지를 찾지 못했음")
        assert False, "Short password test failed - error message not found"    
print("testfie")


    

