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

USERNAME = "qa3team03@elicer.com"
PASSWORD = "@qa12345"

LOGIN_URL = "https://accounts.elice.io/accounts/signin/me?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat&lang=en-US&org=qaproject"
CHAT_URL = "https://qaproject.elice.io/ai-helpy-chat"

@pytest.fixture(scope="session")
def browser():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    yield driver  # 브라우저는 테스트 중에 지속적으로 사용됨
    driver.quit()  # 세션 끝날 때 브라우저 종료


@pytest.fixture(scope="session", autouse=True)
def test_login(browser):
    # 로그인 페이지 접속
    browser.get(LOGIN_URL)
    time.sleep(1)

    # 아이디/비번 입력
    browser.find_element(By.NAME, "loginId").send_keys(USERNAME)
    browser.find_element(By.NAME, "password").send_keys(PASSWORD)

    # 로그인 버튼 클릭
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)


def wait_for_full_answer(browser, selector, min_wait_time=10):
    """무조건 최소 min_wait_time 초 기다린 후, 텍스트 변화가 멈출 때 종료"""
    
    start_time = time.time()
    previous_text = ""
    
    while True:
        current_text = browser.find_element(By.CSS_SELECTOR, selector).text

        # 텍스트 변화 감지
        text_changed = (current_text != previous_text)
        previous_text = current_text

        elapsed = time.time() - start_time

        # 최소 대기 시간 이전이면 계속 기다림
        if elapsed < min_wait_time:
            time.sleep(1)
            continue

        # 최소 대기 시간 이후 → 변화가 없으면 종료
        if not text_changed:
            break

        time.sleep(1)


def test_chat_input(browser):
    # 챗봇 입력란 찾기
    textarea = browser.find_element(By.CSS_SELECTOR, "textarea[name='input']")
    
    # 입력값 전송
    textarea.send_keys("사과가 뭐야?")
    textarea.send_keys(Keys.ENTER)  # 엔터를 눌러 전송
    wait_for_full_answer(browser, ".elice-aichat__markdown", min_wait_time=5)
    
    # AI 답변 텍스트 추출
    response_element = browser.find_element(By.CSS_SELECTOR, ".elice-aichat__markdown")
    answer = response_element.text

    # JSON으로 저장
    chat_log = {
        "question": "사과가 뭐야?",
        "answer": answer
    }

    with open("TC-CHAT-001.json", "w", encoding="utf-8") as f:
        json.dump(chat_log, f, ensure_ascii=False, indent=4)

    print("AI 답변 저장 완료:", answer)

    try:
        new_chat_btn = browser.find_element(
            By.XPATH, "//a[.//span[contains(text(), '새 대화')]]"
        )
        new_chat_btn.click()
        print("새 대화 버튼 클릭 완료")

        # 새 대화창 로딩될 때까지 입력창 대기
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='input']"))
        )
        print("새 대화창 로딩 완료")

        time.sleep(30)

    except Exception as e:
        print("새 대화 버튼 클릭 실패:", e)