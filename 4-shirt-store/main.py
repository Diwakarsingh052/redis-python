import redis

r = redis.Redis('192.168.99.100')


def scan_keys(pattern, pos: int = 0) -> list:
    shirts = []
    while True:
        pos, val = r.scan(cursor=pos, match=pattern)
        shirts = shirts + val
        if pos == 0:
            break

    return shirts


def buy_items(r: redis.Redis, itemid) -> None:
    pipe = r.pipeline()

    # while True:
    nleft: bytes = r.hget(itemid, "quantity")
    if nleft > b"0":
        pipe.hincrby(itemid, "quantity", -1)
        pipe.hincrby(itemid, "nPurchased", 1)
        pipe.execute()

    else:
        print("Sorry ", itemid, "out of stock")

    return None


shirts = scan_keys("shirt:*")
# print(shirts)
buy_items(r, shirts[0])
