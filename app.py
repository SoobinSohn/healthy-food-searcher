from flask import Flask, request, jsonify
import requests
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
import os

app = Flask(__name__)  # ⭐️ 반드시 제일 위에 있어야 함

# 이하 기존 코드 계속...

# 예시 라우터
@app.route("/ingredient", methods=["GET"])
def get_ingredient():
    # 코드 생략
    pass

@app.route("/")
def home():
    return "프록시 서버가 정상 작동 중입니다."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
