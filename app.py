from ssl import PROTOCOL_TLS, CERT_REQUIRED, SSLContext
from flask_limiter.util import get_remote_address
from flask import Flask, render_template, request, send_from_directory,  jsonify
from flask_socketio import SocketIO, emit
from flask_limiter import Limiter
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename
import socket
import os
import rsa
import gzip
import time


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Added CORS allowance for all origins
limiter = Limiter(
    app=app,
    key_func=get_remote_address
)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_LIMIT = 200 * 1024 * 1024  # 200MB
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = UPLOAD_LIMIT

public_key, private_key = rsa.newkeys(2048)
message_senders = {}
from flask import jsonify

@app.route('/get-server-ip', methods=['GET'])
def get_server_ip():
    hostname = socket.gethostname()    
    ip_address = socket.gethostbyname(hostname)    
    return ip_address
    
@app.route('/get-client-ip', methods=['GET'])
def get_client_ip():
    return request.remote_addr, 200
    
@socketio.on('get_statistics')
def handle_statistics_request():
    client_ip = request.remote_addr
    server_ip = '192.168.1.15'  # This can be fetched dynamically if required.
    emit('update_statistics', {'client_ip': client_ip, 'server_ip': server_ip})


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('send_message')
def handle_message(data):
    sender_ip = request.remote_addr
    last_sent_time = message_senders.get(sender_ip, None)
    
    if last_sent_time and time.time() - last_sent_time < 5:
        # It's been less than 5 seconds since the last message
        emit('error_message', {'error': 'You can send a message every 5 seconds only.'})
        return

    nickname = data['nickname']
    encrypted_message = rsa.encrypt(data['message'].encode(), public_key)
    decrypted_message = rsa.decrypt(encrypted_message, private_key).decode()
    emit('receive_message', {'message': f"{nickname}: {decrypted_message}"}, broadcast=True)
    
    message_senders[sender_ip] = time.time()

TEXT_EXTENSIONS = {
    'txt', 'csv', 'xml', 'json', 'html', 'css', 'js',
    'md', 'rst', 'ini', 'yml', 'yaml', 'conf', 'log', 'sql', 'bat', 'sh', 
    'py', 'cpp', 'c', 'h', 'hpp', 'java', 'rb', 'go', 'php', 'pl', 'm',
    'f', 'f90', 'f95', 'f03', 'f08', 'tex', 'bib', 'kt', 'rs', 'toml', 
    'jsx', 'tsx', 'ts', 'less', 'scss', 'sass', 'lua', 'r', 'swift', 'vb', 
    'vbs', 'ps1', 'mm', 'patch', 'diff'
}


@limiter.limit("1/minute")
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    
    filename = secure_filename(file.filename)
    file_extension = filename.rsplit('.', 1)[1].lower()
    
    if file and allowed_file(filename):
        if request.content_length > UPLOAD_LIMIT:
            raise RequestEntityTooLarge

        if file_extension in TEXT_EXTENSIONS:
            # Compress text-like files using gzip
            with gzip.open(os.path.join(app.config['UPLOAD_FOLDER'], filename + '.gz'), 'wb') as f_out:
                f_out.writelines(file)
            emit('file_uploaded', {'filename': filename + '.gz'}, namespace='/', broadcast=True)
        else:
            # Directly save non-textual files without compression
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            emit('file_uploaded', {'filename': filename}, namespace='/', broadcast=True)

        return 'File uploaded'

    return 'Invalid file or file type'


@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
context = SSLContext(PROTOCOL_TLS)
context.load_cert_chain(certfile='ec_cert.pem', keyfile='ec_key.pem')
context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384')

if __name__ == '__main__':
	socketio.run(app, debug=True, host='192.168.1.15', port=5000, ssl_context=context)

