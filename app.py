from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# 인증키 (Encoding 상태) — 공공데이터포털에서 복사한 그대로 넣기
SERVICE_KEY = "uMQ6g1tmbSj9PWUY6%2FJjEZvLtal9Ttjyj%2FVPn9igbGc0k3DONLCy4W%2B6wZ7WQJKfOAWGcDAhty%2F7Oo0KnnTEA%3D%3D"

BASE_URL = "https://apis.data.go.kr/1471000/HtfsInfoService03/getHtfsItem01"

@app.route("/ingredient", methods=["GET"])
def get_ingredient():
    # 페이지 번호와 한 페이지 항목 수 쿼리 (기본값 설정)
    pageNo = request.args.get("pageNo", "1")
    numOfRows = request.args.get("numOfRows", "10")

    params = {
        "ServiceKey": SERVICE_KEY,
        "pageNo": pageNo,
        "numOfRows": numOfRows,
        "type": "json"  # JSON 응답으로 요청
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return jsonify(data), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "프록시 서버 정상 작동 중입니다."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
