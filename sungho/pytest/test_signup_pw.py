from selenium.common.exceptions import TimeoutException
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utills import *
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utills import *


# TC05: 8자 미만 비밀번호 테스트
def test_short_password(driver):
    email = generate_unique_username() + "@naver.com"
    password = "@qa1234"   # 7자
    name = "김성호"

    signup(driver, email, password, name)

    error = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.XPATH, "//p[contains(text(), 'Please make your password stronger!')]")
        )
    )

    save_screenshot(driver, "signup_pw", "TC05_short_password")
    assert "Please make your password stronger!" in error.text


# TC06: 비밀번호 조합 규칙 테스트
def test_wrong_rule_password(driver):
    invalid_passwords = [
        "qa123456",   # 특수문자 없음
        "qa@qaqaqa",  # 숫자 없음
        "12345678"    # 숫자만
    ]

    open_signup_page(driver)

    email = generate_unique_username() + "@naver.com"
    name = "김성호"
    fill_signup_form(driver, email=email, name=name)

    for password in invalid_passwords:
        password_input = driver.find_element(By.CSS_SELECTOR, "[placeholder='Password']")
        password_input.send_keys(Keys.CONTROL, "a")
        password_input.send_keys(Keys.BACKSPACE)
        password_input.send_keys(password)

        submit_signup(driver)

        error = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//p[contains(text(), 'Please make your password stronger!')]")
            )
        )

        save_screenshot(driver, "signup_pw", f"TC06_wrong_rule_{password}")
        assert "Please make your password stronger!" in error.text


# TC07: 정상 비밀번호 입력
def test_right_password(driver):
    email = generate_unique_username() + "@naver.com"
    password = "@qa12345"
    name = "김성호"

    signup(driver, email, password, name)

    welcome = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Nice to meet you again')]")
        )
    )

    save_screenshot(driver, "signup_pw", "TC07_right_password")
    assert welcome.is_displayed()
