from flask import Flask, request
import hashlib
import hmac

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/hash', methods=['GET'])
def hash_parameter():
    parameter = request.args.get('parameter')
    secret_key = request.args.get('secret_key')
    if parameter and secret_key:
        signature = hmac.new(secret_key.encode(), parameter.encode(), hashlib.sha256).hexdigest()
        return signature
    else:
        return "Parameter not provided. Please provide a parameter and secret key."