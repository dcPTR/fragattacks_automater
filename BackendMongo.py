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
    db = MongoDatabase()
    add_dev(db)
    cursor = db.get_all_data()
    output = []
    for document in cursor:
        output.append({key: value for key, value in document.items() if key == "device"})
    response_text = f"{output}".replace("'", '"')
    response = app.response_class(
        response=response_text,
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/interfaces/' , methods=["GET"])
def interfaces():
    return '{"interfaces":["interfaceA","interfaceB"]}' #todo


@app.route('/testing/', methods=["POST"])
def tests():
    data = request.form
    print(data) #todo start tests
    response = app.response_class(
        response='{"error":"not implemented"}',
        status=404,
        mimetype='application/json'
    )
    return response

if __name__ == '__main__':
    app.run()
