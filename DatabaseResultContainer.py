import pyodbc

from TestResult import TestResult
from TestsFileImporter import TestsFileImporter


class DatabaseResultContainer:
    def __init__(self, row: pyodbc.Row):
        self.row = row
        self.test_names = TestsFileImporter().get_test_names()
        self.test_results = []
        self.tests_names_and_results = []
        self.devices_ids = []
        self.test_id = row[0]

        self.devices_ids.append(row[-2])
        self.devices_ids.append(row[-1])

        for i in range(1, len(row) - 2):
            self.test_results.append(row[i])

        for i in range(len(self.test_names)):
            self.tests_names_and_results.append(TestResult(name=self.test_names[i], result=self.test_results[i]))

    def get_test_results(self):
        return self.test_results

    def get_devices_ids(self):
        return self.devices_ids

    def get_test_id(self):
        return self.test_id

    def __str__(self):
        # string in form of "tests":[["testname","true"],["testname2","false"]]
        tests = ""
        for i in range(len(self.tests_names_and_results)):
            tests += f'["{self.tests_names_and_results[i].get_name()}", "{str(self.tests_names_and_results[i].get_result()).lower()}"]'
            if i != len(self.tests_names_and_results) - 1:
                tests += ","
        return f'"tests":[{tests}]'


if __name__ == '__main__':
    def __repr__(self):
        return self.__str__()