import string


class Device:
    def __init__(self, name: string, description: string, software_version: string):
        self.name = name
        self.description = description
        self.software_version = software_version

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_software_version(self):
        return self.software_version

    def __str__(self):
        return f"{self.name}, {self.description}, {self.software_version}"
