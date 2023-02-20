import string


class TestResult:
    def __init__(self, name: string, alias: string = None, type: string = None, result=False, capture_file: string = None):
        self.name = name
        self.alias = alias
        self.type = type
        self.result = result
        self.capture_file = capture_file

    def get_name(self):
        return self.name

    def get_alias(self):
        return self.alias

    def get_type(self):
        return self.type

    def get_result(self):
        return self.result

    def get_capture_file(self):
        return self.capture_file

    def set_name(self, name):
        self.name = name

    def set_alias(self, alias):
        self.alias = alias

    def set_type(self, type):
        self.type = type

    def set_result(self, result):
        self.result = result

    def set_capture_file(self, capture_file):
        self.capture_file = capture_file

    def __str__(self):
        return f"Test: {self.name}, {self.alias}, {self.result}. Type: {self.type}. Capture file: {self.capture_file}"
