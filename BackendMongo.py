import os

from flask import Flask, render_template, request, json

from DatabaseAccess import DatabaseAccess
from Device import Device
from MongoDatabase import MongoDatabase
from TestResult import TestResult
from TestResultsContainer import TestResultsContainer

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('test.html')


@app.route("/list", methods=["GET"])
def list_tests():
    return render_template('list.html')


def add_dev(db):
    dev1 = Device("Test Device", "Test Description", "1.23.486_test")
    dev2 = Device("Test Device 2", "Test Description 2", "2.0")
    test1 = TestResult("Test", "Test", "Test", True)
    test2 = TestResult("Test2", "Test2", "Test2", False)
    trc = TestResultsContainer([test1, test2])
    js1 = dev1.get_json()
    js2 = trc.get_json()
    js_concat = {**js1, **js2}
    db.insert_data(js_concat)
    js1 = dev2.get_json()
    js2 = trc.get_json()
    js_concat = {**js1, **js2}
    db.insert_data(js_concat)


@app.route("/devices/<device_name>", methods=["GET"])
def get_device(device_name):
    db = MongoDatabase()
    add_dev(db)
    cursor = db.find_device_by_name(device_name)
    output = {}
    for document in cursor:
        output = {key: value for key, value in document.items() if key != "_id"}

    response_text = f"{output}".replace("'", '"')
    response = app.response_class(
        # response='{"device":{"name":"Test Device","description":"Test Description","version":"1.23.486_test"},
        # "tests":[["testsucccess","true"],["testfail","false"],["testunknown","null"]]}',
        response=response_text,
        status=200,
        mimetype='application/json'
    )

    return response


@app.route("/testing/<interface>/<test_group>", methods=["POST"])
def test(interface, test_group):
    capture = request.args.get('capture')
    if capture == "true":
        print("yes")

    response = app.response_class(
        response='{"error":"not implemented"}',
        status=404,
        mimetype='application/json'
    )
    return response


@app.route("/devices/", methods=["GET"])
def get_devices():
    print("get devices")
    db = MongoDatabase()
    add_dev(db)
    cursor = db.get_all_data()
    devices = []
    for document in cursor:
        devices.append({key: value for key, value in document.items() if key == "device"})

    # for all device in devices
    # output should be like this: '{"devices":["test_debug_device","test_debug_device2"]}')
    # use for loop to get all devices
    output = '{"devices":['
    for device in devices:
        output += f'"{device["device"]["name"]}",'
    output = output[:-1]
    output += ']}'
    print("Output: " + output)

    response_text = f"{output}".replace("'", '"')
    print("Response text: " + response_text)

    response = app.response_class(
        response=response_text,
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/interfaces/' , methods=["GET"])
def interfaces():
    # command is a linux command to get all wifi interfaces
    command = "iw dev | awk '$1==\"Interface\"{print $2}'"
    interfaces = os.popen(command).read().splitlines()
    output = '{"interfaces":['
    for interface in interfaces:
        output += f'"{interface}",'
    output = output[:-1]
    output += ']}'
    print("Output: " + output)
    return output


@app.route('/testing/', methods=["POST"])
def tests():
    # get interface and test group from request
    print("TESTING")
    data = request.get_json()
    print(data)
    request_data = data['request']
    print(request_data)
    data = request.form
    print(data)
    # ImmutableMultiDict([('{"request":{"ssid":"dsfdsfds","password":"dsf","interface":"none","name":"fdsfdf","description":"fdsfsd","mode":"client","tests":[{"name":"basic-test","capture":false},{"name":"amsdu-test","capture":false}]}}', '')])

    data = data.to_dict()
    for item in data:
        print(item)
    print(request.get_json())
    print(data)
    data = request.get_json(force=True)
    print(data)
    print("SOLO")

    name = data["name"]
    print(name)
    description = data["description"]
    mode = data["mode"]
    ssid = data["ssid"]
    password = data["password"]
    tests = data["tests"]
    #print("Interface: " + interface)
    print("Name: " + name)
    print("Description: " + description)
    print("Mode: " + mode)
    print("SSID: " + ssid)
    print(tests)

    print(data) #todo start tests
    response = app.response_class(
        response='{"error":"not implemented"}',
        status=404,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run()
