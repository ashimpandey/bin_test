from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST", "DELETE", "PUT"])
def proxy():
    try:
        method = request.method
        target_path = request.args.get("url")
        if not target_path:
            return Response("Missing 'url' param", status=400)

        # Determine Binance base URL
        if target_path.startswith("/fapi"):
            base_url = "https://fapi.binance.com"
        elif target_path.startswith("/papi"):
            base_url = "https://papi.binance.com"
        elif target_path.startswith("/api"):
            base_url = "https://api.binance.com"
        elif target_path.startswith("/sapi"):
            base_url = "https://api.binance.com"  # sapi is under main API domain
        elif target_path.startswith("/dapi"):
            base_url = "https://dapi.binance.com"
        else:
            return Response(f"Unsupported path: {target_path}", status=400)

        # Compose full URL
        full_url = f"{base_url}{target_path}"

        # Preserve raw query string (important for HMAC)
        query_string = request.query_string.decode()
        if "url=" in query_string:
            query_string = "&".join(q for q in query_string.split("&") if not q.startswith("url="))
        if query_string:
            full_url = f"{full_url}?{query_string}"

        headers = {k: v for k, v in request.headers if k.lower() != 'host'}
        data = request.get_data()

        # Send request to Binance
        response = requests.request(method, full_url, headers=headers, data=data)

        return Response(response.content, status=response.status_code, content_type=response.headers.get('Content-Type'))

    except Exception as e:
        return Response(f"Error: {str(e)}", status=500)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
