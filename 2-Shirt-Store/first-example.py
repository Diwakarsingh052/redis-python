import redis

r = redis.Redis('192.168.99.100')
r.set("fname","Diwakar")
name_bytes = r.get("fname")

name = name_bytes.decode('utf-8')
msg = f"My name is {name}"

# print(type(name))
print(msg)