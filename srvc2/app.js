const express = require('express');
const { execSync } = require('child_process');
const os = require('os');

const app = express();

function getIpAddress() {
    try {
        const networkInterfaces = os.networkInterfaces();
        for (const interfaceName in networkInterfaces) {
            for (const network of networkInterfaces[interfaceName]) {
                if (network.family === 'IPv4' && !network.internal) {
                    return network.address; // Return first non-internal IPv4 address
                }
            }
        }
        return 'Unknown IP';
    } catch (error) {
        console.error("Error fetching IP address:", error.message);
        return 'Error fetching IP';
    }
}

function getRunningProcesses() {
    try {
        const command = os.platform() === 'win32' ? 'tasklist' : 'ps -ax';
        return execSync(command).toString();
    } catch (error) {
        console.error("Error fetching processes:", error.message);
        return 'Error fetching processes';
    }
}

function getDiskSpace() {
    try {
        const command = os.platform() === 'win32' ? 'wmic logicaldisk get size,freespace,caption' : 'df -h /';
        return execSync(command).toString();
    } catch (error) {
        console.error("Error fetching disk space:", error.message);
        return 'Error fetching disk space';
    }
}

function getUptime() {
    try {
        const uptimeInSeconds = os.uptime();
        const uptimeInHours = (uptimeInSeconds / 3600).toFixed(2);
        return `System uptime: ${uptimeInHours} hours`;
    } catch (error) {
        console.error("Error fetching uptime:", error.message);
        return 'Error fetching uptime';
    }
}

app.get('/', (req, res) => {
    const systemInfo = {
        ip_address: getIpAddress(),
        running_processes: getRunningProcesses(),
        disk_space: getDiskSpace(),
        uptime: getUptime(),
    };
    res.json(systemInfo);
});

app.listen(8199, () => {
    console.log('Service 2 is running on port 8199');
});
