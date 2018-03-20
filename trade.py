#!/usr/bin/env python
'''

'''
import asyncio
import websockets
import datetime
import json
import hashlib

apikeypair= ("api_key","**************************")
apikey = "*********************************"

def get_sign(params):
    sign_str = '&'.join([k+'='+v for k,v in sorted(params)])+'&secret_key=346BD975D145C1686705BB07411ADEFC'
    print(sign_str)
    return hashlib.md5(sign_str.encode('utf8')).hexdigest().upper()



websocket = ''
async def hello():
    global websocket
    websocket = await websockets.connect('wss://real.okex.com:10441/websocket')

    send_string = json.dumps({"event":"login","parameters":{"api_key":apikey,"sign":get_sign([apikeypair])}})
    print(send_string)
    await websocket.send(send_string)
    #await websocket.send("{'event':'addChannel','channel':'ok_sub_spot_etc_btc_depth_3'}")

    #await websocket.send("{'event':'addChannel','channel':'ok_sub_spot_ltc_btc_depth_5'}")
    #await websocket.send("{'event':'removeChannel','channel':'ok_sub_spot_etc_btc_depth_5'}")
        #print("> {}".format(name))
    while True:
        #await websocket.send(name)
        greeting = await websocket.recv()
        print(datetime.datetime.now())
        print("< {}".format(greeting))
        greet_json = json.loads(greeting)
        # if greet_json[0]['channel'] == 'ok_sub_spot_etc_btc_depth_5':
        #     await websocket.send("{'event':'removeChannel','channel':'ok_sub_spot_etc_btc_depth_5'}")
        #     await websocket.send("{'event':'addChannel','channel':'ok_sub_spot_ltc_btc_depth_5'}")
        # if greet_json[0]['channel'] == 'ok_sub_spot_ltc_btc_depth_5':
        #     await websocket.send("{'event':'removeChannel','channel':'ok_sub_spot_ltc_btc_depth_5'}")
        #     await websocket.send("{'event':'addChannel','channel':'ok_sub_spot_etc_btc_depth_5'}")

asyncio.get_event_loop().run_until_complete(hello())
asyncio.get_event_loop().run_forever()
