from flask import Flask, jsonify
import os
import subprocess
import requests

app = Flask(__name__)

def get_system_info():
    return {
        "ip_address": subprocess.getoutput("hostname -I").strip(),
        "running_processes": subprocess.getoutput("ps -ax"),
        "available_disk_space": subprocess.getoutput("df -h /"),
        "uptime": subprocess.getoutput("uptime -p")
    }

@app.route('/')
def index():
    service1_info = get_system_info()

    # Call Service 2 (assumed to run on the same Docker network)
    service2_info = requests.get('http://srvc2:8199').json()

    return jsonify({
        "Service1": service1_info,
        "Service2": service2_info
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8199)
