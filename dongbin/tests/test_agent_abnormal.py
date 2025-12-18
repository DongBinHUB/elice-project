import pytest
import time
import json
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# 기존에 작성하신 유틸리티 함수 임포트
from utils.chat_utils import wait_for_AI_complete

# --- 선택자 및 설정 ---
AGENT_URL = "https://qaproject.elice.io/ai-helpy-chat/agents"
MAKE_BUTTON = (By.XPATH, "//a[normalize-space()='만들기']")
CHAT_CREATE_BUTTON = (By.CSS_SELECTOR, "button[value='chat']")
MESSAGE_TEXTAREA = (By.NAME, "input")
AI_CHAT_BUBBLE = (By.CSS_SELECTOR, "div.elice-aichat__markdown")

def test_agent_abnormal_input(driver):
    """비정상 입력(의미 없는 문자열)에 대한 AI 에이전트 반응 테스트"""
    wait = WebDriverWait(driver, 15)
    conversation_history = []
    
    # 1. 에이전트 페이지 이동
    driver.get(AGENT_URL)
    print(f"\n[INFO] 에이전트 페이지 접속 완료")

    # 2. '만들기' 버튼 클릭
    make_btn = wait.until(EC.element_to_be_clickable(MAKE_BUTTON))
    make_btn.click()
    
    # 3. '대화로 만들기' 클릭
    ai_chat_make = wait.until(EC.element_to_be_clickable(CHAT_CREATE_BUTTON))
    ai_chat_make.click()
    print("[SUCCESS] 에이전트 대화 생성 모드 진입")

    # 4. 비정상 질문 반복 테스트 (4회)
    scenario_questions = ["ㅁㄴㅇ123"] * 4
    
    for i, question in enumerate(scenario_questions, 1):
        # 질문 전송 전 현재 말풍선 개수 파악
        current_bubbles = driver.find_elements(*AI_CHAT_BUBBLE)
        before_count = len(current_bubbles)
        
        print(f"[Step {i}] 입력: {question}")
        
        # 메시지 입력 및 전송
        input_box = wait.until(EC.element_to_be_clickable(MESSAGE_TEXTAREA))
        input_box.send_keys(question)
        input_box.send_keys(Keys.ENTER)
        
        # AI 응답 대기 (기존 유틸리티 활용)
        final_answer = wait_for_AI_complete(driver, before_count, timeout=60)
        
        # 결과 기록
        conversation_history.append({
            "order": i,
            "user_input": question,
            "ai_response": final_answer
        })
        
        # 검증: AI가 최소한 무언가 대답을 했는지 확인
        assert len(final_answer) > 0, f"{i}번째 응답이 비어있습니다."

    # 5. 테스트 결과 JSON 저장
    save_abnormal_log(conversation_history)
    print(f"[PASS] 비정상 입력 테스트 완료 (총 {len(conversation_history)}회)")

def save_abnormal_log(history):
    """비정상 테스트 결과를 JSON 파일로 저장"""
    # 폴더 경로 설정 (qa03/dongbin/results)
    results_dir = os.path.join(os.getcwd(), "dongbin", "results")
    os.makedirs(results_dir, exist_ok=True)
    file_path = os.path.join(results_dir, "abnormal_test_log.json")

    new_entry = {
        "test_type": "비정상 입력 테스트 (의미 없는 문자열)",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "full_chat": history
    }

    # 기존 데이터 로드 및 추가
    data = []
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list): data = [data]
        except:
            data = []
    
    data.append(new_entry)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"[INFO] 로그 저장 완료: {file_path}")