from TestResult import TestResult


class TestsFileImporter:
    def __init__(self, tests_file="resources/tests.conf"):
        self.group = None
        self.tests_file = tests_file
        self.test_results = []
        self.import_tests()

    def import_tests(self):
        with open(self.tests_file, 'r') as file:
            for line in file:
                if line.startswith("#"):
                    # if header contains (DO NOT USE) then do not import the tests from that group
                    if "DO NOT USE" in line:
                        self.group = None
                    else:
                        self.group = line.lower().replace("#", "").replace(",", "").strip() \
                            .replace(" ", "_").replace("-", "_").replace("/", "_")
                else:
                    if "DO NOT USE" not in line and self.group is not None:
                        test_name = line.split('",')[0].replace('"', '').strip()
                        test_alias = line.split('",')[1].replace('"', '').strip()
                        test_result = TestResult(test_name, test_alias, self.group)
                        self.test_results.append(test_result)

    def get_test_results(self):
        return self.test_results

# trc = TestResultsContainer(TestsFileImporter().get_test_results())
# tests = trc.get_test_results_from_group("mixed_key_attacks")
# for test in tests:
#     print(test)
