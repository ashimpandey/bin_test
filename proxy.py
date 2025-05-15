from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST", "DELETE"])
def proxy():
    method = request.method
    target_url = request.args.get("url")
    headers = {k: v for k, v in request.headers if k != 'Host'}
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
    app.run()
