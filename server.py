import flask
from flask import request
from flask_cors import CORS, cross_origin
from tinydb import TinyDB, Query

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
ping_device = threading.Thread(target=commander.ping_device, name="PingDevices")
# ping_device.start()

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

groups = db.table('groups')
Group = Query()
print( "DEVICE GROUPS", groups.all() )

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

@app.route('/api/dev/<group>/list', methods=['GET'])
def device_get(group): #Lista completa
    if group=="0":
        return main.answer(db.all())
    else:
        return main.answer(db.search(Device.group==group))

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


@app.route('/api/dev/<uuid>/test', methods=['GET'])
def device_test(uuid):
    threading.Thread(target=lamp_device, args=db.search(Device.id==uuid), name=str(datetime.datetime.now().timestamp())).start()
    return main.answer()

def lamp_device(d):
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
    if uuid in ([g["id"] for g in groups.all()]):  # array degli id gruppi
        devlist = db.search(Device.group == uuid)  # lo UUID indicato in realtà è il gruppo
    elif uuid=="0":
        devlist = db.search(Device.ip != None)  # tutti i dispositivi raggiungibili
    else:
        devlist = db.search(Device.id == uuid)  # unico dispositivo
        if len(devlist)==0:
            return main.answer(code=400)

    # Aggiorna stato nel database JSON, non preclude il funzionamento, migliora affidabilità
    # toupdate = []
    # for d in devlist:
    #     toupdate.append( db.get(Device.id==d["id"]).doc_id )

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


@app.route('/api/group/new', methods=['POST'])
def group_new():
    groups.insert({"id":str(hash(datetime.datetime.now().timestamp())),"name":request.json["name"]})
    return main.answer()

@app.route('/api/group/<id>/bind', methods=['POST'])
# ["bfece89fc7c58881as65m0","bfece89fc7c58881asaem0","bf9fd3e9354032418ec9m6"]
def group_bind(id):
    toupdate = []
    notfound = []
    for d in request.json:
        try:
            toupdate.append( db.get(Device.id==d).doc_id )
        except:
            print(notfound.append(d))

    db.update({"group":id}, doc_ids=toupdate)
    
    if len(notfound)>0:
        return main.answer(code=207, data=notfound)
    else:
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
    idlist = []
    for dev in request.json:
        idlist.append(dev['id'])

    toupdate = []
    for d in idlist:
        toupdate.append( db.get(Device.id==d["id"]).doc_id )

    db.update({"group":id}, doc_ids=toupdate)
    return main.answer()

@app.route('/api/group/list', methods=['GET'])
def group_get():
    # [  {
    #     "devs": [
    #       "bfece89fc7c58881bfaem0",
    #       "bfec5ab7a4139d7cc7pk1f"
    #     ],
    #     "id": "70434166750730113",
    #     "name": "Stanza 2"
    # }, ...]
    try:
        mydict = {}  # chiave : ID gruppo & val : array di ID devices
        for g in groups.all():
            # print(g)
            mydict[g["id"]] = []  #DICT variant

        for dev in db:
            try:
                mydict[dev["group"]].append(dev["id"])
            except:  # Ignora se non hai ancora il gruppo
                continue
        # print(mydict.keys(), mydict.values())

        myarr = []  # riformatta tutto anche con il nome
        for gid, devs in mydict.items():
            myarr.append( {"id": gid, "name":groups.search(Group.id==gid)[0]["name"], "devs": devs} )

        return main.answer(myarr)
    except:
        return main.answer(code=500)

# @app.route('/api/new/<uuid>', methods=['GET, POST'])
# def add_message(uuid):
#     content = request.json
#     print(content) #JSON body
#     return jsonify({"uuid":uuid}) #url parameter

app.run(host='0.0.0.0')