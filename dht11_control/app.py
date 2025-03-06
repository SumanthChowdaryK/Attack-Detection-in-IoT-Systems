from flask import Flask, render_template, jsonify, request, make_response, send_file
import adafruit_dht
import board
import time
import threading
from threading import Thread
import RPi.GPIO as GPIO
import subprocess
import os
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder
from flask_cors import CORS

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
BUZZER_PIN = 21
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.output(BUZZER_PIN, GPIO.LOW)

# Initialize DHT11 sensor on GPIO 26
sensor = adafruit_dht.DHT11(board.D26)

# Flask app setup
app = Flask(__name__)
CORS(app)

# Initialize global variables
temperature_history = []
humidity_history = []
THRESHOLD_TEMP = 30  # Default threshold in Celsius
threshold = THRESHOLD_TEMP  # Use this variable for checking the threshold

# Load the XGBoost model and label encoder
xgb_model = joblib.load('/home/pi/dht11_control/xgb_model.pkl')
label_encoder = np.load('/home/pi/dht11_control/label_classes.npy', allow_pickle=True)

# Preprocess function
def preprocess_data(file_path):
    column_names = [
        'ts', 'uid', 'id.orig_h', 'id.orig_p', 'id.resp_h', 'id.resp_p', 'proto',
        'service', 'duration', 'orig_bytes', 'resp_bytes', 'conn_state', 'local_orig',
        'local_resp', 'missed_bytes', 'history', 'orig_pkts', 'orig_ip_bytes',
        'resp_pkts', 'resp_ip_bytes', 'tunnel_parents', 'ip_proto'
    ]
    df = pd.read_table(file_path, skiprows=10, names=column_names, low_memory=False)
    df.drop(df.tail(1).index, inplace=True)
    original_data = df.copy()
    # Preprocess numerical and categorical features
    numerical_features = ['duration', 'orig_bytes', 'resp_bytes', 'missed_bytes', 'orig_pkts', 'resp_pkts']
    for feature in numerical_features:
        df[feature] = pd.to_numeric(df[feature], errors='coerce').fillna(0)
        df[feature] = (df[feature] - df[feature].mean()) / (df[feature].std() + 1e-10)
    
    df = pd.get_dummies(df, columns=['proto', 'conn_state', 'service'], drop_first=False)
    training_features = ['duration', 'orig_bytes', 'resp_bytes', 'missed_bytes', 'orig_pkts', 'resp_pkts',
                         'proto_icmp', 'proto_tcp', 'proto_udp',
                         'conn_state_OTH', 'conn_state_REJ', 'conn_state_RSTO', 'conn_state_RSTOS0',
                         'conn_state_RSTR', 'conn_state_S0', 'conn_state_S1', 'conn_state_S2',
                         'conn_state_S3', 'conn_state_SF',
                         'service_dns', 'service_http', 'service_irc', 'service_ssh']
    for col in training_features:
        if col not in df.columns:
            df[col] = 0
    return df[training_features], original_data

# Predict and block
'''
def detect_and_block(file_path):
    preprocessed_data, original_data = preprocess_data(file_path)
    predictions = xgb_model.predict(preprocessed_data)
    decoded_predictions = label_encoder.inverse_transform(predictions)
    original_data['predicted_label'] = decoded_predictions

    attackers = original_data[original_data['predicted_label'] != 'Benign']['id.orig_h'].unique()
    for ip in attackers:
        block_ip(ip)
    return attackers
'''
'''
# Predict, block, and save results
def detect_and_block(file_path):
    try:
        preprocessed_data, original_data = preprocess_data(file_path)
        predictions = xgb_model.predict(preprocessed_data)
        decoded_predictions = [label_encoder[int(pred)] for pred in predictions]

        original_data['predicted_label'] = decoded_predictions

        original_data['attacker_ip'] = original_data.apply(
            lambda row: row['id.orig_h'] if row['predicted_label'] != 'Benign' else None, axis=1
        )

        # Save the updated data to a CSV file
        output_file = '/home/pi/dht11_control/predicted_traffic_data.csv'
        original_data.to_csv(output_file, index=False)

        # Read the updated data from the CSV file
        updated_data = pd.read_csv(output_file)
        print(f"Predicted Labels: {updated_data['predicted_label'].unique()}")
        # Extract attackers' IPs from the saved file
        attackers = updated_data[updated_data['predicted_label'] != 'Benign']['attacker_ip'].unique()
        print(f"Detected Attackers: {attackers}")
        # Block the attackers
        for ip in attackers:
            block_ip(ip)

        return attackers
    except Exception as e:
        app.logger.error(f"Error in detect_and_block: {str(e)}")
        return []
'''

