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
# 테스트할 질문 목록
# -----------------------------
QUESTIONS = [
    ("TC-CHAT-001", "사과가 뭐야?"),
    ("TC-CHAT-002", "사과는 어떻게 수확해?"),
    ("TC-CHAT-003", "교과서의 정의는?"),
]


# -----------------------------
# 여러 질문을 자동 반복 테스트
# -----------------------------
@pytest.mark.parametrize("tc_id, question", QUESTIONS)
def test_chatbot_multiple(browser, tc_id, question):
    tester = ChatBotTester(browser)

    # 1) 질문 전송
    tester.send_message(question)

    # 2) 챗봇 답변 완료까지 대기
    tester.wait_for_answer(min_wait_time=5)

    # 3) 답변 추출
    answer = tester.get_answer()

    # 4) JSON 저장
    save_json(f"{tc_id}.json", {"question": question, "answer": answer})

    # 5) 새 대화로 초기화
    tester.new_chat()

    time.sleep(1)


def test_chat_continuous_three(browser):
    """
    한 대화방에서 3개의 질문을 연속으로 묻고
    답변 3개를 하나의 JSON에 묶어서 저장하는 테스트
    """
    tester = ChatBotTester(browser)

    questions = [
        ("TC-CHAT-CONT-001-1", "체인소맨 : 레제편 영화를 보고 왔어"),
        ("TC-CHAT-CONT-001-2", "그 영화의 평은 어떤지 알아?"),
        ("TC-CHAT-CONT-001-3", "비슷한 느낌의 영화가 있을까?"),
    ]

    results = {}  # 3개의 질문+답변을 모두 저장할 dict

    for tc_id, q in questions:
        # 질문 전송
        tester.send_message(q)

        # 답변 대기
        tester.wait_for_answer(min_wait_time=5, max_wait_time=180)

        # 답변 추출
        answer = tester.get_answer()

        # 메모리에 저장
        results[tc_id] = {
            "question": q,
            "answer": answer
        }

        # 중요: 새 채팅이 아님! (연속 질문)
        time.sleep(1)

    # 최종 JSON 파일 저장
    save_json("TC-CHAT-004.json", results)

    # 마지막에 새 대화로 초기화해놓기 (다음 테스트 대비)
    tester.new_chat()

    time.sleep(1)