import string


class TestResult:
    def __init__(self, name: string, alias: string = None, type: string = None, result=False):
        self.name = name
        self.alias = alias
        self.type = type
        self.result = result

    def get_name(self):
        return self.name

    def get_alias(self):
        return self.alias

    def get_type(self):
        return self.type

    def get_result(self):
        return self.result

    def set_name(self, name):
        self.name = name

    def set_alias(self, alias):
        self.alias = alias

    def set_type(self, type):
        self.type = type

    def set_result(self, result):
        self.result = result

    def __str__(self):
        return f"Test: {self.name}, {self.alias}, {self.result}. Type: {self.type}"
