#AI가 말하는 거 가져오는 모듈

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

AI_CHAT_BUBBLE = (By.CSS_SELECTOR, "div.elice-aichat__markdown")

def get_latest_ai_answer(driver, wait, timeout=10):
    """화면에 표시된 답변들 중 가장 마지막(최신) 답변을 가져옵니다."""
    try:
        # 답변 요소가 나타날 때까지 대기
        wait.until(EC.presence_of_element_located(AI_CHAT_BUBBLE))
   
        time.sleep(2) 
        
        all_responses = driver.find_elements(*AI_CHAT_BUBBLE)
        
        if all_responses:
            #가장 마지막 요소의 텍스트 반환
            return all_responses[-1].text
        return "답변 요소를 찾을 수 없음"
    except Exception as e:
        return f"답변 추출 중 오류 발생: {e}"