from flask import Flask, request
import hashlib
import hmac
from datetime import datetime
import pytz
import requests

app = Flask(__name__)

@app.route('/')
def hello_world():
    tallinn_timezone = pytz.timezone('Europe/Tallinn')
    current_time = datetime.now(tz=tallinn_timezone).strftime("%d%m%Y%H%M%S")
    return str(current_time)

@app.route('/get_data', methods=['GET'])
def hash_parameter():
    api_key = request.args.get('api_key')
    api_secret = request.args.get('api_secret')
    url_root = request.args.get('url_root')
    payload = request.args.get('payload')
    print(api_key, api_secret, url_root, payload)
    if api_key and api_secret and url_root:
        tallinn_timezone = pytz.timezone('Europe/Tallinn')
        current_time = str(datetime.now(tz=tallinn_timezone).strftime("%d%m%Y%H%M%S"))
        if len(payload) == 0:
            to_be_hashed = "timestamp=" + current_time + "&apikey=" + api_key
        else:
            to_be_hashed = payload + "&timestamp=" + current_time + "&apikey=" + api_key
        signature = hmac.new(api_secret.encode(), to_be_hashed.encode(), hashlib.sha256).hexdigest()
        api_url = url_root + "?"+ to_be_hashed +"&signature=" + signature
        response = requests.get(api_url)
        if response.status_code == 200:
            # API request was successful
            return response.json()
        else:
            # API request failed
            return "API request failed. Status code: " + str(response.status_code)
    else:
        return "Parameter not provided. Please provide a parameter and secret key."
    