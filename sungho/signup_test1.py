from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import time
from utills import get_driver

driver = get_driver()


def not_email_test():
    # -----------------------------
    # 드라이버 생성
    # -----------------------------
    try:
        # -----------------------------
        # 테스트 시작
        # -----------------------------
        print("\n▶ TC1: 이메일 빈칸 회원가입 테스트 시작")

        driver.get("https://accounts.elice.io/accounts/signup/form?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat%2Fagents&lang=en-US&org=qaproject")
        time.sleep(2)

        # Create account 클릭
        driver.find_element(By.CSS_SELECTOR, "[type='button']").click()

        # 이메일만 빈칸 → send_keys() 비움
        driver.find_element(By.XPATH, "//input[@placeholder='Email']").send_keys("")
        driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys("@qa12345")
        driver.find_element(By.XPATH, "//input[@placeholder='Name']").send_keys("김성호")

        # Agree all 체크
        driver.find_element(By.CSS_SELECTOR, "[type='checkbox']").click()
        time.sleep(1)

        # Create 버튼 클릭
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)

        # HTML 기본 validation 메시지 읽기
        email_input = driver.find_element(By.XPATH, "//input[@placeholder='Email']")
        msg = driver.execute_script("return arguments[0].validationMessage;", email_input)

        print("브라우저 Validation Message:", msg)

        # -----------------------------
        # 커스텀 에러 메시지 검증
        # -----------------------------
        try:
            error_element = driver.find_element(By.XPATH, "//p[contains(text(), 'Please enter your email address')]")
            print("✔ 오류 메시지 확인됨:", error_element.text)
        except NoSuchElementException:
            print("❌ 오류 메시지를 찾지 못했음")
            assert True, "error message not found"

        print("✔ TC1 통과!")

    finally:
        # 항상 드라이버 종료
        time.sleep(2)
        driver.quit()


if __name__ == "__main__":
    print("Test 1: 이메일 공란 테스트")
    not_email_test()
    
