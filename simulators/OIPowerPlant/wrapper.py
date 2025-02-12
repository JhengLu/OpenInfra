from flask import Flask, request, jsonify
import pandas as pd
from powerplant import PowerGenerator  # Import the class

app = Flask(__name__)

# Global variable to hold the PowerGenerator instance
power_generator = None


@app.route('/initialize', methods=['POST'])
def initialize():
    """Initialize the power generator with a given location and time zone."""
    global power_generator
    data = request.get_json()

    try:
        location = data.get("location", "cal")  # Default to "cal"
        time_zone = data.get("time_zone", "pacific-time")  # Default to "pacific-time"

        # Initialize power generator
        power_generator = PowerGenerator(location, time_zone)

        return jsonify({"message": "Power generator initialized successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/generate_power', methods=['GET'])
def generate_power():
    """Retrieve power generation for a given time step."""
    global power_generator
    if power_generator is None:
        return jsonify({"error": "Power generator not initialized"}), 400

    time_step = request.args.get("time_step", type=int)

    if time_step is None:
        return jsonify({"error": "Missing time_step parameter"}), 400

    try:
        total_power, wind_power, solar_power = power_generator.generate_power(time_step)
        return jsonify({
            "total_power_watts": total_power,
            "wind_power_watts": wind_power,
            "solar_power_watts": solar_power
        })
    except KeyError:
        return jsonify({"error": "Invalid time_step"}), 400


@app.route('/get_processed_trace', methods=['GET'])
def get_processed_trace():
    """Return the processed power trace as JSON."""
    global power_generator
    if power_generator is None:
        return jsonify({"error": "Power generator not initialized"}), 400

    return jsonify(power_generator.power_projected_trace_df.to_dict(orient="records"))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
