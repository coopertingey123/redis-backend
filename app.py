from flask import Flask, request, jsonify
from flask_redis import FlaskRedis

import random
import string


app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost:6379/0"
redis_client = FlaskRedis(app)


@app.route('/url/add', methods=["POST"])
def add_url():
    post_data = request.get_json()
    url = post_data.get("url")

    key = "".join([random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(20)])
    redis_client.set(key, url)

    return jsonify(key)

@app.route("/url/get/<key>", methods=["GET"])
def get_url(key):
    url = redis_client.get(key).decode("utf-8")
    print(url)

    return jsonify(url)

@app.route("/url/get", methods=["GET"])
def get_all_urls():
    all_keys = redis_client.keys("*")
    return jsonify([key.decode("utf-8") for key in all_keys])



if __name__ == "__main__":
    app.run(debug=True)



