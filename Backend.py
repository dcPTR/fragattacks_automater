from flask import Flask, render_template, request, json, send_from_directory

from DatabaseAccess import DatabaseAccess
from Device import Device
from TestResultsContainer import TestResultsContainer
from TestsFileImporter import TestsFileImporter
from os import getcwd, path

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('test.html')


@app.route("/list", methods=["GET"])
def list_tests():
    trc = TestResultsContainer(TestsFileImporter().get_test_results())
    db = DatabaseAccess()
    db.create_database()
    device = Device("test device name", "test description", "1.0.0")
    id1 = db.export_device(device)
    device = Device("test device name 2", "test description 2", "1.1.0")
    id2 = db.export_device(device)

    db.export_test_results(trc)
    dbcs = db.import_test_results()
    db.print_test_results()
    return render_template('list.html', tests=dbcs)

# route for /devices/{device_name}
@app.route("/devices/<device_name>", methods=["GET"])
def get_device(device_name):
    db = DatabaseAccess()
    #device = db.get_device(device_name)
    print(device_name)
    # it should return json with device info
    example_results = TestsFileImporter().get_test_results()
    trc = TestResultsContainer(example_results)

    db = DatabaseAccess()
    db.create_database()
    device = Device("test device name", "test description", "1.0.0")
    print(device)
    id1 = db.export_device(device)
    device = Device("test device name 2", "test description 2", "1.1.0")
    id2 = db.export_device(device)
    db.print_devices()

    db.export_test_results(trc, id1, id2)

    db.print_test_results()
    dbcs = db.import_test_results()
    db.print_test_results()
    response_text = f"{{{device}, {dbcs[0]}}}"
    response_object = json.load(response_text)

    if "tests" in response_object:
        for test in response_object["tests"]:
            # if test has 3 values, 3rd value should be name of the capture dump file
            # format: ["test name", "test status", <"dump file name">]
            if len(test >= 3): 
                if not path.exists(getcwd() + "/captures/" + test[2]):
                    #if file can't be find on the server, don't send it to the user
                    test.pop(2)

    response = app.response_class(
        # response='{"device":{"name":"Test Device","description":"Test Description","version":"1.23.486_test"},"tests":[["testsucccess","true"],["testfail","false"],["testunknown","null"]]}',
        response=response_text,
        status=200,
        mimetype='application/json'
    )
    return response

# route for /captures/{device_name}
@app.route("/captures/<file_name>", methods=["GET"])
def get_capture_file(file_name):
    return send_from_directory(
        getcwd()+"/captures", file_name, as_attachment=True
    )

# route for testing/{interface}/{test_group} in method POST
#it should check if there is query parameter "capture" with value "true"
# if there is it shpuld print yes
@app.route("/testing/<interface>/<test_group>", methods=["POST"])
def test(interface, test_group):
    capture = request.args.get('capture')
    if capture == "true":
        print("yes")
    return "OK"


@app.route("/devices/", methods=["GET"])
def get_devices():
    pass


if __name__ == '__main__':
    app.run()
