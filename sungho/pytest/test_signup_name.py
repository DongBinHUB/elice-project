from selenium.common.exceptions import TimeoutException
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utills import *


# TC08: 이름 미입력
def test_space_name(driver):
    print("▶ TC008: 이름 공란 입력 테스트")

    email = generate_unique_username() + "@naver.com"
    password = "@qa12345"
    name = ""

    signup(driver, email, password, name)

    name_input = driver.find_element(By.XPATH, "//input[@placeholder='Name']")
    msg = driver.execute_script(
        "return arguments[0].validationMessage;", name_input
    )
    print("브라우저 Validation Message:", msg)
    assert msg !=""
    save_screenshot(driver, "signup_name", "TC08_space_name")


# TC09: 이름 너무 김
def test_too_long_name(driver):
    print("▶ TC009: 긴 이름 입력 테스트")

    email = generate_unique_username() + "@naver.com"
    password = "@qa12345"
    name = "가나다라마바사아자차카타파하아야어여오유우이"

    signup(driver, email, password, name)
    save_screenshot(driver, "signup_name", "TC09_long_name_input")

    try:
        error = driver.find_element(
            By.XPATH, "//p[contains(text(), 'your name is too long')]"
        )
        assert "too long" in error.text
    except NoSuchElementException:
        save_screenshot(driver, "signup_name", "TC09_long_name_fail")
        pytest.fail("이름 길이 제한 에러 메시지 없음")


# TC10: 정상 이름
def test_right_name(driver):
    print("▶ TC010: 정상적인 이름 입력 테스트")

    email = generate_unique_username() + "@naver.com"
    password = "@qa12345"
    name = "김성호"

    signup(driver, email, password, name)

    welcome_text = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Nice to meet you again')]")
        )
    )

    assert welcome_text.is_displayed()
    save_screenshot(driver, "signup_name", "TC10_right_name")
