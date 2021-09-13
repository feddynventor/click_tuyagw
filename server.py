import flask
from flask import request
from flask_cors import CORS, cross_origin

import pymongo
import pprint
mongo = pymongo.MongoClient("10.0.0.9", 27017)

import commander
import main

import threading
import time
lastSend = 0
lastMessage = {}

def pending_watcher():
    global lastMessage
    while True:
        # print("PENDING",len(lastMessage.items()))
        if (lastMessage and not lastMessage["executed"]):
            if (int(time.time()*1000) - lastMessage["timestamp"]) >= 1000:
                print("PENDING", lastMessage)
                # commander.set_light(
                #     lastMessage["dev"],
                #     lastMessage["rgb"], lastMessage["bright"], lastMessage["white"]
                # )
                device_op(lastMessage["uuid"], lastMessage["op"], lastMessage["req"])
                lastMessage = {}

        time.sleep(1)
        
pending_packet = threading.Thread(target=pending_watcher, name="PendingPacket")
pending_packet.start()

import datetime

app = flask.Flask(__name__, static_folder='gui_dashboard', static_url_path='')
# app.config["DEBUG"] = True
CORS(app, resources={r"/api/*": {"origins": "*"}})

devices = mongo.tuyagw.devices  #mongo.db.collection

if devices.count_documents({"ip": "None"})>0 or devices.count_documents({"api": "None"})>0:
    print("### NEW DEVICES ### without IP registered")
    commander.scan_ip(devices)

groups = mongo.tuyagw.groups
print( "### DEVICE GROUPS ###" )
pprint.pprint( [x for x in groups.find({},{"_id":0})] )

ping_device = threading.Thread(target=commander.ping_device, args=(devices), name="PingDevices")
# TypeError: 'Collection' object is not iterable
# ping_device.start()

#### API ####

@app.route('/api/', methods=['GET'])
def timestamp():
    return main.answer(data=datetime.datetime.now().timestamp())

@app.route('/api/dev/new', methods=['POST'])
def device_new():  #Aggiunta singola
    if not request.json["id"]:
        return main.answer(code=400)
    devices.insert_one({
        "id":request.json["id"],
        "key":request.json["key"],
        "name":request.json["name"],
        "ip":request.json["ip"],
        "api":request.json["api"]
    })
    return main.answer()

@app.route('/api/dev/<group>/list', methods=['GET'])
def device_get(group): #Lista completa
    response = []
    for dev in devices.find( {"group":group} if (group!="0") else {} ):
        if '_id' in dev:
            del dev['_id']
        response.append(dev)
    
    return main.answer(response)

@app.route('/api/dev/update', methods=['POST'])
def device_update(): #Inserimento da Tuya-cli

    # [ { name: 'giftwhole（rgb）',
    #     id: 'bf957f7112e75c1cedxeuw',
    #     key: '1016d5554017e8a4' } ]
    
    for dev in request.json:
        # print(dev)
        if devices.count_documents({"id":dev['id']})>0:
            devices.update( {"id":dev['id']}, {"$set":{'key': dev['key'], 'name': dev['name']}} )
        else:
            devices.insert_one({
                "id":dev["id"],
                "key":dev["key"],
                "name":dev["name"],
                "ip":None,
                "api":None
            })

        #     data[dev['id']] = {
        #         "key":dev["key"],
        #         "name":dev["name"],
        #         "ip":"waiting-scan"
        #     }

    return main.answer(data={"num":len(request.json)})


@app.route('/api/dev/<uuid>/test', methods=['GET'])
def device_test(uuid):
    # threading.Thread(target=lamp_device, args=db.search(Device.id==uuid), name=str(datetime.datetime.now().timestamp())).start()
    threading.Thread(target=lamp_device, args=([x for x in devices.find({"id": uuid},{"_id":0})]), name=str(datetime.datetime.now().timestamp())).start()
    return main.answer()

def lamp_device(d):
    print("BLINKING", d)
    commander.set_light(d, bright=100)
    for i in range(2,10):
        commander.set_power(d, bool(i%2==0))
        time.sleep(0.8)

    
@app.route('/api/dev/<uuid>/<op>', methods=['POST'])
def device_operation(uuid, op):
    global lastSend
    global lastMessage

    lastMessage["timestamp"] = int(time.time()*1000)
    lastMessage["uuid"] = uuid
    lastMessage["op"] = op
    lastMessage["req"] = request.json
    lastMessage["executed"] = False

    print(int(time.time()*1000) - lastSend)
    if ((int(time.time()*1000) - lastSend) < 1000):
        return main.answer(code=207)

    device_op(uuid, op, request.json)
    lastSend = int(time.time()*1000)
    lastMessage["executed"] = True

    return main.answer(code=200)

