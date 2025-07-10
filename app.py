from flask import Flask, request, jsonify
import requests
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
import os

app = Flask(__name__)

# 공공데이터포털에서 발급받은 디코딩된 인증키 입력
SERVICE_KEY = "uMQ6gI1tmbSj9PWUY6/JjEZvLtal9Ttjyj/VPn9igbGc0k3DONLCy4W+6wZ7WQJKfOAWGcDAhty/7Oo0KnnTEA=="

# 공공데이터포털 SOAP API 엔드포인트
SOAP_URL = "https://apis.data.go.kr/1471000/HtfsTrgetInfoService01/getHtfsTrgetInfoList01"

# TLS1.2 강제 어댑터 (SSL 문제 우회용)
class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')  # 보안 레벨 낮춤
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

@app.route("/ingredient", methods=["GET"])
def get_ingredient():
    keyword = request.args.get("keyword", "")  # 현재 필터 미적용, 추후 개발 가능

    soap_body = f"""<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
   <soapenv:Header/>
   <soapenv:Body>
      <getHtfsTrgetInfoList01 xmlns="http://service.openapi.go.kr">
         <serviceKey>{SERVICE_KEY}</serviceKey>
         <pageNo>1</pageNo>
         <numOfRows>10</numOfRows>
      </getHtfsTrgetInfoList01>
   </soapenv:Body>
</soapenv:Envelope>"""

    headers = {
        "Content-Type": "text/xml;charset=UTF-8"
    }

    session = requests.Session()
    session.mount("https://", TLSAdapter())

    try:
        res = session.post(SOAP_URL, data=soap_body, headers=headers, timeout=10)
        res.raise_for_status()
        return res.text, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "프록시 서버가 정상 작동 중입니다."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render 환경변수 포트 사용
    app.run(host="0.0.0.0", port=port, debug=True)
