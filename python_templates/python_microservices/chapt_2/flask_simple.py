from flask import Flask, jsonify, request, url_for, make_response, redirect
from werkzeug.routing import BaseConverter, ValidationError
import yaml 

_USERS = {"1": "Tarek", "2": "Freya"}
_IDS = {val: id for id, val in _USERS.items()} # what a beautiful list comprehesion / object restructing example




class RegisteredUser(BaseConverter):
    def to_python(self, value):
        if value in _USERS:
            return _USERS[value]
        raise ValidationError
    def to_url(self, value):
        return _IDS[value]


app = Flask(__name__)

## example of custom implementaion of a BaseConverter inherited class
app.url_map.converters["registered"] = RegisteredUser

def yamlify(data, status=200, headers=None):
    _headers = { "Content-Type": "application/x-yaml"}
    if headers is not None:
        _headers.update(headers)
    return yaml.safe_dump(data), status, _headers


@app.route("/yaml")
def yamlroute():
    return yamlify([{"Hello": ["Uaomse"]}, "Yaml", "World"])



@app.route("/", methods=["GET"])
@app.route("/home",  methods=["GET"])
@app.route("/index",  methods=["GET"])
def home():
    print("The raw authorization header")
    print(request.environ["HTTP_AUTHORIZATION"])
    print("Flask's Authorization header")
    print(request.authorization)
    return make_response("Bunda", 200, {"Content-Type": "plain/text"})


@app.route("/auth")
def auth():
    print("The raw authorization header")
    print(request.environ["HTTP_AUTHORIZATION"])
    print("Flask's Authorization header")
    print(request.authorization)
    return ""

@app.route("/login",  methods=["GET"])
def login():
    # nice case display that url_for() returns the route to func/ value it returns
    return redirect(url_for("home"))


@app.route("/api")
def my_microservice():
    print(request) 
    print("\n\n",request.environ) 
    response = jsonify({'Hello': 'World!'}) 
    print(response) 
    print(response.data) 
    return response 

# introducing variable within carrots
@app.route("/api/person/<person_id>")
def person(person_id):
    response = jsonify({"Hello": person_id})
    return response


@app.route("/api/user/<registered:name>")
def user(name):
    reponse = jsonify({"Hello": name})
    print(url_for("user", name="Tarek"))
    return reponse

#

if __name__ == "__main__":
    print(app.url_map)
    
    app.run()
  
