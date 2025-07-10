from flask import Flask, request, jsonify
import requests
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
import os

app = Flask(__name__)

# 공공데이터 인증키
SERVICE_KEY = "uMQ6gI1tmbSj9PWUY6/JjEZvLtal9Ttjyj/VPn9igbGc0k3DONLCy4W+6wZ7WQJKfOAWGcDAhty/7Oo0KnnTEA=="
SOAP_URL = "https://apis.data.go.kr/1471000/HtfsTrgetInfoService01/getHtfsTrgetInfoList01"

# ✅ TLS 호환성용 어댑터 정의
class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')  # 낮은 보안 수준 허용 (공공데이터포털 대응용)
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

# 🚀 SOAP 호출용 엔드포인트
@app.route("/ingredient", methods=["GET"])
def get_ingredient():
    keyword = request.args.get("keyword", "")  # 아직 필터에는 사용 안함

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

    # TLS 호환 세션 구성
    session = requests.Session()
    session.mount("https://", TLSAdapter())

    try:
        res = session.post(SOAP_URL, data=soap_body, headers=headers, timeout=10)
        res.raise_for_status()
        return res.text, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 기본 라우트
@app.route("/")
def home():
    return "프록시 서버가 정상 작동 중입니다."

# Render에서 포트 환경변수 사용
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
