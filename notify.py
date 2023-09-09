import requests
import json


def notify(data):
    requests.post('http://localhost:4444/slack', data=data)
