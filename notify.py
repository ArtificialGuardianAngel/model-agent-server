import requests
import json


def notify(data):
    json_data = json.dumps(data)
    requests.post('http://localhost:4444/slack', data=json_data)
