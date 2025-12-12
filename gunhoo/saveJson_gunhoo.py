import json

def save_json(filename, data):
    """
    JSON 데이터를 지정한 이름으로 저장하는 공용 유틸 함수.
    indent=4 로 알맞게 저장.
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"JSON 저장 완료 → {filename}")