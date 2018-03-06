#!/usr/bin/env python
'''
apiKey:  eca729c5-cbf5-4333-8476-56bd0bb1009f
secretKey:  346BD975D145C1686705BB07411ADEFC

'''
import asyncio
import websockets
import datetime
import time
import json
import hashlib

apikeypair= ("api_key","eca729c5-cbf5-4333-8476-56bd0bb1009f")
apikey = "eca729c5-cbf5-4333-8476-56bd0bb1009f"
order_numbers = []
class finite_machine(object):
    """docstring for finite_machine"""
    def __init__(self,ws):
        self.ws = ws
        self.status = 0
        self.curr_price = ''
        self.curr_amount = ''
        self.a = 0
        self.b = 0

        self.log_file = opne('order.log','a')

        self.a_symbol = 'etc'
        self.b_symbol = 'eth'
        self.symbol = self.a_symbol+'_'+self.b_symbol
        self.depth_channel = "ok_sub_spot_{0}_depth_20".format(self.symbol)
        self.order_channel = "ok_sub_spot_{0}_order".format(self.symbol)


        depth_string = json.dumps({"event":"addChannel","channel":self.depth_channel})
        self.ws.send(depth_string)
        login_string = '{"event": "login","parameters": {"sign": "65A16B64192413F1F44227A73E8ADADF", "api_key": "eca729c5-cbf5-4333-8476-56bd0bb1009f"}}'
        self.ws.send(login_string)



    def _query_account():
        query_string = '{"channel": "ok_spot_userinfo", "parameters": {"sign": "65A16B64192413F1F44227A73E8ADADF", "api_key": "eca729c5-cbf5-4333-8476-56bd0bb1009f"}, "event": "addChannel"}'
        self.ws.send(query_string)
        self.status = 1
    def _check_account_value(message):
        if message[0]['data']['result'] == 'true':
            self.a = float(message[0]['data']['info']['funds']['free'][self.a_symbol])
            self.b = float(message[0]['data']['info']['funds']['free'][self.b_symbol])
            self.status = 2
        else:
            self.status == 0
    def order(self,message):
        ts = int(message[0]['data']['timestamp'])
        now = int(time.time()*1000)

        if now-ts>800:
            return
        self.order_type,self.depth_type=order_type,depth_type = \
        'sell','asks' if (self.a*float(message[0]['data']['asks'][0][0]))>self.b else 'buy','bids'
        self.curr_price = price = float(message[0]['data'][self.depth_type][0][0])
        self.curr_amount= amount = math.floor((self.b/price)*1e8)/1e8 if order_type=='buy' else self.a
        sign_pamams = [apikeypair,('symbol',self.symbol),('type',order_type),('price',str(price)),('amount',amount)]
        order_data = {'event':'addChannel','channel':'ok_spot_order',
        'parameters':{'api_key':'"eca729c5-cbf5-4333-8476-56bd0bb1009f"',
        'sign':get_sign(sign_pamams),'symbol':self.symbol,'type':order_type,'price':str(price),
        'amount':str(amount)}}
        print(json.dumps(order_data))
        #self.ws.send(json.dumps(order_data))
        self.status = 3

    def check_order_send_result(message):
        print(message)
        if message[0]['data']['result'] == 'true':
            self.orderId = message[0]['data']['order_id']
            self.status = 4
            order_numbers.append(message)
            
        else:
            self.status = 0
            print('order wrong')
            exit()
    def check_order_excute_result(message):
        stus = message[0]['data']['status']
        if  stus == 2:
            self.status = 0
        elif stus == 1:
            print(message)
    def check_should_cancel(message):

        comapre_price = float(message[0]['data'][self.depth_type][-1][0])
        com_result = (self.curr_price>comapre_price) if (self.order_type=='sell') else (self.curr_price<comapre_price)
        if com_result:
            cancel_data = 
                {
                    'event':'addChannel','channel':'ok_spot_cancel_order',
                    'parameters':{'api_key':apikey,
                        'sign':get_sign([apikeypair,('symbol',self.symbol),('order_id',self.order_id)]),
                        'symbol':self.symbol,
                        'order_id':self.order_id
                    }
                }
            self.ws.send(json.dumps(cancel_data))
            self.status = 5
    def check_cancel_result(message):
        if message[0]['data']['result'] == True:
            self.status = 0
            print(message.file=self.log_file)
        else:
            print(message.file=self.log_file)




    def check_message(self,message=None):
        if self.status == 0:
            self._query_account()
        elif self.status == 1:
            if message[0]['channel'] == 'ok_spot_userinfo':
                self._check_account_value(message)
        elif self.status == 2:
            if message[0]['channel'] == self.depth_channel:
                self.order(message)
        elif self.status == 3:
            if message[0]['channel'] == "ok_spot_order":
                self.check_order_send_result(message)
        elif self.status == 4:
            if message[0]['channel'] == self.order_channel:
                self.check_order_excute_result(message)
            elif message[0]['channel'] == self.depth_channel:
                self.check_should_cancel(message)
        elif self.status == 5:
            if message[0]['channel'] == 'ok_spot_cancel_order':
                self.check_cancel_result(message)

        

def get_sign(params):
    sign_str = '&'.join([k+'='+v for k,v in sorted(params)])+'&secret_key=346BD975D145C1686705BB07411ADEFC'
    print(sign_str)
    return hashlib.md5(sign_str.encode('utf8')).hexdigest().upper()



websocket = ''
async def hello():
    global websocket
    websocket = await websockets.connect('wss://real.okex.com:10441/websocket')

    send_string = json.dumps({"event":"addChannel","channel":"ok_spot_userinfo","parameters":{"api_key":apikey,"sign":get_sign([apikeypair])}})
    print(send_string)
    #await websocket.send(send_string)
    #await websocket.send("{'event':'addChannel','channel':'ok_sub_spot_etc_btc_depth_3'}")

    #await websocket.send("{'event':'addChannel','channel':'ok_sub_spot_ltc_btc_depth_5'}")
    #await websocket.send("{'event':'removeChannel','channel':'ok_sub_spot_etc_btc_depth_5'}")
        #print("> {}".format(name))
    while True:
        #await websocket.send(name)
        await websocket.send(send_string)
        greeting = await websocket.recv()
        
        print("< {}".format(greeting))
        print(datetime.datetime.now())
        greet_json = json.loads(greeting)
        time.sleep(100)
        
        # if greet_json[0]['channel'] == 'ok_sub_spot_etc_btc_depth_5':
        #     await websocket.send("{'event':'removeChannel','channel':'ok_sub_spot_etc_btc_depth_5'}")
        #     await websocket.send("{'event':'addChannel','channel':'ok_sub_spot_ltc_btc_depth_5'}")
        # if greet_json[0]['channel'] == 'ok_sub_spot_ltc_btc_depth_5':
        #     await websocket.send("{'event':'removeChannel','channel':'ok_sub_spot_ltc_btc_depth_5'}")
        #     await websocket.send("{'event':'addChannel','channel':'ok_sub_spot_etc_btc_depth_5'}")

asyncio.get_event_loop().run_until_complete(hello())
asyncio.get_event_loop().run_forever()