from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST", "DELETE"])
def proxy():
    try:
        method = request.method
        target_url = request.args.get("url")
        if not target_url:
            return jsonify({"error": "Missing 'url' param"}), 400

        # Prepare actual request to Binance
        binance_url = f"https://fapi.binance.com{target_url}"
        headers = {k: v for k, v in request.headers if k.lower() != 'host'}
        data = request.get_data()
        params = dict(request.args)
        params.pop("url", None)  # Don't forward 'url' param to Binance

        # Forward request
        response = requests.request(method, binance_url, headers=headers, data=data, params=params)

        # Try parsing as JSON
        try:
            return jsonify(response.json()), response.status_code
        except ValueError:
            return jsonify({"error": "Non-JSON response from Binance", "content": response.text}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
