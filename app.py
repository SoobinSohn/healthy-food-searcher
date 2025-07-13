@app.route("/ingredient", methods=["GET"])
def get_ingredient():
    page_no = request.args.get("pageNo", "1")
    num_of_rows = request.args.get("numOfRows", "10")
    resp_type = request.args.get("type", "json")  # json 또는 xml

    # 👉추가: 제품명/업체명 파라미터도 받기
    prduct = request.args.get("PRDUCT")
    entrps = request.args.get("ENTRPS")

    session = requests.Session()
    session.mount("https://", TLSAdapter())

    params = {
        "ServiceKey": SERVICE_KEY,
        "pageNo": page_no,
        "numOfRows": num_of_rows,
        "type": resp_type
    }
    if prduct:
        params["PRDUCT"] = prduct
    if entrps:
        params["ENTRPS"] = entrps

    try:
        res = session.get(BASE_URL, params=params, timeout=10)
        res.raise_for_status()
        if resp_type == "json":
            return jsonify(res.json())
        else:
            return res.text, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
