import requests


def notify(data):
    try:
        requests.post('http://localhost:4444/slack', data=data)
    except:
        pass
