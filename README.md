
# WebChat – Secure Chat Application

WebChat is a real-time chat application designed with a strong emphasis on user privacy and data protection. Utilizing double encryption, WebChat ensures that your messages are always kept away from prying eyes.
Table of Contents

## Features

  Real-Time Chat: Seamless real-time messaging to keep you connected with your peers.
  
  File Sharing: Share documents and media files with complete peace of mind.

  Client-Server Architecture: Ensures fast message delivery without compromising on security.

  Intuitive User Interface: A user-friendly design to make your chat experience smooth.

## Double Encryption

WebChat prioritizes security by using a double encryption mechanism. This provides an additional layer of protection, ensuring that even if one encryption method is compromised, the data remains protected by the second encryption layer.
How Double Encryption Works

At a high level, double encryption involves:

First Layer of Encryption: The initial data is encrypted using the first encryption algorithm, producing an intermediary encrypted result.

Second Layer of Encryption: This intermediary encrypted result is then encrypted again using a second, different encryption algorithm.

To decrypt the data, the process is simply reversed: The data is first decrypted using the second encryption algorithm, and then again using the first.
Benefits of Double Encryption

Enhanced Security: Even if an attacker manages to break one encryption layer, the data remains secure behind the second layer.

Mitigate Risks: In the case of any vulnerabilities found in one encryption algorithm, the data is still protected by the second encryption method.

Increase Difficulty for Brute Force Attacks: Double encryption considerably increases the computational power and time required to perform brute force attacks.

## Encryption Algorithms Used

First Layer: AES (Advanced Encryption Standard) – A symmetric encryption algorithm that's widely recognized for its robustness and speed. It uses block ciphers to encrypt and decrypt data in blocks.

Second Layer: RSA (Rivest–Shamir–Adleman) – An asymmetric encryption algorithm. It uses a pair of keys: a public key, which encrypts data, and a private key, which decrypts data. This ensures that even if the public key is known, the data cannot be decrypted without the private key.

## Why Double and Not Single Encryption?

While single encryption might be sufficient for many applications, double encryption is chosen for scenarios where data sensitivity is extremely high, or where regulatory or compliance demands dictate stronger data protection. By using two distinct encryption methods, we ensure that the vulnerabilities or weaknesses of one method are offset by the strengths of the other.
Considerations

Performance: Double encryption requires more computational resources than single encryption. However, for applications where security is paramount, this trade-off is often deemed acceptable.

Key Management: Properly managing and storing the encryption keys is crucial. Losing access to the keys, especially with RSA's private key, means data can become irretrievable.

## Getting Started

Clone the repository:

    git clone https://github.com/ishaiva/webappchat.git

Navigate into the project directory:

    cd webchat

Install the required packages:

    pip install -r requirements.txt

setup keys

    sudo python3 setup.py

![setup_Screenshot](https://github.com/ishaiva/webappchat/assets/111692746/7fe705bd-b1b8-4b7f-9f59-f3f602e9ed83)

## Configuration for Deployment

Before running the application, you'll need to configure a few settings to make it compatible with your environment.
1. Set Server IP Address and Port

Both the application server and the client-side JavaScript need to know where your server is running.
Python App Configuration:

In app.py (or wherever your main application file is located), look for a line similar to:

python

    socketio.run(app, host='192.168.x.x', port=5000)

Replace '192.168.x.x' with your server's IP address and 5000 with your desired port if different.
Client-side JavaScript Configuration:

In static/script.js, locate a line similar to:

javascript

    var socket = io.connect('http://192.168.x.x:5000/');

Replace 'http://192.168.x.x:5000/' with the correct server IP and port in the format 'http://[YOUR_SERVER_IP]:[YOUR_PORT]/'.

2. Ensure Port Availability

Make sure the port you've chosen (e.g., 5000 in the example) is open and available on your server, and there's no firewall blocking incoming/outgoing requests to that port.

Run the application:

    sudo python3 app.py

![app_Screenshot_in_ter](https://github.com/ishaiva/webappchat/assets/111692746/2decd03f-b2d4-4238-8323-0bddd6582131)

### Usage

Open a web browser and navigate to https://192.168.x.x:5000. 
Enter a nickname and start chatting. You can also share files and view your connection statistics.

![webappGUIScreenshot](https://github.com/ishaiva/webappchat/assets/111692746/a5bf977e-1826-40a4-8850-22438e76499b)

### Contributing

Contributions, issues, and feature requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### License MIT

This project is licensed under the MIT License.
Copyright 2023 ishaiva

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE.

