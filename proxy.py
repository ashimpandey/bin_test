from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST", "DELETE"])
def proxy():
    method = request.method
    target_url = request.args.get("url")
    headers = {k: v for k, v in request.headers if k.lower() != 'host'}
    data = request.get_data()
    params = dict(request.args)

    if not target_url:
        return jsonify({"error": "Missing 'url' param"}), 400

    binance_url = f"https://fapi.binance.com{target_url}"
    try:
        response = requests.request(method, binance_url, headers=headers, data=data, params=params)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # ✅ Render requires this
    app.run(host="0.0.0.0", port=port)
