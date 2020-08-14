import time
import urllib.request, json
import pickle
import numpy as np

def json_openener(url_link):
    start = time.time()
    with urllib.request.urlopen(url_link) as url:
        data = json.loads(url.read().decode())
    end = time.time()
    print("took {} secs".format(end - start))
    return data

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    # np.save(name, obj)

def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
    # return np.load(name)
