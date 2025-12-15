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

    def send_message(self, message):
        textarea = self.browser.find_element(By.CSS_SELECTOR, "textarea[name='input']")

        for line in message.split("\n"):
            textarea.send_keys(line)
            textarea.send_keys(Keys.SHIFT, Keys.ENTER)

        # 마지막에만 Enter → 전송
        textarea.send_keys(Keys.ENTER)

    # ------------------------------------------------
    # 2. 모든 답변 요소 가져오기
    # ------------------------------------------------

    def get_all_answers(self):
        return self.browser.find_elements(
            By.CSS_SELECTOR, ".elice-aichat__markdown"
        )
    
    # ------------------------------------------------
    # 3. 답변 대기 
    # ------------------------------------------------

    def wait_for_answer(
        self,prev_answer_count,
        spinner_selector="svg.MuiCircularProgress-svg",
        answer_selector=".elice-aichat__markdown",
        min_wait_time=10.0,
        stable_duration=1.0
    ):
        start_time = time.time()

        # 1️⃣ 최소 대기시간 동안은 무조건 기다림
        while time.time() - start_time < min_wait_time:
            time.sleep(0.2)


        print("⏳ 최소 대기 시간 경과")

        # 2️⃣ 스피너가 있다면 사라질 때까지
        try:
            WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, spinner_selector))
            )
            WebDriverWait(self.browser, 300).until_not(
                EC.presence_of_element_located((By.CSS_SELECTOR, spinner_selector))
            )
        except Exception:
            print("ℹ️ 스피너 감지되지 않음 (즉시 답변 가능)")

        print("⏳ 스피너 대기 종료")

        # 3️⃣ 새 답변이 추가될 때까지 대기
        WebDriverWait(self.browser, 300).until(
            lambda d: len(d.find_elements(By.CSS_SELECTOR, answer_selector))
            > prev_answer_count
        )

        print("⏳ 새 답변 감지")

        # 4️⃣ 마지막 답변 텍스트 안정화
        last_answer = self.get_all_answers()[-1] #역순으로 넣어 답변 누적

        prev_text = ""
        stable_start = None

        while True:
            current_text = last_answer.text.strip() 

            if not current_text:
                prev_text = ""
                stable_start = None
                time.sleep(0.3)
                continue

            if current_text != prev_text:
                prev_text = current_text
                stable_start = time.time()
            else:
                if stable_start and time.time() - stable_start >= stable_duration:
                    break

            time.sleep(0.3)

        print("✅ 답변 안정화 완료")


    # ------------------------------------------------
    # 4. 마지막 답변 가져오기
    # ------------------------------------------------
    def get_last_answer(self):
        return self.get_all_answers()[-1].text

    # ------------------------------------------------
    # 5. 새 대화 시작 버튼 클릭
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


    