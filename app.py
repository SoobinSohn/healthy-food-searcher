from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 당신의 공공데이터 인증키 (디코딩된 것)
SERVICE_KEY = "uMQ6gI1tmbSj9PWUY6/JjEZvLtal9Ttjyj/VPn9igbGc0k3DONLCy4W+6wZ7WQJKfOAWGcDAhty/7Oo0KnnTEA=="

SOAP_URL = "https://apis.data.go.kr/1471000/HtfsTrgetInfoService01/getHtfsTrgetInfoList01"

# 실제 API 호출을 담당할 엔드포인트
@app.route("/ingredient", methods=["GET"])
def get_ingredient():
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

    try:
        res = requests.post(SOAP_URL, data=soap_body, headers=headers, timeout=10)
        res.raise_for_status()

        # 결과는 XML이므로 일단 텍스트로 반환
        return res.text, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Render 서버용 기본 루트
@app.route("/")
def home():
    return "프록시 서버가 정상 작동 중입니다."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)

