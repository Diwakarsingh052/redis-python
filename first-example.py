import redis

r = redis.Redis('192.168.99.100')
r.set("name", "Diwakar")
name = r.get("name")
print(name)
