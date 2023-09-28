const socket = io.connect('https://192.168.1.15:5000', {secure: true});
let lastMessageTime = 0;
let lastFileUploadTime = 0;

// Elements to display the statistics
let clientIPElement = document.getElementById('clientIP');
let serverIPElement = document.getElementById('serverIP');
let pingElement = document.getElementById('ping');

socket.on('receive_message', function(data) {
    let msg = data['message'];
    document.getElementById("messages").innerHTML += `<p>${msg}</p>`;
});

socket.on('error_message', function(data) {
    alert(data['error']);
});

socket.on('file_uploaded', function(data) {
    let filename = data['filename'];
    let msg = `shared file ${filename}`;
    document.getElementById("messages").innerHTML += `<p>${msg}</p>`;
    document.getElementById("messages").innerHTML += `<a href="/uploads/${filename}" target="_blank">${filename}</a>`;
});

document.getElementById("message").addEventListener('keydown', function(e) {
    if (e.ctrlKey && e.keyCode == 13) {
        e.preventDefault();  // Prevents adding a new line in the textarea when Ctrl+Enter is pressed
        sendMessage();
    }
   

});


function sendMessage() {
    const currentTime = new Date().getTime();

    if (currentTime - lastMessageTime < 5000) {
        alert("You can send a message every 5 seconds.");
        return;
    }

    let nickname = document.getElementById("nickname").value;
    let message = document.getElementById("message").value;
    socket.emit('send_message', {'nickname': nickname, 'message': message});
    document.getElementById("message").value = "";

    lastMessageTime = currentTime;
}

function shareFile() {
    const currentTime = new Date().getTime();

    if (currentTime - lastFileUploadTime < 60000) {
        alert("You can upload a file once every 60 seconds.");
        return;
    }

    let input = document.createElement('input');
    input.type = 'file';
    input.onchange = e => {
        let file = e.target.files[0];
        
        if (file.size > 200 * 1024 * 1024) { // 200MB
            alert('File size should be less than 200MB.');
            return;
        }

        let formData = new FormData();
        formData.append('file', file);
        
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(data => {
            if(data !== 'File uploaded') {
                alert('Failed to upload file. Please try again.');
            }
        })
        .catch(error => {
            console.error('There was a problem with the file upload:', error);
            alert('Failed to upload file. Please try again.');
        });

        lastFileUploadTime = currentTime;
    };
    input.click();
}

// Handle stats updates from the server
socket.on('update_statistics', function(data) {
    let endPingTime = Date.now();
    let ping = endPingTime - startPingTime;

    clientIPElement.textContent = "Client IP: " + data.client_ip;
    serverIPElement.textContent = "Server IP: " + data.server_ip;
    pingElement.textContent = "Ping: " + ping + " ms";
});

// Request for stats update from the server
function requestStatsUpdate() {
    startPingTime = Date.now();
    socket.emit('get_statistics');
}

// Call the requestStatsUpdate function every 10 seconds
setInterval(requestStatsUpdate, 10000);

// Initial request to display stats on page load
requestStatsUpdate();

