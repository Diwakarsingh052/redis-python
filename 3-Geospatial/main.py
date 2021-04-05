from flask import Flask, render_template, request, json, redirect

import redis

app = Flask(__name__)

r = redis.Redis('192.168.99.100')


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("map.html")


@app.route("/data")
def data():
    loc_name = r.get("last_loc_name")
    if loc_name is None:
        r.geoadd("points", '-104.985784', '39.728206', "parking")
        loc_name = "parking"
    all_loc = r.georadiusbymember(name='points', member=loc_name, radius=40000, unit='mi', withcoord=True)
    # print(all_loc)
    cord = dict()

    for loc in all_loc:
        # print(loc)
        name = loc[0].decode("utf-8")
        lat = loc[1][1]
        long = loc[1][0]

        cord[name] = {"lat": lat, "lng": long}

    return json.dumps(cord)


@app.route("/last")
def last_loc():
    return r.get("last_loc_name").decode("utf-8")
    

@app.route("/add-marker", methods=["POST"])
def add_marker():
    req = request.form
    location = req["lname"]
    latitude = req["latitude"]
    longitude = req["longitude"]

    print(location, latitude, location)

    r.geoadd("points", longitude, latitude, location)
    r.set("last_loc_name", location)

    return redirect("/")


if __name__ == "__main__":
    app.run()
