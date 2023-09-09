import requests


def notify(last_error, errors):
    requests.post('http://localhost:4444/slack',
                  json={'last_error': last_error, 'errors': errors})
