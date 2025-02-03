from flask import Flask, request, jsonify
from storage import SimpleBattery  # Importing the class from storage.py

app = Flask(__name__)

# Global variable to hold the battery instance
battery = None


@app.route('/initialize', methods=['POST'])
def initialize():
    """Initialize or reset the battery with new parameters."""
    global battery
    data = request.get_json()

    try:
        battery = SimpleBattery(
            capacity=data["capacity"],
            initial_soc=data["initial_soc"],
            min_soc=data.get("min_soc", 0.0),
            c_rate=data.get("c_rate", None)
        )
        return jsonify({"message": "Battery initialized successfully"})
    except (KeyError, ValueError, AssertionError) as e:
        return jsonify({"error": str(e)}), 400


@app.route('/update', methods=['POST'])
def update():
    """Update battery charge/discharge via API."""
    global battery
    if battery is None:
        return jsonify({"error": "Battery not initialized"}), 400

    data = request.get_json()
    power = data.get("power")
    duration = data.get("duration")

    if power is None or duration is None:
        return jsonify({"error": "Missing power or duration"}), 400

    try:
        energy_transferred = battery.update(power, duration)
        return jsonify({"energy_transferred": energy_transferred, "soc": battery.soc()})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route('/soc', methods=['GET'])
def get_soc():
    """Get battery state-of-charge."""
    global battery
    if battery is None:
        return jsonify({"error": "Battery not initialized"}), 400
    return jsonify({"soc": battery.soc()})


@app.route('/state', methods=['GET'])
def get_state():
    """Get battery details."""
    global battery
    if battery is None:
        return jsonify({"error": "Battery not initialized"}), 400
    return jsonify(battery.state())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