def detect_and_block(file_path):
    try:
        preprocessed_data, original_data = preprocess_data(file_path)
        predictions = xgb_model.predict(preprocessed_data)
        decoded_predictions = [label_encoder[int(pred)] for pred in predictions]

        original_data['predicted_label'] = decoded_predictions

        original_data['attacker_ip'] = original_data.apply(
            lambda row: row['id.orig_h'] if row['predicted_label'] != 'Benign' else None, axis=1
        )

        # Save the updated data to a CSV file
        output_file = '/home/pi/dht11_control/predicted_traffic_data.csv'
        original_data.to_csv(output_file, index=False)

        # Read the updated data from the CSV file
        updated_data = pd.read_csv(output_file)
        print(f"Predicted Labels: {updated_data['predicted_label'].unique()}")
        
        # Block attackers
        attackers = updated_data[updated_data['predicted_label'] != 'Benign']['attacker_ip'].unique()
        print(f"Detected Attackers: {attackers}")
        for ip in attackers:
            block_ip(ip)

        return updated_data  # Return the entire dataframe

    except Exception as e:
        app.logger.error(f"Error in detect_and_block: {str(e)}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

    
# Block IP function
def block_ip(ip):
    subprocess.run(['sudo', 'iptables', '-A', 'INPUT', '-s', ip, '-j', 'DROP'])

# Read DHT11 sensor
def read_dht11():
    try:
        humidity = sensor.humidity
        temperature = sensor.temperature
        if humidity is not None and temperature is not None:
            return {"temperature": temperature, "humidity": humidity}
        else:
            return {"temperature": None, "humidity": None}
    except RuntimeError:
        return {"temperature": None, "humidity": None}

# Function to check threshold and control buzzer
def check_and_buzz(temp):
    if temp > threshold:
        GPIO.output(BUZZER_PIN, GPIO.HIGH)  # Turn on the buzzer
    else:
        GPIO.output(BUZZER_PIN, GPIO.LOW)   # Turn off the buzzer

# API route to set the threshold
@app.route('/api/set_threshold', methods=['POST'])
def set_threshold():
    global threshold
    data = request.get_json()
    if 'threshold' in data:
        threshold = float(data['threshold'])
        return jsonify({"status": "success", "threshold": threshold})
    return jsonify({"status": "failure"})
'''
# Flask endpoint for attack detection
@app.route('/api/detect_attacks', methods=['POST'])
def detect_attacks():
    try:
        traffic_file = '/home/pi/dht11_control/live_traffic_conn.log'
        attackers = detect_and_block(traffic_file)

        # Prepare attacker details for frontend
        attackers_details = [{"attacker_ip": ip} for ip in attackers]
        return jsonify({"attackers": attackers_details}), 200
    except Exception as e:
        app.logger.error(f"Error: {str(e)}")  # Log error details
        return jsonify({'error': 'Internal Server Error'}), 500
'''
# Background thread to collect data periodically
def collect_data():
    while True:
        data = read_dht11()
        if data["temperature"] is not None:
            temperature_history.append(data["temperature"])
            humidity_history.append(data["humidity"])
            check_and_buzz(data["temperature"])  # Check threshold and buzz
        if len(temperature_history) > 10:
            temperature_history.pop(0)
            humidity_history.pop(0)
        time.sleep(5)

# Start background data collection thread
threading.Thread(target=collect_data, daemon=True).start()

# Home route
@app.route('/')
def index():
    data = read_dht11()
    response = make_response(render_template("index.html", data=data, threshold=threshold))
    response.headers["Content-Type"] = "text/html; charset=utf-8"
    return response

# Flask endpoint for download attack detection
@app.route('/download_csv', methods=['GET'])
def download_csv():
    data_file = '/home/pi/dht11_control/live_traffic_conn.log'
    updated_data = detect_and_block(data_file)

    try:
        traffic_file = '/home/pi/dht11_control/predicted_traffic_data.csv'
        if os.path.exists(traffic_file):
            return send_file(traffic_file, as_attachment=True)
        else:
            return jsonify({"status": "failure", "error": "CSV file not found."})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"status": "failure", "error": str(e)})
