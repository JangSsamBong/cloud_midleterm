# Flask API를 완성하세요.
# 요구사항:
# - 데이터 파일 경로: /app/data/expenses.json  (초기 내용: [])
# - GET  /api/records   : 저장된 데이터를 JSON으로 반환
# - POST /api/records   : {title, amount, date} 저장 (유효성 검사 포함)
# - GET  /api/summary   : {count, total} 반환
# - GET  /api/download  : expenses.json 파일 다운로드

from flask import Flask, request, jsonify, send_file
from pathlib import Path
import json, os

app = Flask(__name__)

DATA_PATH = Path("/app/data/expenses.json")
DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
if not DATA_PATH.exists():
    DATA_PATH.write_text("[]", encoding="utf-8")

def load_data():
    with DATA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)
    
def save_data(data):
    with DATA_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
@app.get("/healthz")
def healthz():
    return "ok", 200

# 아래 엔드포인트들을 구현하세요. ( 함수명은 임의로 지정한 내용임 )
@app.get("/api/records")
def get_records():
    data = load_data()
    return jsonify(data)

@app.post("/api/records")
def add_record():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    req = request.get_json()

    title = req.get("title")
    amount = req.get("amount")
    date = req.get("date")

    # 유효성 검사
    if not title or not isinstance(title, str) or title.strip() == "":
        return jsonify({"error": "title is required and must be a non-empty string"}), 400
    try:
        amount = int(amount)
        if amount < 0:
            raise ValueError
    except:
        return jsonify({"error": "amount must be a non-negative integer"}), 400
    if not date or not isinstance(date, str) or date.strip() == "":
        return jsonify({"error": "date is required and must be a non-empty string"}), 400
    # (날짜 형식 검사 추가 가능)

    data = load_data()
    data.append({"title": title.strip(), "amount": amount, "date": date.strip()})
    save_data(data)

    return jsonify({"message": "record saved successfully"}), 201

@app.get("/api/summary")
def summary():
    data = load_data()
    count = len(data)
    total = sum(item.get("amount", 0) for item in data)
    return jsonify({"count": count, "total": total})

@app.get("/api/download")
def download_json():
    return send_file(str(DATA_PATH), as_attachment=True, download_name="expenses.json")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)