from flask import Flask, jsonify, request
import os
import subprocess
import requests
import time
import sys
import docker
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/stop-instances', methods=['POST'])
def stop_instances():
    try:
        client = docker.from_env()
        # Get all running containers
        containers = client.containers.list()
        # Stop and remove all containers
        for container in containers:
            print(f"Stopping container: {container.name}")
            container.stop()
            print(f"Removing container: {container.name}")
            container.remove()
        
        return jsonify({"status": "All containers stopped and removed"}), 200
    except Exception as e:
        # Log exception details
        print(f"Exception occurred: {e}")
        import traceback
        traceback.print_exc()  # Logs the stack trace
        return jsonify({"status": "An error occurred", "error": str(e)}), 500

@app.route('/stop', methods=['POST'])
def stop():
    try:
        # Call the shell script to stop Docker services
        subprocess.run(["bash", "docker-stop.sh"], check=True)
        return jsonify({"status": "Services stopped successfully"}), 200
    except subprocess.CalledProcessError as e:
        print(f"Error executing docker-stop.sh: {e}")
        return jsonify({"status": "Error stopping services", "error": str(e)}), 500
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        return jsonify({"status": "An unexpected error occurred", "error": str(e)}), 500

def get_system_info():
    return {
        "ip_address": subprocess.getoutput("hostname -I").strip(),
        "running_processes": subprocess.getoutput("ps -ax"),
        "available_disk_space": subprocess.getoutput("df -h /"),
        "uptime": subprocess.getoutput("uptime -p")
    }

@app.route('/service1')
def index():
    print("calling....")
    service1_info = get_system_info()

    # Call Service 2 (assumed to run on the same Docker network)
    service2_info = requests.get('http://srvc2:8199').json()

    time.sleep(2)  # Delay response
    return jsonify({
        "Service1": service1_info,
        "Service2": service2_info
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8199)
