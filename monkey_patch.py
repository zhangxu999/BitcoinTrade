import websocket
import time
import json
from gevent import monkey; monkey.patch_all()
import gevent
cnt = 0
def on_message(ws, message):
    global cnt
    cnt+=1
    string = json.loads(message)
    ts = string[0]['data']['timestamp']
    bids1 = string[0]['data']['bids'][0][0]
    asks1 = string[0]['data']['asks'][0][0]
    now = int(time.time()*1000)
    #if cnt>20:
        #ws.send("{'event':'removeChannel','channel':'ok_sub_spot_ace_eth_depth_5'}")

    print(ts,now-int(ts),string[0]['channel'][12:19],'bids1:',bids1,'asks1',asks1)
    #print(string[0]['channel'][12:],end=';')
    #last = now

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")
    #ws.connect("wss://real.okex.com:10441/websocket")    
    

def on_open(ws):
    ws.send("{'event':'addChannel','channel':'ok_sub_spot_etc_btc_depth_5'}")
        #time.sleep(1)
        #ws.close()
        #print("thread terminating...")
    #thread.start_new_thread(run, ())
def on_ping(ws,ping):
    print('ping!',pong)
def on_pong(ws,pong):
    print('pong!',pong)

def on_open2(ws):
    ws.send("{'event':'addChannel','channel':'ok_sub_spot_eth_btc_depth_5'}")
        #time.sleep(1)
        #ws.close()
        #print("thread terminating...")
    #thread.start_new_thread(run, ())
def on_open3(ws):
    #ws.send("{'event':'addChannel','channel':'ok_sub_spot_dash_eth_depth_5'}")
    ws.send("{'event':'addChannel','channel':'ok_sub_spot_ace_eth_depth_5'}")
    ws.send("{'event':'addChannel','channel':'ok_sub_spot_eth_btc_depth_5'}")
if __name__ == "__main__":
    #websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://real.okex.com:10441/websocket",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close,on_open = on_open,on_ping=on_ping,on_pong=on_pong)
    #ws.on_open = on_open
    ws2 = websocket.WebSocketApp("wss://real.okex.com:10441/websocket",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close,on_open = on_open2,on_ping=on_ping,on_pong=on_pong)
    ws3 = websocket.WebSocketApp("wss://real.okex.com:10441/websocket",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close,on_open = on_open3,on_ping=on_ping,on_pong=on_pong)
    
def addnewws():
    ws3 = websocket.WebSocketApp("wss://real.okex.com:10441/websocket",
                        on_message = on_message,
                        on_error = on_error,
                        on_close = on_close,on_open = on_open3,on_ping=on_ping,on_pong=on_pong)
    return ws3


def funcws1():
    ws.run_forever(ping_interval=5)
def funcws2():
    ws2.run_forever(ping_interval=5)

def deamon1():
    #global ws3
    while True:
        print('in deamon1::')
        print([j.dead for j in jobs])
        print([id(j) for j in jobs])
        for i in range(len(jobs)):

            if jobs[i].dead:
                print('restart new:')
                ws3 = addnewws()
                greenl = gevent.spawn(ws3.run_forever)
                jobs[i] = greenl
                greenl.start()
                greenl.join()
                print(greenl.dead)
        gevent.sleep(1)



#gevent.spawn(ws.run_forever),gevent.spawn(ws2.run_forever),gevent.spawn(ws3.run_forever),,gevent.spawn(ws.run_forever)
jobs = [gevent.spawn(ws2.run_forever)]
gevent.joinall(jobs)