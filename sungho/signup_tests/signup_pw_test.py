from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utills import *


#TC05 비밀번호 길이 제한 검증 테스트 
def short_password_test():
   
    try:
        print("▶ TC005: 8자 미만 패스워드 테스트")

        driver = get_driver()
        email = generate_unique_username()+"@naver.com"
        password = "@qa1234"
        name = "김성호"
        signup(driver, email, password, name)

        
        try:
            error_element = driver.find_element(By.XPATH, "//p[contains(text(), 'Please make your password stronger!')]")
            print("✔ 오류 메시지 확인됨:", error_element.text)
            print("✔ TC5 통과!")
            save_screenshot(driver,"signup_pw","TC05_short_ps")
            time.sleep(2)
        except NoSuchElementException:
            print("❌ Please make your password stronger! 메시지를 찾지 못했음")

    finally:
        driver.quit()
# TC06 비밀번호 조합 규칙 검증 테스트
def wrong_rule_password_test():

    try:
        driver = get_driver()

        invalid_passwords = [
            "qa123456",   # 특수문자 없음
            "qa@qaqaqa",  # 숫자 없음
            "12345678"    # 숫자만
        ]

        print("▶ TC06: 비밀번호 조합 규칙 테스트 시작")

        # 1️⃣ 회원가입 페이지 진입 (한 번만)
        open_signup_page(driver)

        email = generate_unique_username() + "@naver.com"
        name = "김성호"

        # 2️⃣ email, name 한 번만 입력
        fill_signup_form(driver, email=email, name=name)

        for password in invalid_passwords:

            print(f"▶ 테스트 패스워드: {password}")
            password_input = driver.find_element(By.CSS_SELECTOR, "[placeholder='Password']")
            password_input.send_keys(Keys.CONTROL, "a")
            password_input.send_keys(Keys.BACKSPACE)
            password_input.send_keys(password)
  

            # 4️⃣ 제출
            submit_signup(driver)

            # 5️⃣ 에러 메시지 검증
            try:
                error_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//p[contains(text(), 'Please make your password stronger!')]")
                    )
                )
                print("✔ 오류 메시지 확인:", error_element.text)
                save_screenshot(driver,"signup_pw","TC06_wrong_rule_pw")
                time.sleep(1)
            except TimeoutException:
                print("❌ 오류 메시지를 찾지 못했음")

            time.sleep(1)
        

        print("✔ TC06 전체 패스워드 조합 테스트 완료")

    finally:
        driver.quit()
#TC07: 정상 패스워드 입력
def right_password_test():

    try:
        driver = get_driver()
        email = generate_unique_username()+"@naver.com"
        password = "@qa12345"
        name = "김성호"
        print("▶ TC07: 비밀번호 조합 규칙 테스트 시작")
        signup(driver, email, password, name)
        welcome_text = WebDriverWait(driver, 10).until(
             EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Nice to meet you again')]")
            )
        )
        assert welcome_text.is_displayed()
        print("✔ 계정 정상적으로 생성")
        save_screenshot(driver,"signup_pw","TC07_right_pw")
    finally:
        driver.quit()


if __name__ == "__main__":
    print("Test 5: 8자 미만 패스워드 테스트")
    short_password_test()
    print("Test 6: 잘못된 조합의 패스워드 테스트")
    wrong_rule_password_test()
    print("Test 7: 정상적인 비밀번호 입력 테스트")
    right_password_test()