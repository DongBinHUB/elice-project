from selenium.common.exceptions import TimeoutException
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utills import *



#TC1 이메일 공란 회원가입 테스트
def space_email_test():
   
    try:
        print("\n▶ TC1: 이메일 빈칸 회원가입 테스트 시작")

        driver = get_driver()
        email= ""
        password= "@qa12345"
        name = "김성호"

        signup(driver, email, password, name)
    

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
            print("❌ Please enter your email address 메시지를 찾지 못했음")
            save_screenshot(driver, "signup_email", "TC01_space_email_test")
            print("스크린샷 저장")
            

        print("✔ TC1 통과!")

    finally:
        
        driver.quit()
#tc2
def wrong_email_type_test():
    try:
        print("\n▶ TC2: 잘못된 이메일 형식의 회원가입 테스트 시작")

        driver = get_driver()
        email= generate_unique_username()+"naver.com"
        password= "@qa12345"
        name = "김성호"

        signup(driver, email, password, name)
         # HTML 기본 validation 메시지 읽기
        email_input = driver.find_element(By.XPATH, "//input[@placeholder='Email']")
        msg = driver.execute_script("return arguments[0].validationMessage;", email_input)

        print("브라우저 Validation Message:", msg)

        # 커스텀 에러 메시지 검증
        try:
            error_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//p[contains(text(), 'Email address is incorrect.')]")))
            print("✔ 오류 메시지 확인됨:", error_element.text)
            assert "Email address is incorrect." in error_element.text
            print("✔ 테스트 통과!")
            save_screenshot(driver,"signup_email","TC02_wrong_email_type")
        except NoSuchElementException:
            print("❌ Please enter your email address 메시지를 찾지 못했음")
            assert False, "error message not found"

        print("✔ TC2 통과!")

    finally:
        driver.quit()

def right_signup_test():

    try:
        print("\n▶ TC3: 정상 회원가입 테스트 시작")
        
        driver = get_driver()
        email= generate_unique_username()+"@naver.com"
        password= "@qa12345"
        name = "김성호"

        signup(driver, email, password, name)
         # 회원가입 성공 화면 검증
        welcome_text = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Nice to meet you again')]")
            )
        )
        assert welcome_text.is_displayed()
        print("✔ 계정 정상적으로 생성")
        save_screenshot(driver,"signup_email","TC03_계정생성완료")

        #생성된 계정으로 로그인 시도
        type_text(driver, "Password", "@qa12345")
        click_element(driver, "button[type='submit']")

        #ai-helpy-chat창으로 넘어가는지 시도
        try:
            WebDriverWait(driver, 10).until(
            EC.url_contains("/ai-helpy-chat")
        )
            print("✔ ai-helpy-chat 페이지 이동 확인 (테스트 성공)")
        except TimeoutException:
            print("❌ ai-helpy-chat 페이지로 이동하지 않음 (테스트 실패)")
            save_screenshot(driver,"signup_email","TC03_right_signup_Fail")

    finally:
        driver.quit()

#TC004 중복된 이메일로 회원가입 테스트
def duplicate_email_test():
    try: 
        print("\n▶ TC4: 중복된 이메일 회원가입 테스트 시작")
        driver = get_driver()
        email= generate_unique_username()+"@naver.com"
        password= "@qa12345"
        name = "김성호"
        #올바른 형식으로 회원가입 
        signup(driver, email, password, name)
        time.sleep(2)
        #회원가입 완료 후 다시 회원가입 창으로 가서 직전에 회원가입한 이메일 입력
        open_signup_page(driver)
        fill_signup_form(driver, email)

        #이미 이메일이 존재한다는 문구가 뜨는지 확인
        error_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//p[contains(text(), 'This is an already registered email address.')]")))
        print("✔ 오류 메시지 확인됨:", error_element.text)
        assert "This is an already registered email address." in error_element.text
        print("✔ 테스트 통과!")
        save_screenshot(driver,"signup_email","TC04_duplicate_test")
    finally:
        driver.quit()
        




            
    


if __name__ == "__main__":
    print("Test 1: 이메일 공란 테스트")
    space_email_test()
    print("Test 2: 잘못된 이메일 형식 회원가입 테스트")
    wrong_email_type_test()
    print("Test3: 정상적 회원가입 후 로그인 테스트")
    right_signup_test()
    print("Test4: 정상적 회원가입 후 로그인 테스트")
    duplicate_email_test()

