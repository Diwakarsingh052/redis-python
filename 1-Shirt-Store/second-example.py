import redis
import datetime

r = redis.Redis('192.168.99.100')

today = datetime.date.today()
stoday = today.isoformat()  # Python 3.7+
visitors = {"dan", "jon", "alex"}
r.sadd(stoday, *visitors)
values = r.smembers(stoday)
print(values)

card = r.scard(today.isoformat())
print(card)
