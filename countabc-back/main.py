import argparse
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response
from functools import wraps
from models import RedBase
import re
from middleware import RedisDB, generate_random_key

import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
db: RedisDB = None
username = password = host = port = db_number = ""


def jsonp(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # Check if a callback function is specified in the request
        callback = request.args.get('callback')

        # Call the original route function and get the response
        response = func(*args, **kwargs)

        # If a callback is specified, wrap the bytes response with the callback function
        if callback:
            response_data = response.data.decode('utf-8')
            jsonp_response = f"{callback}({response_data})"
            response = make_response(jsonp_response)
            response.headers['Content-Type'] = 'application/javascript'

        return response

    return decorated_function


def check_and_modify_key(func):

    @wraps(func)
    def decorated_function(*args, **kwargs):
        key = kwargs.get('key')
        if len(key) < 3:
            key = f":{key}:"

        kwargs['key'] = key

        return func(*args, **kwargs)

    return decorated_function


@app.before_request
def hit():
    db.hit_count()


@app.after_request
def add_x_key_header(response):
    # Retrieve the modified 'key' from the route parameters
    response.headers["Access-Control-Allow-Origin"] = os.environ.get(
        "Access-Control-Allow-Origin", "*")
    response.headers["Access-Control-Allow-Headers"] = os.environ.get(
        "Access-Control-Allow-Headers", "*")
    response.headers["Access-Control-Allow-Methods"] = os.environ.get(
        "Access-Control-Allow-Methods", "*")
    # response.headers["Content-Type"] = os.environ.get("Content-Type",
    #                                                   "application/json")
    if response.headers.get('X-Key'):

        return response
    # print(re)
    try:
        key = request.view_args.get('key', "FIELD")
    except:
        key = "shubh"
    if len(key) < 3:
        key = f":{key}:"
    # Concatenate 'namespace' and modified 'key' to form the 'X-Key' header value
    try:
        namespace = request.view_args.get('namespace', "HOST")
    except:
        namespace = "default"
    # namespace = request.view_args.get('namespace', 'default')
    x_key_value = f"{namespace}:{key}"

    response.headers['X-Key'] = x_key_value
    return response


@app.route("/")
def home():
    return redirect("https://documenter.getpostman.com/view/33991252/2sA35MxJR8")


@app.route("/get/<key>")
@app.route("/get/<namespace>/<key>")
@check_and_modify_key
@jsonp
def get_key(key, namespace="default"):
    status, resp = db.get_value(f"{namespace}:{key}")
    response = make_response(jsonify(resp), status)
    response.headers['X-Key'] = f"{namespace}:{key}"
    response.headers["Content-Type"] = os.environ.get("Content-Type",
                                                      "application/json")
    return response


@app.route("/set/<key>")
@app.route("/set/<namespace>/<key>")
@check_and_modify_key
@jsonp
def set_key(key, namespace="default"):
    value = request.args.get("value")
    if not value:
        return jsonify({"Error": "Value not provided"}), 400
    status, resp = db.set_value(f"{namespace}:{key}", value)
    response = make_response(jsonify(resp), status)
    response.headers['X-Key'] = f"{namespace}:{key}"
    response.headers["Content-Type"] = os.environ.get("Content-Type",
                                                      "application/json")
    return response


@app.route("/update/<key>")
@app.route("/update/<namespace>/<key>")
@check_and_modify_key
@jsonp
def update_key(key, namespace="default"):
    amount = request.args.get("amount")
    if not amount or not amount.lstrip("-").isdigit():
        return jsonify({"Error": "Amount not provided"}), 400
    amount = int(amount)
    status, resp = db.update_value(f"{namespace}:{key}", int(amount))
    response = make_response(jsonify(resp), status)
    response.headers['X-Key'] = f"{namespace}:{key}"
    response.headers["Content-Type"] = os.environ.get("Content-Type",
                                                      "application/json")
    return response


@app.route("/hit/<key>")
@app.route("/hit/<namespace>/<key>")
@check_and_modify_key
@jsonp
def hit_key(key, namespace="default"):
    # print(key)
    if not re.match(r"^[A-Za-z0-9_\-.]{3,64}$", key) or len(key) > 64:
        key = generate_random_key()
        print(key)
    status, resp = db.hit_value(f"{namespace}:{key}")

    response = make_response(jsonify(resp), status)
    response.headers['X-Key'] = f"{namespace}:{key}"
    response.headers["Content-Type"] = os.environ.get("Content-Type",
                                                      "application/json")
    return response


@app.route("/create/")
@jsonp
def create_key():
    name = request.args.get("key")
    # pass_
    if not name or not re.match(r"^[A-Za-z0-9_\-.]{3,64}$",
                                name) or len(name) > 64:
        # generate a random key which is unique and based on current datetime
        name = generate_random_key()
    if len(name) < 3:
        name = f":{name}:"
    a = RedBase()
    namespace = request.args.get("namespace", "default")
    # if not()
    if not re.match(r"^[A-Za-z0-9_\-.]{3,64}$", namespace):
        namespace = "default"

    enable_reset = request.args.get("enable_reset", a.enable_reset)
    update_lowerbound = request.args.get("update_lowerbound",
                                         a.update_lowerbound)
    update_upperbound = request.args.get("update_upperbound",
                                         a.update_upperbound)
    value = request.args.get("value", a.value)

    if not str(enable_reset).lstrip("-").isdigit():
        enable_reset = a.enable_reset
    if not str(update_lowerbound).lstrip("-").isdigit():
        update_lowerbound = a.update_lowerbound
    if not str(update_upperbound).lstrip("-").isdigit():
        update_upperbound = a.update_upperbound
    if not str(value).lstrip("-").isdigit():
        value = a.value

    # print(f"namespace:{namespace},name:{name}")
    new_mapping = {
        "namespace": namespace,
        "enable_reset": enable_reset,
        "update_lowerbound": update_lowerbound,
        "update_upperbound": update_upperbound,
        "value": value
    }
    status, resp = db.new_key(f"{namespace}:{name}", new_mapping)
    resp["key"] = f"{namespace}:{name}"
    response = make_response(jsonify(resp), status)
    response.headers['X-Key'] = f"{namespace}:{name}"
    response.headers["Content-Type"] = os.environ.get("Content-Type",
                                                      "application/json")
    return response


@app.route("/info/<key>")
@app.route("/info/<namespace>/<key>")
@check_and_modify_key
@jsonp
def get_info(key, namespace="default"):
    status, resp = db.get_info(f"{namespace}:{key}")

    response = make_response(jsonify(resp), status)
    response.headers["Content-Type"] = os.environ.get("Content-Type",
                                                      "application/json")
    return response


@app.route("/stats")
@jsonp
def get_stats():
    status, resp = db.get_stats()
    response = make_response(jsonify(resp), status)
    response.headers['X-Key'] = "stats"
    response.headers["Content-Type"] = os.environ.get("Content-Type",
                                                      "application/json")
    return response


@app.route("/namespace")
@app.route("/namespace/<namespace>")
@jsonp
def get_namespace(namespace="default"):
    status, resp = db.get_namespace(namespace)
    response = make_response(jsonify(resp), status)
    response.headers['X-Key'] = f"{namespace}:*"
    response.headers["Content-Type"] = os.environ.get("Content-Type",
                                                      "application/json")
    return response


@app.route('/logs/shubh/mittal/')
def show_logs():
    try:
        with open('access.log', 'r') as log_file:
            logs = log_file.readlines()
        return render_template('logs.html', logs=logs[::-1])
    except FileNotFoundError:
        return 'Log file not found'


with app.app_context():
    username = os.environ.get("r_username", "default")
    password = os.environ.get("r_password", "Shubh@2003")
    host = os.environ.get(
        "r_host", "redis-19606.c301.ap-south-1-1.ec2.cloud.redislabs.com")
    port = os.environ.get("r_port", 19606)
    if not username or not password or not host or not port:
        print("Please Setup the Environment Variables")
        exit(1)
    db_number = os.environ.get("db", 0)
    # env_fetch
    db = RedisDB(username=username,
                 password=password,
                 host=host,
                 port=port,
                 db=db_number)
    db.connect()
    # db.setup()
# Argparse for server Setup In Command Line


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CountABC Server")
    parser.add_argument("--setup", help="Setup the Server",
                        action="store_true")
    if parser.parse_args().setup:
        print("Setting Up the Database!")
        db.setup()
        print("Setup Complete!")
    app.run()
