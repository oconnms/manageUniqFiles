# MUFUtils.py

import pickle
import hashlib

def md5sumOfFile(file):
    with open(file, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()

def md5sum(string):
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()

def save_obj(obj, name):
    with open('obj\\' + name + '.pkl', 'wb+') as f:
        pickle.dump(obj, f, 0)

def load_obj(name):
    with open('obj\\' + name + '.pkl', 'rb') as f:
        return pickle.load(f)
