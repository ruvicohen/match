import requests

def get_dbz(url):
    response = requests.get(url)
    return response.json()