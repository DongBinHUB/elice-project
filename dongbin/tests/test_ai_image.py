import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

def test_ai_image_generation(driver):
    """AI 이미지 생성 기능 테스트"""
    wait = WebDriverWait(driver, 20)
    
    # 1. 메인 페이지 이동
    if "tools" in driver.current_url:
        driver.get("https://qaproject.elice.io/ai-helpy-chat")

    # 2. '+' 버튼 클릭 
    PLUS_BUTTON = (By.CSS_SELECTOR, "div.e1826rbt2 button")
    plus_btn = wait.until(EC.element_to_be_clickable(PLUS_BUTTON))
    driver.execute_script("arguments[0].click();", plus_btn)
    
    # 3. '이미지 생성' 메뉴 선택
    image_menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='이미지 생성']")))
    image_menu.click()
    
    # 4. 프롬프트 입력 및 전송
    input_box = wait.until(EC.element_to_be_clickable((By.NAME, "input")))
    input_box.send_keys("사과")
    input_box.send_keys(Keys.ENTER)
    
    # 5. 결과 검증 (Assertion)
    print("이미지 생성 대기 중...")
    result_img = WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.elice-aichat__markdown img"))
    )
    
    assert result_img.is_displayed(), "이미지가 화면에 노출되지 않았습니다."
    assert "http" in result_img.get_attribute("src"), "이미지 경로가 잘못되었습니다."
    print("\n[PASS] 이미지 생성 테스트 성공")