'''@app.route('/api/detect_attacks', methods=['POST'])
def detect_attacks():
    try:
        traffic_file = '/home/pi/dht11_control/live_traffic_conn.log'
        attackers = detect_and_block(traffic_file)

        # Log the attackers list to ensure it's populated
        print(f"Attackers detected: {attackers}")

        return jsonify({"status": "success", "attackers": list(attackers)})
    except Exception as e:
        print(f"Error in Flask route: {str(e)}")
        return jsonify({"status": "failure", "error": str(e)})
'''
'''
@app.route('/api/detect_attacks', methods=['POST'])
def detect_attacks():
    try:
        traffic_file = '/home/pi/dht11_control/predicted_traffic_data.csv'
        
        # Check if the file exists
        if not os.path.exists(traffic_file):
            return jsonify({"status": "failure", "error": "CSV file not found."})
        
        # Read the CSV file using pandas
        updated_data = pd.read_csv(traffic_file)

        if updated_data.empty:
            return jsonify({"status": "failure", "error": "CSV is empty."})

        # Generate an HTML table from the CSV data
        html_table = updated_data.to_html(classes="table table-bordered table-striped", index=False)

        return jsonify({"status": "success", "html_table": html_table})

    except Exception as e:
        print(f"Error in Flask route: {str(e)}")
        return jsonify({"status": "failure", "error": str(e)})
'''
'''@app.route('/api/detect_attacks', methods=['POST'])
def detect_attacks():
    try:
        traffic_file = '/home/pi/dht11_control/live_traffic_conn.log'
        updated_data = detect_and_block(traffic_file)

        # Read the updated data from the CSV file
        updated_data = pd.read_csv('/home/pi/dht11_control/predicted_traffic_data.csv')

        # Debugging: Print the data to ensure it's being read correctly
        print("Data read from CSV:")
        print(updated_data.head())

        # Check if data is populated
        if updated_data.empty:
            return jsonify({"status": "failure", "error": "No data in the CSV file."})

        # Convert the dataframe to JSON format for frontend
        data_json = updated_data.to_dict(orient='records')

        return jsonify({"status": "success", "data": data_json})

    except Exception as e:
        print(f"Error in Flask route: {str(e)}")
        return jsonify({"status": "failure", "error": str(e)})'''

'''@app.route('/api/detect_attacks', methods=['POST'])
def detect_attacks():
    try:
        # Mock response for testing
        mock_data = [
            {"id.orig_h": "192.168.1.1", "id.resp_h": "192.168.1.2", "predicted_label": "Malicious"},
            {"id.orig_h": "192.168.1.3", "id.resp_h": "192.168.1.4", "predicted_label": "Benign"}
        ]
        
        return jsonify({"status": "success", "data": mock_data})

    except Exception as e:
        print(f"Error in Flask route: {str(e)}")
        return jsonify({"status": "failure", "error": str(e)})'''

# API route for JSON data
@app.route('/api/data')
def api_data():
    data = read_dht11()
    return jsonify(data)

# API route to turn off the buzzer
@app.route('/api/turn_off_buzzer', methods=['POST'])
def turn_off_buzzer():
    global buzzer_state
    GPIO.output(BUZZER_PIN, GPIO.LOW)  # Turn off the buzzer
    buzzer_state = False  # Keep the buzzer off
    return jsonify({"status": "success"})

# API route for historical data
@app.route('/api/historical')
def historical_data():
    return jsonify({
        "temperature": temperature_history,
        "humidity": humidity_history
    })

# Clean up GPIO on exit
@app.before_request
def cleanup_gpio():
    GPIO.output(BUZZER_PIN, GPIO.LOW)

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=8081)
    except KeyboardInterrupt:
        GPIO.cleanup()  # Reset GPIO settings on exit
