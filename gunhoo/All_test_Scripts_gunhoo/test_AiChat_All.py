import time
import pytest
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from saveJson_gunhoo import save_json

USERNAME = "qa3team03@elicer.com"
PASSWORD = "@qa12345"

LOGIN_URL = "https://accounts.elice.io/accounts/signin/me?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat&lang=en-US&org=qaproject"
CHAT_URL = "https://qaproject.elice.io/ai-helpy-chat"


# -------------------------
#  CLASS: ChatBotTester
# -------------------------

class ChatBotTester:
    def __init__(self, browser):
        # 브라우저 객체(WebDriver)를 받아서 테스트 클래스 내부에서 사용, class 생성시 무조건 만드는 함수
        self.browser = browser

    def send_message(self, message):
        # 챗봇 입력창 textarea 선택 후 메시지 입력 + 엔터 전송
        textarea = self.browser.find_element(By.CSS_SELECTOR, "textarea[name='input']")
        textarea.send_keys(message)
        textarea.send_keys(Keys.ENTER)

    def wait_for_answer(self, selector=".elice-aichat__markdown", min_wait_time=10):
        """
        챗봇의 답변이 "끝나는 시점"을 기다리는 함수.
        - 일정 시간(min_wait_time) 동안 답변이 계속 변하는지 체크
        - 더 이상 텍스트 변화가 없으면 답변 완료로 판단
        """
        start_time = time.time()
        previous_text = ""

        while True:
            current_text = self.browser.find_element(By.CSS_SELECTOR, selector).text
            text_changed = (current_text != previous_text)
            previous_text = current_text

            elapsed = time.time() - start_time

            # 최소 대기시간이 지나기 전까지는 계속 기다림
            if elapsed < min_wait_time:
                time.sleep(1)
                continue

            # 일정 시간이 지난 후 텍스트 변화가 없으면 종료
            if not text_changed:
                break

            time.sleep(1)

    def get_answer(self):
        # 챗봇 답변 엘리먼트에서 텍스트만 추출하여 반환
        element = self.browser.find_element(By.CSS_SELECTOR, ".elice-aichat__markdown")
        return element.text

    def new_chat(self):
        """
        사이드바에 있는 '새 대화' 버튼 클릭.
        - 새 대화 버튼 클릭 후, 입력칸 로딩 완료까지 대기
        """
        try:
            btn = self.browser.find_element(
                By.XPATH, "//a[.//span[contains(text(), '새 대화')]]"
            )
            btn.click()
            print("새 대화 버튼 클릭 완료")

            # 입력창이 다시 로딩될 때까지 기다림
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='input']"))
            )
            print("새 대화창 로딩 완료")

        except Exception as e:
            print("새 대화 버튼 클릭 실패:", e)


# -------------------------
#  PYTEST FIXTURE
# -------------------------

@pytest.fixture(scope="session")
def browser():
    """
    pytest에서 한 세션 동안 공용으로 사용할 브라우저 생성.
    테스트 끝나면 자동으로 종료됨.
    """
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture(scope="session", autouse=True)
def test_login(browser):
    """
    테스트 세션이 시작될 때 자동으로 로그인 처리.
    이후 모든 테스트에서 로그인된 상태로 진행됨.
    """
    browser.get(LOGIN_URL)
    time.sleep(1)

    browser.find_element(By.NAME, "loginId").send_keys(USERNAME)
    browser.find_element(By.NAME, "password").send_keys(PASSWORD)
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    time.sleep(2)  # 로그인 안정화 대기


# -------------------------
#  TEST CASE
# -------------------------

def test_chat_input(browser):
    """
    기본 챗봇 입력 테스트:
    1) 질문 입력
    2) 답변 대기
    3) JSON 저장
    4) 새 대화 페이지로 이동
    """
    tester = ChatBotTester(browser)

    question = "사과가 뭐야?"
    tester.send_message(question)
    tester.wait_for_answer(selector=".elice-aichat__markdown", min_wait_time=5)

    answer = tester.get_answer()

    #JSON 저장 함수 utils.py에서 호출
    save_json("TC-CHAT-001.json", {"question": question, "answer": answer})

    # 테스트 종료 전 새 대화로 이동
    tester.new_chat()

    time.sleep(30)  # 브라우저 닫히기 전에 확인용



