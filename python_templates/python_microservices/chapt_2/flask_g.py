from flask import Flask, jsonify, g, request, request_finished
from flask.signals import signals_available

if not signals_available:
    raise RuntimeError("pip install blinker")

app = Flask(__name__)

def finished(sender, response, **extra):
    print("About to send a Response")
    print(response.data)

request_finished.connect(finished)

@app.route("/")
def api():
    return jsonify({"Hello": "World"})



@app.before_request
def authenticate():
    if request.authorization:
        g.user = request.authorization["username"]
    else:
        g.user = "Anonymous"


@app.route("/api")
def my_microservice():
    return jsonify({"Hello": g.user})

if __name__ == "__main__":
    app.run()