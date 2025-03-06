import RPi.GPIO as GPIO
from flask import Flask, render_template, request, redirect, url_for

# Set up Raspberry Pi GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Pin for the LED
LED_PIN = 17
GPIO.setup(LED_PIN, GPIO.OUT)

# Flask app setup
app = Flask(__name__)

# Route for the home page
@app.route('/')
def index():
    # Read the current state of the LED
    led_state = GPIO.input(LED_PIN)
    return render_template('index.html', led_state=led_state)

# Route for turning the LED on
@app.route('/led/on')
def led_on():
    GPIO.output(LED_PIN, GPIO.HIGH)  # Turn the LED on
    return redirect(url_for('index'))

# Route for turning the LED off
@app.route('/led/off')
def led_off():
    GPIO.output(LED_PIN, GPIO.LOW)  # Turn the LED off
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8002)
