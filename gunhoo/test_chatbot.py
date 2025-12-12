import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from chatbot_tester import ChatBotTester # 챗봇 동작 로직 클래스
from saveJson_gunhoo import save_json # json 저장 유틸

# -----------------------------
# 로그인 정보 / URL 설정
# -----------------------------
USERNAME = "qa3team03@elicer.com"
PASSWORD = "@qa12345"

LOGIN_URL = "https://accounts.elice.io/accounts/signin/me?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat&lang=en-US&org=qaproject"

# -----------------------------
# pytest 브라우저 생성 FIXTURE (파이테스트 - 테스트 이전 미리 준비하는 것)
# -----------------------------
@pytest.fixture(scope="session") 
def browser(): # 테스트 전체(session) 동안 사용할 브라우저를 1개 생성하는 함수
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10) # 기본 암시적 대기 설정
    yield driver
    driver.quit() # 세션 종료 후 브라우저 자동 종료

# -----------------------------
# 자동 로그인 FIXTURE
# -----------------------------

@pytest.fixture(scope="session", autouse=True)
def test_login(browser): # 테스트 시작 시 자동으로 로그인 처리
    browser.get(LOGIN_URL)
    time.sleep(1)

    browser.find_element(By.NAME, "loginId").send_keys(USERNAME)
    browser.find_element(By.NAME, "password").send_keys(PASSWORD)
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    time.sleep(2)  # 로그인 안정화 대기

# -----------------------------
# 기본 챗봇 입력 테스트
# -----------------------------
def test_chat_input(browser):
    """
    기본 챗봇 입력 테스트:
    1) 질문 전송
    2) 챗봇 답변 대기
    3) 답변 추출
    4) JSON 저장
    5) 새 대화 페이지로 리셋
    """
    tester = ChatBotTester(browser)

    question = "사과가 뭐야?"
    tester.send_message(question)
    tester.wait_for_answer(selector=".elice-aichat__markdown", min_wait_time=5)

    # 챗봇 답변 추출
    answer = tester.get_answer()

    # JSON 파일 저장
    save_json("TC-CHAT-001.json", {"question": question, "answer": answer})

    # 새 대화 화면으로 이동
    tester.new_chat()

    time.sleep(3)
