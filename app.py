from flask import Flask, request, jsonify
import requests
import os
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

app = Flask(__name__)

# 공공데이터 포털에서 받은 인증키 (디코딩된 상태)
SERVICE_KEY = "uMQ6gI1tmbSj9PWUY6/JjEZvLtal9Ttjyj/VPn9igbGc0k3DONLCy4W+6wZ7WQJKfOAWGcDAhty/7Oo0KnnTEA=="

# API 주소
SOAP_URL = "https://apis.data.go.kr/1471000/HtfsTrgetInfoService01/getHtfsTrgetInfoList01"

# TLS1.2 강제 어댑터 (SSL 오류 대비)
class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.set_ciphers("DEFAULT@SECLEVEL=1")  # 보안 레벨 낮춤
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

@app.route("/ingredient", methods=["GET"])
def get_ingredient():
    # 쿼리 파라미터 (필요시 사용 가능)
    keyword = request.args.get("keyword", "")

    soap_body = f"""<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ser="http://service.openapi.go.kr">
   <soapenv:Header/>
   <soapenv:Body>
      <ser:getHtfsTrgetInfoList01>
         <serviceKey>{SERVICE_KEY}</serviceKey>
         <pageNo>1</pageNo>
         <numOfRows>100</numOfRows>
         <type>xml</type>
      </ser:getHtfsTrgetInfoList01>
   </soapenv:Body>
</soapenv:Envelope>"""

    headers = {
        "Content-Type": "text/xml;charset=UTF-8"
    }

    session = requests.Session()
    session.mount('https://', TLSAdapter())

    try:
        response = session.post(SOAP_URL, data=soap_body, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "프록시 서버가 정상 작동 중입니다."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
