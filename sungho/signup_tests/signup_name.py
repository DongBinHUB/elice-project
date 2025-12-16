from selenium.common.exceptions import TimeoutException
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utills import *

#TC08 이름 미입력시 테스트
def space_name_test():
    try:
        driver = get_driver()
        print("▶ TC008: 이름 공란 입력 테스트")

        email = generate_unique_username()+"@naver.com"
        password = "@qa12345"
        name = ""
        signup(driver, email, password, name)

        name_input = driver.find_element(By.XPATH, "//input[@placeholder='Name']")
        msg = driver.execute_script("return arguments[0].validationMessage;", name_input)

        print("브라우저 Validation Message:", msg)

        try:
            error_element = driver.find_element(By.XPATH, "//p[contains(text(), 'Please enter your name')]")
            assert "enter your name" in error_element.text
            print("오류 메세지 확인됨:",error_element.text)
            
            print("TC08 통과")
        except NoSuchElementException:
            print("❌ Please enter your name! 메시지를 찾지 못했음")
            save_screenshot(driver,"signup_name","TC08_space_name")
    finally:
        driver.quit()
        


#TC09 제목필드에 긴 제목 입력하기
def too_long_name_test():
    try:
        print("▶ TC009: 긴 제목 입력 테스트")
        driver = get_driver()
        email = generate_unique_username()+"@naver.com"
        password = "@qa12345"
        name = "가나다라마바사아자차카타파하아야어여오유우이"
        signup(driver,email,password,name)
        save_screenshot(driver,"signup_name","TC09_long_name_input")
        try:
            error_element = driver.find_element(By.XPATH, "//p[contains(text(), 'Please enter your name')]")
            assert "enter your name" in error_element.text
            print("오류 메세지 확인됨:",error_element.text)
            
            print("TC08 통과")
        except NoSuchElementException:
            print("❌ 어떠한 오류메시지를 찾지 못했음")
            print("❌ TC009: 테스트 실패")
            save_screenshot(driver,"signup_name","TC09_long_name")
    finally:
        driver.quit()
#TC010: 정상적인 이름 입력 테스트
def right_name_test():
    try:
        print("▶ TC010: 정상적인 이름 입력 테스트")
        driver = get_driver()
        email = generate_unique_username()+"@naver.com"
        password = "@qa12345"
        name = "김성호"
        signup(driver,email,password,name)
        welcome_text = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Nice to meet you again')]")
            )
        )
        assert welcome_text.is_displayed()
        print("✔ 계정 정상적으로 생성")
        save_screenshot(driver,"signup_name","TC10_right_name")
        print("TC010 테스트 성공")
    finally:
        driver.quit()

if __name__ == "__main__":
    print("Test 8: 이름 빈칸으로 입력 테스트")
    space_name_test()
    print("\nTest 9: 너무 긴 이름 입력 테스트")
    too_long_name_test()
    print("\nTest 10: 정상적 이름 입력 테스트")
    right_name_test()


            

        