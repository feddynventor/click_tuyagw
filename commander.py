import tinytuya
import time
from tinydb import TinyDB, Query
from multiping import multi_ping

db = TinyDB('db.json')
Device = Query()

#####################
# Pending packet da parte di server.py

#####################

def ping_device():
    while True:
        addrs = []
        for dev in db:
            if dev["ip"] is not None:
                addrs.append(dev["ip"])
        print("PINGING", addrs)
        responses, no_responses = multi_ping(addrs, timeout=5, retry=3)

        for ip in responses:
            db.update({"state":"on"}, Device.id == db.search(Device.ip == ip)[0]["id"])

        for ip in no_responses:
            db.update({"state":"ko"}, Device.id == db.search(Device.ip == ip)[0]["id"])
            print("DOWN PING",no_responses)

        time.sleep(25)

#####################

def scan_ip():
    print("SCAN IP STARTED")

    # fornisce una dummy key, usare quella di tuya-cli ottenuta tramite hijack
    devices = tinytuya.deviceScan()

    # 10.0.0.17 -> {'ip': '10.0.0.17', 'gwId': 'bf957f7112e75c1cedxeuw', 'active': 2, 'ablilty': 0, 'encrypt': True, 'productKey': 'keytg5kq8gvkv9dh', 'version': '3.3'}
    for key, value in devices.items():
        print("SCAN IP:", key, '->', value)

        if db.search(Device.id == value["gwId"]):
            db.update({'ip': key, 'api': value['version']}, Device.id == value["gwId"])
        else:
            db.insert({
                "id":value["id"],
                "name":value["name"],
                "key":None,
                "ip":key,
                "api":value['version']
            })

def get_status(dev):
    d = tinytuya.BulbDevice(dev['id'], dev['ip'], dev['key'])
    d.set_version(float(dev["api"]))
    return d.status()

def set_power(dev, on=True):
    d = tinytuya.BulbDevice(dev['id'], dev['ip'], dev['key'])
    d.set_version(float(dev["api"]))

    if on:
        d.turn_on()
    else:
        d.turn_off()

def set_light(dev, rgb=None, bright=None, white=None):
    d = tinytuya.BulbDevice(dev['id'], dev['ip'], dev['key'])
    d.set_version(float(dev["api"]))

    if rgb is not None:
        d.set_colour(rgb[0],rgb[1],rgb[2])
        # db.update({"rgb":rgb}, Device.id == dev['id'])
    if bright is not None:
        d.set_brightness_percentage(int(bright))
        # db.update({"bright":int(bright)}, Device.id == dev['id'])
    if white is not None:
        d.set_colourtemp_percentage(int(white))
        # db.update({"white":int(white)}, Device.id == dev['id'])
