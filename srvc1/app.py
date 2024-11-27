from flask import Flask, jsonify, request
import os
import subprocess
import requests
import time
import sys
import psutil
import platform
import docker

app = Flask(__name__)

def get_ip_address():
    try:
        if platform.system() == "Windows":
            ip = subprocess.check_output("ipconfig", shell=True).decode()
            lines = [line.strip() for line in ip.split("\n") if "IPv4 Address" in line]
            return lines[0].split(":")[1].strip() if lines else "Unknown IP"
        else:
            ip = subprocess.check_output("hostname -I", shell=True).decode().strip()
            return ip
    except Exception as e:
        return f"Error fetching IP: {str(e)}"

def get_running_processes():
    try:
        if platform.system() == "Windows":
            processes = subprocess.check_output("tasklist", shell=True).decode('utf-8', 'ignore')
        else:
            processes = subprocess.check_output("ps -ax", shell=True).decode('utf-8', 'ignore')
        return processes
    except Exception as e:
        return f"Error fetching processes: {str(e)}"

def get_disk_space():
    try:
        if platform.system() == "Windows":
            disk_space = subprocess.check_output(
                "wmic logicaldisk get size,freespace,caption", shell=True
            ).decode()
        else:
            disk_space = subprocess.check_output("df -h /", shell=True).decode('utf-8', 'ignore')
        return disk_space
    except Exception as e:
        return f"Error fetching disk space: {str(e)}"

def get_uptime():
    try:
        uptime_seconds = time.time() - psutil.boot_time()
        uptime_hours = uptime_seconds / 3600
        return f"System uptime: {uptime_hours:.2f} hours"
    except Exception as e:
        return f"Error fetching uptime: {str(e)}"

@app.route('/stop-instances', methods=['POST'])
def stop_instances():
    try:
        client = docker.from_env()
        containers = client.containers.list()
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

@app.route('/service1')
def index():
    service1_info = get_system_info()
    service2_info = requests.get('http://srvc2:8199').json()

    time.sleep(2)
    return jsonify({
        "Service1": service1_info,
        "Service2": service2_info
    })

def get_system_info():
    return {
        "ip_address": get_ip_address(),
        "running_processes": get_running_processes(),
        "available_disk_space": get_disk_space(),
        "uptime": get_uptime()
    }

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8199)