const express = require('express');
const { execSync } = require('child_process');

const app = express();

function getSystemInfo() {
    return {
        ip_address: execSync('hostname -I').toString().trim(),
        running_processes: execSync('ps -ax').toString(),
        available_disk_space: execSync('df -h /').toString(),
        uptime: execSync('uptime -p').toString()
    };
}

app.get('/', (req, res) => {
    res.json(getSystemInfo());
});

app.listen(8199, () => {
    console.log('Service 2 is running on port 8199');
});
