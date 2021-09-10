# import pickle
from flask import jsonify
# import time

# def data_save(data):
#     with open('./db.pickle', 'wb') as f:
#         pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

# def data_load():
#     try:
#         with open('./db.pickle', 'rb') as f:
#             data = pickle.load(f)
#             return data
#     except:
#         return {}

# lastSend = 0
# def buffer(db, query, object_ref, key):
#     global lastSend
#     # print(int(time.time()*1000), lastSend, int(time.time()*1000) - lastSend)

#     if (int(time.time()*1000) - lastSend > 400):
#         lastSend = int(time.time()*1000)
    
#         # d.set_brightness_percentage(query["bright"])
    
#         db.update(query, object_ref.id == key)
    
#         lastSend = int(time.time()*1000)

def answer(data={},code=200):
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE')
    response.headers.add('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')
    return (response, code)