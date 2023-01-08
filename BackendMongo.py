import os

from flask import Flask, render_template, request, json

from Device import Device
from MongoDatabase import MongoDatabase
from TestResult import TestResult
from TestResultsContainer import TestResultsContainer
from Automater import Automater
from ClientConfiguration import replace_conf_file

app = Flask(__name__)

db = MongoDatabase()


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/list", methods=["GET"])
def list_lists():
    return render_template('list.html')


@app.route("/test", methods=["GET"])
def list_tests():
    return render_template('test.html')


def add_dev():
    global db
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


@app.route("/devices/", methods=["GET"])
def get_devices():
    db = MongoDatabase()

    cursor = db.get_all_data()
    devices = []
    for document in cursor:
        devices.append({key: value for key, value in document.items() if key == "device"})

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


@app.route('/interfaces/', methods=["GET"])
def interfaces():
    command = "iw dev | awk '$1==\"Interface\"{print $2}'"
    interfaces = os.popen(command).read().splitlines()
    output = '{"interfaces":['
    for interface in interfaces:
        output += f'"{interface}",'
    output = output[:-1]
    output += ']}'
    return output


@app.route('/testing/', methods=["POST"])
def tests():
    global db
    data = json.loads(next(iter(request.form)))
    request_data = data.get("request")

    name = request_data["name"]
    description = request_data["description"]
    version = request_data["version"]
    mode = request_data["mode"]
    ssid = request_data["ssid"]
    password = request_data["password"]
    interface = request_data["interface"]
    tests = request_data["tests"]
    print("Interface: " + interface)
    print("Name: " + name)
    print("Description: " + description)
    print("Mode: " + mode)
    print("SSID: " + ssid)
    print("Password: " + password)
    replace_conf_file(ssid, password)
    dev = Device(name=name, description=description, software_version=version)
    dev_json = dev.get_json()
    results_container = []

    for test in tests:
        test_group = test["name"]
        test_capture = test["capture"]
        # print("Test group: ", test_group)
        # print("Test capture: ", test_capture)
        auto = Automater(capture=test_capture, interface=interface, group=test_group)
        results = auto.run()
        results_container.append(results)
    print("Results: ", results_container)
    results = []
    for result in results_container:
        for item in result:
            results.append(item)
    print("Results: ", results)
    trc = TestResultsContainer(results)
    tests_json = trc.get_json()
    js_concat = {**dev_json, **tests_json}
    print(js_concat)
    db.insert_data(js_concat)
        # print("Test: ", test)
    # print(tests)

    response = app.response_class(
        response='{"status":"success"}',
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run()
