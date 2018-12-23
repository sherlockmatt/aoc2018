import requests


def download(url):
    # Session cookie is stored in a separate file so we can avoid cheking it into Git
    with open('session.txt', 'r') as f:
        r = requests.get(url, cookies={'session': f.read()})
    if r.status_code != 200:
        r.raise_for_status()

    return r


def manhattan(point1, point2):
    dist = 0
    for axis in range(len(point1)):
        dist += abs(point1[axis] - point2[axis])
    return dist
