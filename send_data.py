from flask import Flask, request, jsonify # use FlASK to create a web server
import serial # to import pyserial for USB communication
import time
import json

app = Flask(__name__)  # Create a Flask web server

arduino = serial.Serial('COM3', 9600, timeout=1)  
time.sleep(2)  # give time for connection

@app.route('/sendData', methods=['POST'])

# create a function that receives data from the web server
def receive_data():
    schedule_data = request.get_json() # gets data from the web server
    print("Received Schedule:", schedule_data)

    for entry in schedule_data:
        formatted_entry = f"{entry['compartment']},{entry['date']},{entry['time']},{entry['medication']}, {entry['effects']}\n"
        arduino.write(formatted_entry.encode()) # send to ardunio
        time.sleep(0.5)  # give time to send so buffer doesn't blow up

    return jsonify({"status": "Data sent to Arduino"})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
