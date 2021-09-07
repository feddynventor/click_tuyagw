import flask
from flask import request
from flask_cors import CORS, cross_origin
from tinydb import TinyDB, Query

import commander
import main

import threading
pending_packet = threading.Thread(target=commander.pending_packet, name="PendingPacket")
pending_packet.start()
ping_device = threading.Thread(target=commander.ping_device, name="PingDevices")
ping_device.start()

# import asyncio
# import wss
# asyncio.get_event_loop().create_task(wss.start_server)

# App Libraries
import datetime

app = flask.Flask(__name__)
# app.config["DEBUG"] = True
CORS(app, resources={r"/api/*": {"origins": "*"}})
db = TinyDB('db.json')
    
Device = Query()
if len(db.search(Device.ip == "None"))>0 or len(db.search(Device.api == "None"))>0:
    commander.scan_ip()


#### API ####

@app.route('/api/', methods=['GET'])
def timestamp():
    return main.answer(data=datetime.datetime.now().timestamp())

@app.route('/api/dev/new', methods=['POST'])
def device_new():  #Aggiunta singola
    if not request.json["id"]:
        return main.answer(code=400)
    db.insert({
        "id":request.json["id"],
        "key":request.json["key"],
        "name":request.json["name"],
        "ip":request.json["ip"],
        "api":request.json["api"]
    })
    return main.answer()

@app.route('/api/dev/list', methods=['GET'])
def device_get(): #Lista completa
    return main.answer(db.all())

@app.route('/api/dev/update', methods=['POST'])
def device_update(): #Inserimento da Tuya-cli

    # [ { name: 'giftwhole（rgb）',
    #     id: 'bf957f7112e75c1cedxeuw',
    #     key: '1016d5554017e8a4' } ]
    
    for dev in request.json:
        # print(dev)
        if db.search(Device.id == dev['id']):
            db.update({'key': dev['key'], 'name': dev['name']}, Device.id == dev['id'])
        else:
            db.insert({
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

    return main.answer()


@app.route('/api/dev/<uuid>/<op>', methods=['POST'])
def device_operation(uuid, op):
    if uuid=="all":
        dev = db.search(Device.ip != None)  # tutti i dispositivi raggiungibili
    else:
        dev = db.search(Device.id == uuid)  # unico dispositivo
        if len(dev)==0:
            return main.answer(code=400)

    for d in dev:
        if op == '0': #Spegni
            commander.set_power(d, on=False)
            db.update({'power':'off'}, Device.id == uuid)
        if op == '1': #Accendi
            commander.set_power(d)
            db.update({'power':'on'}, Device.id == uuid)
        if op == '2': #Custom
            # commander.set_power(dev)
            
            if request.json.get("rgb",None) is not None:
                commander.set_light(d,rgb=request.json.get("rgb"))
            if request.json.get("bright",None) is not None:
                commander.set_light(d,bright=request.json.get("bright"))
            if request.json.get("white",None) is not None:
                commander.set_light(d,white=request.json.get("white"))

    return main.answer(code=200)
 
@app.route('/api/dev/<uuid>/status', methods=['GET'])
def device_status(uuid):
    # commander.get_status( db.search(Device.id == uuid)[0] )
    # [{'id': 'bf957f7112e75c1cedxeuw', 'key': '1016d5554017e8a4', 'name': 'giftwhole（rgb）', 'ip': '10.0.0.17', 'api': '3.3'}]

    # db.update({'state': {'power':'on'}}, Device.id == uuid)

    return main.answer( commander.get_status( db.search(Device.id == uuid)[0] ) )

@app.route('/api/dev/<uuid>/prop', methods=['GET'])
def device_prop(uuid):
    return main.answer( db.search(Device.id == uuid)[0] )

@app.route('/api/dev/<uuid>/delete', methods=['GET'])
def device_delete(uuid):
    db.remove(Device.id == uuid)
    return main.answer(code=200)



@app.route('/api/dev/scan', methods=['GET'])
def device_scan():
    commander.scan_ip()
    return main.answer( db.all() )

# @app.route('/api/new/<uuid>', methods=['GET, POST'])
# def add_message(uuid):
#     content = request.json
#     print(content) #JSON body
#     return jsonify({"uuid":uuid}) #url parameter

app.run(host='0.0.0.0')