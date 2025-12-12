import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ChatBotTester:
    """
    챗봇 테스트를 위해 공통으로 사용하는 동작 모음 클래스.
    메시지 전송, 답변 대기, 새 대화 버튼 클릭 등을 담당한다.
    """
    def __init__(self, browser):
        # pytest FIXTURE에서 전달받은 WebDriver(브라우저), init 는 클래스 생성시 반드시 만드는 함수
        self.browser = browser

    # ------------------------------------------------
    # 1. 메시지 전송
    # ------------------------------------------------

    def send_message(self, message): #챗봇 입력창에 텍스트를 입력하고 엔터를 눌러 전송
        textarea = self.browser.find_element(By.CSS_SELECTOR, "textarea[name='input']")
        textarea.send_keys(message)
        textarea.send_keys(Keys.ENTER)

def wait_for_answer(
    self,
    spinner_selector=".elice-aichat__spinner",
    answer_selector=".elice-aichat__markdown",
    stable_duration=1.0
):
    """
    가장 안정적인 챗봇 답변 대기 방식:
    1) 로딩 스피너가 사라질 때까지 대기
    2) 답변 텍스트 요소가 나타날 때까지 대기
    3) 텍스트가 일정 시간(stable_duration) 동안 변하지 않으면 완료
    """

    # ------------------------------------
    # 1) 로딩 스피너가 사라질 때까지 대기
    # ------------------------------------
    while True:
        try:
            self.browser.find_element(By.CSS_SELECTOR, spinner_selector)
            time.sleep(0.2)
        except:
            break  # 스피너가 없어짐 → 다음 단계 진행

    # ------------------------------------
    # 2) 답변 텍스트가 나타날 때까지 대기
    # ------------------------------------
    WebDriverWait(self.browser, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, answer_selector))
    )

    # ------------------------------------
    # 3) 텍스트 안정화 대기
    # ------------------------------------
    prev_text = ""
    stable_start = None

    while True:
        current_text = self.browser.find_element(By.CSS_SELECTOR, answer_selector).text

        if current_text != prev_text:
            prev_text = current_text
            stable_start = time.time()  # 변화 시작
        else:
            # 일정 시간 동안 변화 없으면 끝
            if stable_start and (time.time() - stable_start) >= stable_duration:
                break

        time.sleep(0.2)


    # ------------------------------------------------
    # 3. 챗봇 답변 가져오기
    # ------------------------------------------------

    def get_answer(self):
        """가장 최근 챗봇 답변 텍스트를 반환"""
        element = self.browser.find_element(By.CSS_SELECTOR, ".elice-aichat__markdown")
        return element.text

    # ------------------------------------------------
    # 4. 새 대화 시작 버튼 클릭
    # ------------------------------------------------
    def new_chat(self):
        """
        사이드바의 '새 대화' 버튼을 눌러 채팅방 초기화.
        그리고 입력창이 다시 표시될 때까지 대기.
        """
        try:
            btn = self.browser.find_element(
                By.XPATH, "//a[.//span[contains(text(), '새 대화')]]"
            )
            btn.click()

            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='input']"))
            )
        except Exception as e:
            print("새 대화 버튼 클릭 실패:", e)
    # ------------------------------------------------
    # 5. 단일 질문-답변 사이클 한번에 자동 실행
    # ------------------------------------------------
    def ask(self, question): # 질문 → 답변대기 → 결과 반환까지 한 번에 처리하는 Shortcut 메서드
        
        self.send_message(question)
        self.wait_for_answer()
        return self.get_answer()
