from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Map service names to their container endpoints
SERVICES = {
    "powerplant": "http://powerplant-service:5000",
    "battery": "http://battery-service:5000"
}


@app.route('/<service>/<path:endpoint>', methods=['GET', 'POST'])
def proxy(service, endpoint):
    """Forward API calls to the correct service."""
    if service not in SERVICES:
        return jsonify({"error": "Service not found"}), 404

    url = f"{SERVICES[service]}/{endpoint}"

    try:
        if request.method == 'POST':
            response = requests.post(url, json=request.get_json())
        else:
            response = requests.get(url, params=request.args)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"error": f"Could not reach {service} service"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
