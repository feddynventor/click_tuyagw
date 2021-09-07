#!/usr/bin/env python

# WS server that sends messages at random intervals

import asyncio
import websockets

import json

from tinydb import TinyDB, Query
db = TinyDB('db.json')
Device = Query()

from multiping import multi_ping

async def time(websocket, path):
    while True:
        addrs = []
        for dev in db:
            if dev["ip"] is not None:
                addrs.append(dev["ip"])
        print("TO PING", addrs)
        responses, no_responses = multi_ping(addrs, timeout=2, retry=3)

        for dev in responses:
            db.update({"state":"on"}, Device.id == db.search(Device.ip == ip)["id"])
            await websocket.send( json.dumps(db.search(Device.state == "on")) )

        for ip in no_responses:
            db.update({"state":"ko"}, Device.id == db.search(Device.ip == ip)["id"])
            print("KO Devices", no_responses)
            await websocket.send( json.dumps(db.search(Device.state == "on")) )

        await asyncio.sleep(15)


start_server = websockets.serve(time, "127.0.0.1", 8765)

# asyncio.get_event_loop().create_task(start_server)
# asyncio.get_event_loop().run_forever()