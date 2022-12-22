import pyodbc

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
            self.tests_names_and_results.append((self.test_names[i], self.test_results[i]))

    def get_test_results(self):
        return self.test_results

    def get_devices_ids(self):
        return self.devices_ids

    def get_test_id(self):
        return self.test_id

    def __str__(self):
        return "Test id: " + str(self.test_id) + ", devices ids: " + str(self.devices_ids) + ", test results: " + str(self.test_results)

    def __repr__(self):
        return self.__str__()