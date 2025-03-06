import requests
import time
import threading
import random

# Raspberry Pi configuration
raspberry_ip = "http://192.168.120.110"  # Replace with the Raspberry Pi's IP
port_dht11 = 8081
port_led = 8002

# List of endpoints for different actions
led_on_endpoint = f"{raspberry_ip}:{port_led}/led/on"
led_off_endpoint = f"{raspberry_ip}:{port_led}/led/off"
dht11_data_endpoint = f"{raspberry_ip}:{port_dht11}/api/data"
set_threshold_endpoint = f"{raspberry_ip}:{port_dht11}/api/set_threshold"

# Function to send a request to toggle the LED
def toggle_led(state):
    endpoint = led_on_endpoint if state == "on" else led_off_endpoint
    try:
        response = requests.get(endpoint, timeout=5)
        if response.status_code == 200:
            print(f"LED {state.upper()} request successful")
        else:
            print(f"LED {state.upper()} request failed with status {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error toggling LED {state.upper()}: {e}")

# Function to fetch temperature and humidity data
def fetch_temperature_and_humidity():
    for _ in range(3):  # Retry up to 3 times
        try:
            response = requests.get(f"{raspberry_ip}:{port_dht11}/api/data", timeout=10)
            response.raise_for_status()
            data = response.json()
            print(f"Fetched data: {data}")
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching temperature and humidity: {e}")
            time.sleep(2)  # Wait before retrying
    print("Failed to fetch data after 3 attempts.")
    return None


# Function to dynamically set the threshold
def set_dynamic_threshold():
    threshold = random.randint(1, 30)
    try:
        response = requests.post(set_threshold_endpoint, json={"threshold": threshold}, timeout=5)
        if response.status_code == 200:
            print(f"Threshold set to {threshold}°C successfully")
        else:
            print(f"Failed to set threshold with status {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error setting threshold: {e}")

# Function to perform a dynamic action loop
def dynamic_action_loop():
    while True:
        # Toggle LED ON
        toggle_led("on")
        time.sleep(1)  # Wait for 1 second

        # Fetch temperature and humidity
        fetch_temperature_and_humidity()
        time.sleep(1)

        # Toggle LED OFF
        toggle_led("off")
        time.sleep(1)

        # Set a dynamic threshold
        set_dynamic_threshold()
        time.sleep(1)

if __name__ == "__main__":
    print("Starting dynamic IoT interaction on Raspberry Pi...")
    try:
        dynamic_action_loop()
    except KeyboardInterrupt:
        print("Program interrupted by user.")
