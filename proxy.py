from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST", "DELETE"])
def proxy():
    try:
        method = request.method
        target_path = request.args.get("url")
        if not target_path:
            return jsonify({"error": "Missing 'url' param"}), 400

        # Determine which Binance domain to use
        if target_path.startswith("/fapi"):
            base_url = "https://fapi.binance.com"
        elif target_path.startswith("/papi"):
            base_url = "https://papi.binance.com"
        elif target_path.startswith("/api"):
            base_url = "https://api.binance.com"
        elif target_path.startswith("/dapi"):
            base_url = "https://dapi.binance.com"
        elif target_path.startswith("/sapi"):
            base_url = "https://api.binance.com"
        elif target_path.startswith("/eapi"):
            base_url = "https://eapi.binance.com"
        else:
            return jsonify({"error": f"Unsupported path: {target_path}"}), 400

        # Compose full URL
        full_url = f"{base_url}{target_path}"

        # Extract headers and query params
        headers = {k: v for k, v in request.headers if k.lower() != 'host'}
        data = request.get_data()
        params = dict(request.args)
        params.pop("url", None)  # Don't forward 'url' param to Binance

        # Forward the request
        response = requests.request(method, full_url, headers=headers, data=data, params=params)

        # Try to return JSON response
        try:
            return jsonify(response.json()), response.status_code
        except ValueError:
            return jsonify({"error": "Non-JSON response from Binance", "content": response.text}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
