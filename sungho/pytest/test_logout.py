from selenium.common.exceptions import TimeoutException
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utills import *

def test_login_logout(driver):
        
        login(driver, "qa3team03@elicer.com", "@qa12345")
        print("로그인 완료")
        logout(driver)

        type_text(driver, "Password", "@qa12345")
        click_element(driver, "button[type='submit']")
        
        WebDriverWait(driver, 15).until(
                EC.url_contains("/ai-helpy-chat")
            )
        icon = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[data-testid="PersonIcon"]')
        )
    )
        assert icon.is_displayed()
        print("✔ ai-helpy-chat 페이지 이동 확인 (테스트 성공)")
        print("TC18 재로그인 성공")
    
