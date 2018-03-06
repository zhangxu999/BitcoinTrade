import gevent
from ws4py.client.geventclient import WebSocketClient
ws = WebSocketClient('wss://real.okex.com:10441/websocket', protocols=['http-only', 'chat'])
ws.connect()

def incoming():
    """
    Greenlet waiting for incoming messages
    until ``None`` is received, indicating we can
    leave the loop.
    """
    while True:
        print('incoming')
        m = ws.receive()
        if m is not None:
           print(m)
        else:
           break

def send_a_bunch():
    print('send_a_bunch')
    ws.send("{'event':'addChannel','channel':'ok_sub_spot_etc_btc_depth_5'}")
print('dsfffffff')
greenlets = [
    
    gevent.spawn(send_a_bunch),
    gevent.spawn(incoming),
]
print('')
gevent.joinall(greenlets)