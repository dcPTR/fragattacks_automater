import os
import threading

from flask import Flask, render_template, request, json, send_from_directory

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


@app.route("/list_all", methods=["GET"])
def list_all():
    return render_template('list_all.html')


@app.route("/test", methods=["GET"])
def list_tests():
    return render_template('test.html')


@app.route("/guide", methods=["GET"])
def guide():
    return render_template('guide.html')


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

    response_object = json.loads(response_text)

    if "tests" in response_object:
        for test in response_object["tests"]:
            # if test has 3 values, 3rd value should be name of the capture dump file
            # format: ["test name", "test status", <"dump file name">]
            if len(test) >= 3:

                if not os.path.exists(f"{os.getcwd()}/captures/{test[2]}.pcap"):
                    # if file can't be find on the server, don't send it to the user
                    print("File not found")
                    test.pop(2)
    response_text = json.dumps(response_object)

    response = app.response_class(
        response=response_text,
        status=200,
        mimetype='application/json'
    )

    return response


@app.route("/all_devices/", methods=["GET"])
def get_all_devices():
    cursor = db.get_all_data()

    all_dev = []
    output = {}
    for document in cursor:
        output = {key: value for key, value in document.items() if key != "_id"}
        all_dev.append(output)

    response_text = f"{all_dev}".replace("'", '"')

    response = app.response_class(
        response=response_text,
        status=200,
        mimetype='application/json'
    )

    # @app.route("/all_devices/", methods=["GET"])
    # def get_all_devices():
    #     cursor = db.get_all_data()
    #     output = {}
    #     for document in cursor:
    #         output = {key: value for key, value in document.items() if key != "_id"}
    #         print(output)
    #
    #     response_text = f"{output}".replace("'", '"')
    #
    #     response_object = json.loads(response_text)
    #
    #     print(response_object)
    #     print(type(response_object))
    #     for device in response_object:
    #
    #         print(type(device))
    #         device_object = device
    #         print(type(device_object))
    #         print("Device: ", device_object)
    #         if "tests" in device:
    #             for test in device["tests"]:
    #                 # if test has 3 values, 3rd value should be name of the capture dump file
    #                 # format: ["test name", "test status", <"dump file name">]
    #                 if len(test) >= 3:
    #                     if not os.path.exists(os.getcwd() + "/captures/" + test[2]):
    #                         # if file can't be find on the server, don't send it to the user
    #                         test.pop(2)
    #         device = json.dumps(device_object)
    #
    #     response = app.response_class(
    #         # response='{"device":{"name":"Test Device","description":"Test Description","version":"1.23.486_test"},
    #         # "tests":[["testsucccess","true"],["testfail","false"],["testunknown","null"]]}',
    #         response=response_text,
    #         status=200,
    #         mimetype='application/json'
    #     )

    return response


# route for /captures/{device_name}
@app.route("/captures/<file_name>", methods=["GET"])
def get_capture_file(file_name):
    return send_from_directory(
        f"{os.getcwd()}/captures{file_name}", as_attachment=True
    )


@app.route("/devices/", methods=["GET"])
def get_devices():
    global db
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


def test_thread_func(request_form):
    print("Starting test thread")
    print(request_form)
    global db
    data = json.loads(request_form)
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
        print(test)
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


@app.route('/testing/', methods=["POST"])
def tests():
    thread = threading.Thread(target=test_thread_func, args=request.form, daemon=True)
    thread.start()

    response = app.response_class(
        response='{"status":"success"}',
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run()
