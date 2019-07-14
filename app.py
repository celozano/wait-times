import json
import requests

from flask import Flask, jsonify, redirect
from flask_cors import CORS
from helper import get_wait_times

with open('config.json', 'r') as f:
  config = json.load(f)

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
  return redirect("https://notengosentri.com")

@app.route('/wait_times')
def wait_times():
  try:
    r = requests.get(config['URL'], timeout=5)
    r.raise_for_status()

    response = get_wait_times(r.text)
    return jsonify(response)
  except requests.exceptions.RequestException as e:
    response = {
      "err": {
         "message": e
       }
    }

    return jsonify(response)

if __name__ == '__main__':
  app.run(host='0.0.0.0')
