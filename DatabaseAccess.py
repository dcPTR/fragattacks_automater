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

    def export_test_results(self, tests: TestResultsContainer):
        self.cursor.execute(
            f"INSERT INTO test_results ({tests.get_aliases_as_string()}) VALUES ({tests.get_test_results_as_bit_string()})")
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
        self.cursor.execute("SELECT * FROM test_results")
        for row in self.cursor:
            dbcs.append(DatabaseResultContainer(row))
        return dbcs
