import time
import urllib.request
import json


def json_openener(url_link):
    start = time.time()
    with urllib.request.urlopen(url_link) as url:
        data = json.loads(url.read().decode())
    end = time.time()
    print("took {} secs".format(end - start))
    
    return data