def device_op(uuid, op, req):
    if uuid in ( [x["id"] if x else None for x in groups.find({},{"_id":0,"id":1})] ):  # array degli id gruppi
        devlist = [x for x in devices.find({"group": uuid},{"_id":0})]  # lo UUID indicato in realtà è il gruppo
    elif uuid=="0":
        devlist = [x if (x['ip']!=None) else None for x in devices.find({},{"_id":0})]  # tutti i dispositivi raggiungibili
    else:
        devlist = [x for x in devices.find({"id": uuid},{"_id":0})]  # unico dispositivo
    
    devlist = [x for x in devlist if x is not None]
    if len(devlist)==0:
        return main.answer(code=400)

    # Aggiorna stato nel database JSON, non preclude il funzionamento, migliora affidabilità

    if op == '0': #Spegni
        for d in devlist:
            threading.Thread(target=commander.set_power, args=(d, False), name=str(datetime.datetime.now().timestamp())).start()
        
        # db.update({'power':'off'}, doc_ids=toupdate)
    
    if op == '1': #Accendi
        for d in devlist:
            threading.Thread(target=commander.set_power, args=(d, True), name=str(datetime.datetime.now().timestamp())).start()
    
        # db.update({'power':'on'}, doc_ids=toupdate)
    
    if op == '2': #Custom
        # if req.get("rgb",None) is not None:
        #     db.update({'rgb':req.get("rgb")}, doc_ids=toupdate )
        # if req.get("bright",None) is not None:
        #     db.update({'bright':req.get("bright")}, doc_ids=toupdate )
        # if req.get("white",None) is not None:
        #     db.update({'white':req.get("white")}, doc_ids=toupdate )
        
        for d in devlist:
            threading.Thread(target=commander.set_light, args=(d, req.get("rgb",None), req.get("bright",None), req.get("white",None)), name=str(datetime.datetime.now().timestamp())).start()
    
    return True

@app.route('/api/dev/<uuid>/status', methods=['GET'])
def device_status(uuid):
    # commander.get_status( db.search(Device.id == uuid)[0] )
    # [{'id': 'bf957f7112e75c1cedxeuw', 'key': '1016d5554017e8a4', 'name': 'giftwhole（rgb）', 'ip': '10.0.0.17', 'api': '3.3'}]

    return main.answer( commander.get_status( ([x for x in devices.find({"id": uuid},{"_id":0})])[0] ) )

@app.route('/api/dev/<uuid>/prop', methods=['GET'])
def device_prop(uuid):
    return main.answer( ([x for x in devices.find({"id": uuid},{"_id":0})])[0] )

@app.route('/api/dev/<uuid>/delete', methods=['GET'])
def device_delete(uuid):
    devices.remove({"id":uuid})
    return main.answer(code=200)

@app.route('/api/dev/scan', methods=['GET'])
def device_scan():
    number_updated = commander.scan_ip(devices)
    print( ([x for x in devices.find({},{"_id":0,"id":1,"ip":1,"name":1})]) )
    return main.answer( data={"number":number_updated} )


@app.route('/api/group/new', methods=['POST'])
def group_new():
    groups.insert({"id":str(hash(datetime.datetime.now().timestamp())),"name":request.json["name"]})
    return main.answer()

@app.route('/api/group/<id>/bind', methods=['POST'])
# ["bfece89fc7c58881as65m0","bfece89fc7c58881asaem0","bf9fd3e9354032418ec9m6"]
def group_bind(id):
    for d in request.json:
        devices.update_many({"id":d}, {"$set":{"group":id}})
    return main.answer()

@app.route('/api/group/<id>/bind2', methods=['POST'])
# [ { "name": "Smart Bulb CA 4.5",
#     "id": "bfece89fc7c58881as65m0",
#     "key": "2c85d3ed288960be" },
#   { "name": "Smart Bulb LA 2.10",
#     "id": "bfec5aba4139d7cgfd2e1f",
#     "key": "bd3a72d239517e90" },
#   { "name": "Smart Bulb CA 4.5",
#     "id": "bfece89ft5c58881asaem0",
#     "key": "2c85d3ed288960be" } ]
def group_bind2(id):
    for d in request.json:
        devices.update_many({"id":d["id"]}, {"$set":{"group":id}})
    
    return main.answer()

@app.route('/api/group/list', methods=['GET'])
def group_get():
    # RESPONSE
    # [  {
    #     "devs": [
    #       "bfece89fc7c58881bfaem0",
    #       "bfec5ab7a4139d7cc7pk1f"
    #     ],
    #     "id": "70434166750730113",
    #     "name": "Stanza 2"
    # }, ...]

    result = []
    gids = [x for x in groups.find({},{"_id":0})]  # ID Gruppo e Nome
    print(gids)
    for g in gids:
        result.append({
            "id":g['id'], "name":g['name'],
            "devs":[x['id'] for x in devices.find({"group": g['id']},{"_id":0,"id":1})]
        })
    return main.answer(result)


# @app.route('/api/new/<uuid>', methods=['GET, POST'])
# def add_message(uuid):
#     content = request.json
#     print(content) #JSON body
#     return jsonify({"uuid":uuid}) #url parameter

app.run(host='0.0.0.0')