import websocket
import time
import math
import json
cnt = 0
last=0
begin = 0
ping_l = []
pong_l = []
time_list=[]

import datetime
import time
import json
import hashlib

apikeypair= ("api_key","eca729c5-cbf5-4333-8476-56bd0bb1009f")
apikey = "eca729c5-cbf5-4333-8476-56bd0bb1009f"
order_numbers = []

def get_sign(params):
    sign_str = '&'.join([k+'='+v for k,v in sorted(params)])+'&secret_key=346BD975D145C1686705BB07411ADEFC'
    #print(sign_str)
    return hashlib.md5(sign_str.encode('utf8')).hexdigest().upper()

class finite_machine(object):
    """docstring for finite_machine"""
    def __init__(self):
        self.ws = websocket.WebSocketApp("wss://real.okex.com:10441/websocket",
                                  on_message = self.on_message,
                                  on_error = self.on_error,
                                  on_close = self.on_close,on_ping=self.on_ping,on_pong=self.on_pong,on_open = self.on_open)
        
        self.status = 0
        self.curr_price = ''
        self.curr_amount = ''
        self.a = 0
        self.b = 0

        self.log_file = open('order.log','a')

        self.a_symbol = 'etc'
        self.b_symbol = 'eth'
        self.symbol = self.a_symbol+'_'+self.b_symbol
        self.depth_channel = "ok_sub_spot_{0}_depth_5".format(self.symbol)
        self.order_channel = "ok_sub_spot_{0}_order".format(self.symbol)

    def run_forever(self):
        self.ws.run_forever(ping_interval=60)


    def _query_account(self):
        query_string = '{"channel": "ok_spot_userinfo", "parameters": {"sign": "65A16B64192413F1F44227A73E8ADADF", "api_key": "eca729c5-cbf5-4333-8476-56bd0bb1009f"}, "event": "addChannel"}'
        self.ws.send(query_string)
        self.status = 1
    def _check_account_value(self,message):
        #print(message)
        if message[0]['data']['result'] == True:
            self.a = float(message[0]['data']['info']['funds']['free'][self.a_symbol])
            self.b = float(message[0]['data']['info']['funds']['free'][self.b_symbol])
            self.status = 2
        else:
            self.status == 0
    def order(self,message):
        ts = int(message[0]['data']['timestamp'])
        now = int(time.time()*1000)
        if now-ts>500:
            return
        self.order_type,self.depth_type=order_type,depth_type = \
        ('sell','asks') if (self.a*float(message[0]['data']['asks'][0][0]))>self.b else ('buy','bids')
        price_index = -1 if self.depth_type=='asks' else 0
        self.curr_price = price = float(message[0]['data'][self.depth_type][price_index][0])
        self.curr_price = price = price if self.order_type=='buy' else price
        price_com_result = (price >float(message[0]['data']['bids'][0][0]))  if self.depth_type == 'asks' else (price <float(message[0]['data']['bids'][0][-1]))
        if not price_com_result:
            return 
        self.curr_amount= amount = math.floor((self.b/price)*1e8)/1e8 if order_type=='buy' else self.a
        #self.curr_amount= amount = str(min(amount,0.05))
        sign_pamams = [apikeypair,('symbol',self.symbol),('type',order_type),('price',str(price)),('amount',str(amount))]
        #print(message[0]['data']['bids'])
        #print(message[0]['data']['asks'])
        print(self.order_type,self.depth_type,self.curr_price,self.curr_amount)
        order_data = {'event':'addChannel','channel':'ok_spot_order',
        'parameters':{'api_key':"eca729c5-cbf5-4333-8476-56bd0bb1009f",
        'sign':get_sign(sign_pamams),'symbol':self.symbol,'type':order_type,'price':str(price),
        'amount':str(amount)}}
        
        #print(json.dumps(order_data))
        print('--------')
        now = int(time.time()*1000)
        if now-ts>500:
            return
        self.ws.send(json.dumps(order_data))
        print(datetime.datetime.now(),json.dumps(order_data),file=self.log_file,flush=True)
        self.status = 3

    def check_order_send_result(self,message):

        if message[0]['data']['result'] == True:
            self.order_id = message[0]['data']['order_id']
            self.status = 4
            order_numbers.append(message)
            print(datetime.datetime.now(),message,file=self.log_file,flush=True)
            
        else:
            self.status = 0
            print('order wrong')
            exit()
    def check_order_excute_result(self,message):
        
        stus = message[0]['data']['status']
        if  stus == 2:
            #self.status = 0
            print(datetime.datetime.now(),message,file=self.log_file,flush=True)
            self.status = 0
        elif stus == 1:
            print(datetime.datetime.now(),message,file=self.log_file,flush=True)
    def check_should_cancel(self,message):
        price_index = 0 if self.depth_type == 'asks' else -1
        comapre_price = float(message[0]['data'][self.depth_type][price_index][0])
        com_result = (self.curr_price>comapre_price) if (self.depth_type=='asks') else (self.curr_price<comapre_price)
        #print('curr_price:',self.curr_price,'comapre_price',comapre_price,com_result,self.depth_type)
        #print('asks:',[x for x,y in message[0]['data']['asks']])
        #print('bids:',[x for x,y in message[0]['data']['bids']])
        #print('---------------check_should_cancel--------------')
        if com_result:
            
            cancel_data = \
                {
                    'event':'addChannel','channel':'ok_spot_cancel_order',
                    'parameters':{'api_key':apikey,
                        'sign':get_sign([apikeypair,('symbol',self.symbol),('order_id',str(self.order_id))]),
                        'symbol':self.symbol,
                        'order_id':self.order_id
                    }
                }
            self.ws.send(json.dumps(cancel_data))
            print('cancel:',datetime.datetime.now(),com_result,json.dumps(cancel_data),message,file=self.log_file,flush=True)
            self.status = 5
    def check_cancel_result(self,message):
        if message[0]['data']['result'] == True:
            #self.status = 0
            self.status = 0
            print(message,file=self.log_file,flush=True)
        else:
            pass
            #print(message,file=self.log_file,flush=True)




    def check_message(self,message=None):
        channel = message[0].get('channel')
        print(time.time(),'status:',self.status,channel)
        #print(message)
        if self.status == -1:
            print('完成一单，停车观察')
            self.ws.close()
            exit()
        if self.status == -2:
            print('撤销一单，停车观察')
            self.ws.close()
            exit()
        if self.status == 0:
            self._query_account()
        elif self.status == 1:
            if channel == 'ok_spot_userinfo':
                self._check_account_value(message)
        elif self.status == 2:
            #print(message)
            if channel == self.depth_channel:
                self.order(message)
        elif self.status == 3:
            #print(message[0]['data']['bids'])
            #print(message[0]['data']['asks'])

            if channel == "ok_spot_order":
                self.check_order_send_result(message)
        elif self.status == 4:
            if channel == self.order_channel:
                self.check_order_excute_result(message)
            elif channel == self.depth_channel:
                self.check_should_cancel(message)
        elif self.status == 5:
            if channel == 'ok_spot_cancel_order':
                self.check_cancel_result(message)

        




    def on_message(self,ws, message):
        #global cnt 
        #global last
        #cnt+=1
        string = json.loads(message)
        #print(string)
        # ts = string[0]['data']['timestamp']
        # bids = string[0]['data']['bids'][0:5]
        # asks = string[0]['data']['asks'][0:5]
        # now = int(time.time()*1000)


        #print(ts,now-int(ts),now-last)
        #print('bids:',bids)
        #print('asks',asks)
        #print('--------------')
        #time_list.append((ts,now))
        self.check_message(string)

        

    def on_error(self,ws, error):
        print(error.with_traceback(None))

    def on_close(self,ws):
        now = time.time()
        self.log_file.flush()
        self.log_file.close()

        print('time:',now-begin)
        # print('cnt:',len(time_list))
        # print('delay_avg:',sum([y-x for x,y in time_list])/(len(time_list)+1e-8))
        # xxx,yyy = time_list.copy(),time_list.copy()
        # xxx.pop(0);yyy.pop(-1)
        # zzz = [x-y for x,y in zip([a for a,b in xxx],[m for m,n in yyy])]
        # print('send_freq:',sum(zzz)/(len(zzz)+1e-8))
        print(ping_l,'pingpong',pong_l)
        print("### closed ###")
    def on_ping(self,ws,ping):
        #print('ping!',pong)
        ping_l.append('ping')
    def on_pong(self,ws,pong):
        #print('pong!',pong)
        pong_l.append('pong')

    def on_open(self,ws):
        global begin
        begin = time.time()
        ws.send("{'event':'addChannel','channel':'ok_sub_spot_etc_eth_depth_5'}")
        depth_string = json.dumps({"event":"addChannel","channel":self.depth_channel})
        ws.send(depth_string)
        login_string = '{"event": "login","parameters": {"sign": "65A16B64192413F1F44227A73E8ADADF", "api_key": "eca729c5-cbf5-4333-8476-56bd0bb1009f"}}'
        ws.send(login_string)

        #time.sleep(1)
        #ws.close()
        #print("thread terminating...")
    #thread.start_new_thread(run, ())
    #websocket.enableTrace(True)

if __name__ == '__main__':
    fm = finite_machine()
    fm.run_forever()