from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

@app.route("/<path:path>", methods=["GET", "POST", "DELETE", "PUT"])
def proxy(path):
    try:
        # Determine Binance base URL
        if path.startswith("fapi"):
            base_url = "https://fapi.binance.com"
        elif path.startswith("papi"):
            base_url = "https://papi.binance.com"
        elif path.startswith("api"):
            base_url = "https://api.binance.com"
        elif path.startswith("sapi"):
            base_url = "https://api.binance.com"
        elif path.startswith("dapi"):
            base_url = "https://dapi.binance.com"
        else:
            return Response(f"Unsupported path: {path}", status=400)

        # Compose full Binance URL
        full_url = f"{base_url}/{path}"
        if request.query_string:
            full_url += f"?{request.query_string.decode()}"

        headers = {k: v for k, v in request.headers if k.lower() != 'host'}
        data = request.get_data()

        # Forward the request
        response = requests.request(request.method, full_url, headers=headers, data=data)
        return Response(response.content, status=response.status_code, content_type=response.headers.get('Content-Type'))

    except Exception as e:
        return Response(f"Error: {str(e)}", status=500)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
