from flask import Flask, render_template, request, flash

import redis

app = Flask(__name__)
app.secret_key = 'super secret key'


r = redis.Redis('192.168.99.100')

last_id = 0


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        global last_id
        req = request.form
        name = req["full_name"]
        post = req["data"]
        # print(name, post)

        last = r.get("last_id")
        # print("last_id", last)
        if last is None:
            last_id = 1
        else:
            last_id = int(last)
            last_id += 1
        r.set(f"news:name:{last_id}", name)
        r.set(f"news:post:{last_id}", post)
        r.set("last_id", last_id)
        r.lpush("post_id", last_id)
        flash("Successfully submitted the post please check it in all posts or recent posts", category='success')

    return render_template("home.html")


@app.route("/all")
def all_posts():
    post_ids = r.lrange("post_id", 0, -1)
    posts = dict()

    for post_id in post_ids:
        name = r.get(f'news:name:{post_id.decode("utf-8")}').decode("utf-8")
        post_data = r.get(f'news:post:{post_id.decode("utf-8")}').decode("utf-8")
        posts[name] = post_data

    return render_template("all.html", posts=posts)


@app.route("/latest")
def latest_posts():
    post_ids = r.lrange("post_id", 0, 2)
    posts = dict()

    for post_id in post_ids:
        name = r.get(f'news:name:{post_id.decode("utf-8")}').decode("utf-8")
        post_data = r.get(f'news:post:{post_id.decode("utf-8")}').decode("utf-8")
        posts[name] = post_data

    return render_template("latest.html", posts=posts)


if __name__ == "__main__":
    app.run()
