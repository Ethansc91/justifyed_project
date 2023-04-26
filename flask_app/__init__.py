from flask import Flask
app = Flask(__name__)
app.secret_key = "aa45ge5657450trgefj569rht48523njkfjo50y"
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024