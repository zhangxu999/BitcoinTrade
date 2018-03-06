import gevent
from gevent import socket
urls = ['www.baidu.com', 'www.qq.com', 'www.python.org']
jobs = [gevent.spawn(socket.gethostbyname, url) for url in urls]
gevent.joinall(jobs, timeout=2)
print([job.value for job in jobs])
