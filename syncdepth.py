#!/usr/bin/env python

import asyncio
import websockets
import time
import json
websocket = ''
async def hello():
    global websocket
    websocket = await websockets.connect('wss://real.okex.com:10441/websocket')
    await websocket.send("{'event':'addChannel','channel':'ok_sub_spot_etc_btc_depth_20'}")
    #await websocket.send("{'event':'addChannel','channel':'ok_sub_spot_etc_btc_depth_3'}")

    #await websocket.send("{'event':'addChannel','channel':'ok_sub_spot_ltc_btc_depth_5'}")
    #await websocket.send("{'event':'removeChannel','channel':'ok_sub_spot_etc_btc_depth_5'}")
        #print("> {}".format(name))
    while True:
        #await websocket.send(name)
        greeting = await websocket.recv()
        print("< {}".format(greeting))
        greet_json = json.loads(greeting)
        # if greet_json[0]['channel'] == 'ok_sub_spot_etc_btc_depth_5':
        #     await websocket.send("{'event':'removeChannel','channel':'ok_sub_spot_etc_btc_depth_5'}")
        #     await websocket.send("{'event':'addChannel','channel':'ok_sub_spot_ltc_btc_depth_5'}")
        # if greet_json[0]['channel'] == 'ok_sub_spot_ltc_btc_depth_5':
        #     await websocket.send("{'event':'removeChannel','channel':'ok_sub_spot_ltc_btc_depth_5'}")
        #     await websocket.send("{'event':'addChannel','channel':'ok_sub_spot_etc_btc_depth_5'}")

#asyncio.get_event_loop().run_until_complete(hello())
#asyncio.get_event_loop().run_forever()
websocket = websockets.connect('wss://real.okex.com:10441/websocket')
websocket.send("{'event':'addChannel','channel':'ok_sub_spot_etc_btc_depth_20'}")