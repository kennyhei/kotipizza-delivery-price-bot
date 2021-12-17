from flask import Flask
from flask import request


app = Flask(__name__)


@app.route('/<string:text>', methods=['POST'])
def webhook():
    print(request)
    print(request.get_json(force=True))
    return 'ok'


@app.route('/')
def index():
    return 'moi!'
