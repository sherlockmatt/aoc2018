import requests


def download(url):
    # Session cookie is stored in a separate file so we can avoid cheking it into Git
    with open('session.txt', 'r') as f:
        r = requests.get(url, cookies={'session': f.read()})
    if r.status_code != 200:
        r.raise_for_status()

    return r


def manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)
