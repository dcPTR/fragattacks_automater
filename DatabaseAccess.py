import os
import string

import pyodbc

from DatabaseResultContainer import DatabaseResultContainer
from Device import Device
from TestResultsContainer import TestResultsContainer

server = "fragattacks.database.windows.net"
database = "fragattacks"
username = "dev"
password = os.environ.get("fadbpassword")  # environment variable fadbpassword contains the password to the database
driver = '{ODBC Driver 17 for SQL Server}'


class DatabaseAccess:
    def __init__(self):
        self.conn = pyodbc.connect(
            'DRIVER=' + driver + ';SERVER=tcp:' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        self.cursor = self.conn.cursor()

    def execute_query(self, query: string):
        self.cursor.execute(query)
        self.conn.commit()
        print("Query executed successfully")

    def print_all_tables(self):
        self.cursor.execute("SELECT * FROM INFORMATION_SCHEMA.TABLES")
        for row in self.cursor:
            print(row)

    def create_database(self, path="resources/database.sql"):
        with open(path, 'r') as f:
            sql = f.read()
            self.cursor.execute(sql)
            self.conn.commit()
            print("Database created successfully")

    def export_test_results(self, tests: TestResultsContainer, device1_id: int = None, device2_id: int = None):

        self.cursor.execute(
            f"INSERT INTO test_results ({tests.get_aliases_as_string()}, device1_id, device2_id) VALUES ({tests.get_test_results_as_bit_string()}, {device1_id}, {device2_id})")
        # self.cursor.execute(
        #     f"INSERT INTO test_results ({tests.get_aliases_as_string()}) VALUES ({tests.get_test_results_as_bit_string()})")
        self.conn.commit()
        print("Test results exported successfully")

    def print_test_results(self):
        self.cursor.execute("SELECT * FROM test_results")
        for row in self.cursor:
            print(row)

    def export_device(self, device: Device):
        self.cursor.execute(
            f"INSERT INTO devices (name, description, software_version) VALUES ('{device.get_name()}', "
            f"'{device.get_description()}', '{device.get_software_version()}')")
        self.conn.commit()
        print("Device exported successfully")
        self.cursor.execute("SELECT @@IDENTITY AS 'Identity';")
        return self.cursor.fetchone()[0]    # id of the inserted device

    def print_devices(self):
        self.cursor.execute("SELECT * FROM devices")
        for row in self.cursor:
            print(row)

    def execute_select(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close_connection(self):
        self.conn.close()
        print("Connection closed")

    def import_test_results(self):
        dbcs = []
        # self.cursor.execute("SELECT * FROM test_results INNER JOIN devices AS d1 ON test_results.device1_id = d1.id INNER JOIN devices AS d2 ON test_results.device2_id = d2.id")
        self.cursor.execute("SELECT * FROM test_results")
        for row in self.cursor:
            print(row)
            dbcs.append(DatabaseResultContainer(row))
            print(dbcs[-1])
        return dbcs

    def get_device_by_name(self, device_name):
        self.cursor.execute(f"SELECT * FROM devices WHERE name = '{device_name}'")
        return self.cursor.fetchone()

    def get_device_by_id(self, device_id):
        self.cursor.execute(f"SELECT * FROM devices WHERE id = {device_id}")
        return self.cursor.fetchone()