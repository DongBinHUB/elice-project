from selenium.common.exceptions import TimeoutException
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utills import *

#TC1 이메일 공란 회원가입 테스트
def test_space_email(driver):
    print("\n▶ TC001: 이메일 공란 입력 테스트")
    email = ""
    password = "@qa12345"
    name = "김성호"

    signup(driver, email, password, name)

    email_input = driver.find_element(By.XPATH, "//input[@placeholder='Email']")
    msg = driver.execute_script(
        "return arguments[0].validationMessage;", email_input
    )
    time.sleep(1)

    assert msg != ""  # 브라우저 validation 발생 확인
    print("▶ TC001: 이름 공란 입력 테스트 성공")


# TC2 잘못된 이메일 형식
def test_wrong_email_type(driver):
    print("\n▶ TC002: 잘못된 이메일 입력 테스트")
    email = generate_unique_username() + "naver.com"
    password = "@qa12345"
    name = "김성호"

    signup(driver, email, password, name)

    error = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.XPATH, "//p[contains(text(), 'Email address is incorrect.')]")
        )
    )

    assert "Email address is incorrect." in error.text
    save_screenshot(driver, "signup_email", "TC02_wrong_email_type")
    print("▶ TC002: 잘못된 이메일 입력 테스트 성공")


# TC3 정상 회원가입
def test_right_signup(driver,valid_signup_data):

    print("\n▶ TC003: 정상 회원가입 테스트")
    signup(driver, **valid_signup_data)

    WebDriverWait(driver, 15).until(
                EC.url_contains("/ai-helpy-chat")
            )
    icon = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[data-testid="PersonIcon"]')
        )
    )
    assert icon.is_displayed()
    save_screenshot(driver, "signup_email", "TC03_signup_success")
    print("▶ TC003: 정상 회원가입 테스트 성공")

# TC4 중복 이메일 회원가입
def test_duplicate_email(driver,valid_signup_data):

    print("\n▶ TC004: 중복된 이메일 입력 테스트")

    signup(driver,**valid_signup_data)
    WebDriverWait(driver, 10).until(
                EC.url_contains("/ai-helpy-chat")#회원가입 정상적으로 됐는지 확인
        )

    open_signup_page(driver)
    type_text(driver, "Email", valid_signup_data["email"])# 회원가입했던 이메일 입력 

    error = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.XPATH, "//p[contains(text(), 'This is an already registered email address.')]")
        )
    )

    assert "already registered email" in error.text
    save_screenshot(driver, "signup_email", "TC04_duplicate_email")
    print("▶ TC004: 중복된 이메일 입력 테스트 성공")
