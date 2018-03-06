import websocket
import json
try:
    import thread
except ImportError:
    import _thread as thread
import time
cnt = 0
def on_message(ws, message):
    #print(message)
    #ws.send("{'event':'addChannel','channel':'ok_sub_spot_etc_btc_depth_5'}")
    mess_json = json.loads(message)
    print(mess_json)
    # if mess_json[0]['channel'] == "ok_sub_spot_etc_btc_depth_5":
    #     if cnt>20:
    #         ws.send("{'event':'removeChannel','channel':'ok_sub_spot_etc_btc_depth_5'}")
    #print(mess_json[0]['data']['asks'][0],end=';')

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        #ws.send("{'event':'addChannel','channel':'ok_sub_spot_etc_btc_depth_5'}")

        ws.send("{'event':'addChannel','channel':'ok_sub_spot_bch_btc_ticker'}")
        #time.sleep(1)
        #ws.close()
        #print("thread terminating...")
    for i in ['etc_btc']:
        thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://real.okex.com:10441/websocket",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
