import requests,json,time,datetime
from requests import Session,Request
domain = 'https://api.huobipro.com'
url_kline='/market/history/kline'
url_ticker = '/market/detail/merged'
url_account = '/v1/account/accounts'
params = {'symbol':'bchbtc'}
header = {"user agent":"User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36"}
count = 0
for i in range(350):
    s = Session()
    req = Request('GET', domain+url_ticker, headers=header,)
    try:
        prepped = s.prepare_request(req)
        resp = s.send(prepped).text
        resp = json.loads(resp)
        dts = datetime.datetime.utcfromtimestamp(resp['ts']//1000)
        print(count,dts,resp['tick']['open'],resp['tick']['close'])
        count+=1
    except Exception as e:
        #logger.error('通知接口HTTP调用失败,url:'+domain+url_ticker, exc_info=True)
        print(domain+url_ticker)
        raise e
    finally:
        s.close()
    time.sleep(1)