from flask import Flask, request, jsonify
import requests
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
import os

app = Flask(__name__)

# 공공데이터 인증키 (디코딩된 것)
SERVICE_KEY = "uMQ6gI1tmbSj9PWUY6/JjEZvLtal9Ttjyj/VPn9igbGc0k3DONLCy4W+6wZ7WQJKfOAWGcDAhty/7Oo0KnnTEA=="

BASE_URL = "https://apis.data.go.kr/1471000/HtfsInfoService03/getHtfsItem01"

# TLS1.2 강제 어댑터 정의
class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        ctx = ssl.create_default_context()
        ctx.set_ciphers("DEFAULT@SECLEVEL=1")  # 보안 강도 낮춤(서버와 호환용)
        self.poolmanager = PoolManager(num_pools=connections, maxsize=maxsize, block=block, ssl_context=ctx)

@app.route("/ingredient", methods=["GET"])
def get_ingredient():
    page_no = request.args.get("pageNo", "1")
    num_of_rows = request.args.get("numOfRows", "10")
    resp_type = request.args.get("type", "json")  # json 또는 xml

    session = requests.Session()
    session.mount("https://", TLSAdapter())

    params = {
        "ServiceKey": SERVICE_KEY,
        "pageNo": page_no,
        "numOfRows": num_of_rows,
        "type": resp_type
    }

    try:
        res = session.get(BASE_URL, params=params, timeout=10)
        res.raise_for_status()

        if resp_type == "json":
            return jsonify(res.json())
        else:
            # XML인 경우 텍스트로 반환
            return res.text, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "프록시 서버가 정상 작동 중입니다."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render 등에서 자동 할당하는 포트 사용
    app.run(host="0.0.0.0", port=port, debug=True)
