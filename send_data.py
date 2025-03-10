from flask import Flask, request, jsonify
import serial
import time
import json

app = Flask(__name__)

# Replace with the correct COM port for Arduino
# Windows: 'COM3', 'COM4', etc.
# Mac/Linux: '/dev/ttyUSB0', '/dev/ttyACM0'
arduino = serial.Serial('COM3', 9600, timeout=1)  
time.sleep(2)  # Allow time for connection

@app.route('/sendData', methods=['POST'])
def receive_data():
    schedule_data = request.get_json()
    print("Received Schedule:", schedule_data)

    for entry in schedule_data:
        formatted_entry = f"{entry['compartment']},{entry['date']},{entry['time']},{entry['medication']}\n"
        arduino.write(formatted_entry.encode())
        time.sleep(0.5)  # Avoid buffer overflow

    return jsonify({"status": "Data sent to Arduino"})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
