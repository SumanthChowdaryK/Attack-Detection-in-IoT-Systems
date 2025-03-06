import requests

# Raspberry Pi configuration
raspberry_ip = "http://192.168.120.110"  # Replace with the Raspberry Pi's IP
port_dht11 = 8081
port_led = 8002

# List of endpoints
endpoints = {
    "dht11_data": f"{raspberry_ip}:{port_dht11}/api/data",
    "turn_off_buzzer": f"{raspberry_ip}:{port_dht11}/api/turn_off_buzzer",
    "historical_data": f"{raspberry_ip}:{port_dht11}/api/historical",
    "set_threshold": f"{raspberry_ip}:{port_dht11}/api/set_threshold",
    "led_on": f"{raspberry_ip}:{port_led}/led/on",
    "led_off": f"{raspberry_ip}:{port_led}/led/off"
}

# Function to retrieve DHT11 data
def get_dht11_data():
    try:
        response = requests.get(endpoints["dht11_data"])
        if response.status_code == 200:
            data = response.json()
            print("DHT11 Data Retrieved:")
            print(f"Temperature: {data['temperature']}°C")
            print(f"Humidity: {data['humidity']}%")
        else:
            print("Failed to retrieve DHT11 data.")
    except Exception as e:
        print(f"Error: {e}")

# Function to control the LED
def control_led(state):
    try:
        if state.lower() == "on":
            response = requests.get(endpoints["led_on"])
        elif state.lower() == "off":
            response = requests.get(endpoints["led_off"])
        else:
            print("Invalid LED state. Use 'on' or 'off'.")
            return

        if response.status_code == 200:
            print(f"LED turned {state.upper()} successfully.")
        else:
            print(f"Failed to turn {state.upper()} the LED.")
    except Exception as e:
        print(f"Error: {e}")

# Function to set the threshold temperature
def set_threshold_temperature(threshold):
    try:
        data = {"threshold": threshold}
        response = requests.post(endpoints["set_threshold"], json=data)
        if response.status_code == 200:
            print(f"Threshold set to {threshold}°C successfully.")
        else:
            print("Failed to set threshold.")
    except Exception as e:
        print(f"Error: {e}")

# Menu for interacting with the Raspberry Pi
def main():
    while True:
        print("\n--- IoT Control Menu ---")
        print("1. Retrieve DHT11 Data")
        print("2. Control LED (On/Off)")
        print("3. Set Threshold Temperature")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            get_dht11_data()
        elif choice == "2":
            state = input("Enter LED state (on/off): ").strip()
            control_led(state)
        elif choice == "3":
            try:
                threshold = float(input("Enter threshold temperature (°C): ").strip())
                set_threshold_temperature(threshold)
            except ValueError:
                print("Invalid input. Please enter a numeric value.")
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
