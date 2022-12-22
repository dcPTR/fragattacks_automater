from flask import Flask, render_template

from DatabaseAccess import DatabaseAccess
from TestResultsContainer import TestResultsContainer
from TestsFileImporter import TestsFileImporter

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('test.html')


@app.route("/list", methods=["GET"])
def list_tests():
    trc = TestResultsContainer(TestsFileImporter().get_test_results())
    db = DatabaseAccess()
    db.create_database()
    db.export_test_results(trc)
    dbcs = db.import_test_results()
    db.print_test_results()
    return render_template('list.html', tests=dbcs)


if __name__ == '__main__':
    app.run()
