import os
import sys
import threading

import pyshark as pyshark
from colorama import Fore, Style
import uuid

from TestResult import TestResult
from TestResultsContainer import TestResultsContainer
from TestsFileImporter import TestsFileImporter


# research_dir = os.getcwd()
# iface = "wlp0s20f3"
# should_capture = True

class Automater:
    def __init__(self, capture=None, interface=None, group=None):
        self.should_capture = capture
        self.research_dir = os.getcwd()
        self.capture = capture
        self.interface = interface
        self.group_name = group
        # initialize(capture=capture, interface=interface, group=group)
        self.tests_all = TestsFileImporter().get_test_results()
        self.tests = []
        self.capture_name = str(uuid.uuid4().hex)
        for test in self.tests_all:
            if self.group_name is not None:
                if test.type == self.group_name:
                    self.tests.append(test)

        self.results = TestResultsContainer(self.tests)

    def run(self):
        for test in self.tests:
            if self.should_capture:
                test.set_capture_file(self.capture_name)
            print(test)
            if self.group_name is not None and test.type != self.group_name:
                continue
            self.automate(test)

            # self.results.add(test)
        print("TESTS")
        print(self.tests)
        print(f"{Fore.GREEN}Successful tests:")

        maxLength = max([len(test.name) for test in self.tests])
        for test in self.tests:
            if test.result:
                print(f"{Fore.GREEN}{test.name}:{' ' * (maxLength + 1 - len(test.name))}{test.result}{Style.RESET_ALL}")

        print(f"\n{Fore.RED}Failed tests:")
        for test in self.tests:
            if not test.result:
                print(f"{Fore.RED}{test.name}:{' ' * (maxLength + 1 - len(test.name))}{test.result}{Style.RESET_ALL}")

        return self.tests

    def attack(self, test: TestResult, interface="wlp0s20f3"):
        command = f"{self.research_dir}/fragattack.py {interface} {test.name}"
        # os.system(command)
        log = os.popen(command).read()
        if ">>> TEST COMPLETED SUCCESSFULLY" in log:
            test.set_result(True)
            return True
        return False

    def sniff(self, capture):
        # for raw_packet in capture.sniff_continuously():
        #     print(raw_packet)
        capture.sniff(timeout=20)

    def automate(self, test: TestResult):
        print(f"Starting attack {Fore.YELLOW}{test.name}{Style.RESET_ALL} ")
        file = ""
        if self.should_capture:
            file = f"{self.research_dir}/captures/capture_{self.capture_name}.pcap"
            output = open(file, "w")
            capture = pyshark.LiveCapture(interface=self.interface, output_file=file)
            print(f"Starting capture on {Fore.YELLOW}{self.interface,}{Style.RESET_ALL}...")
            sniff_thread = threading.Thread(target=self.sniff, args=(capture,), daemon=True)
            sniff_thread.start()

        print(f"Starting attack {Fore.YELLOW}{test.name}{Style.RESET_ALL} "
              f"on interface {Fore.YELLOW}{self.interface}{Style.RESET_ALL}")

        results = self.attack(test=test, interface=self.interface)
        if results:
            print(f"{Fore.GREEN}Attack {test.name} was successful")
        else:
            print(f"{Fore.LIGHTRED_EX}Attack {test.name} failed")
        print(Style.RESET_ALL, end="")
        if self.should_capture:
            sniff_thread.join()
            capture.close()
            print(f"Capture finished\n")
            output.close()

    def initialize(self, capture=None, interface=None, group=None):
        if os.geteuid() != 0:
            print("Please run this script as root")
            exit(1)
        if not os.path.exists(f"{self.research_dir}/captures"):
            os.mkdir(f"{self.research_dir}/captures")
        if "--no-capture" in sys.argv:
            self.should_capture = False
            print("Not capturing packets")
        if "--iface" in sys.argv:
            self.interface = sys.argv[sys.argv.index("--iface") + 1]
        # if --group is in sys.argv, run all tests in that group
        if "--group" in sys.argv:
            self.group_name = sys.argv[sys.argv.index("--group") + 1]
        if capture is not None:
            self.should_capture = capture
        if interface is not None:
            self.interface = interface
        if group is not None:
            self.group_name = group

# if __name__ == '__main__':
#     initialize()
#     if not group_name:
#         group_name = "sanity_checks"
#     trc = TestResultsContainer(TestsFileImporter().get_test_results())
#
#     if group_name:
#         tests = trc.get_test_results_from_group(group_name)
#         print(f"Running {len(tests)} tests from group {group_name}")
#     else:
#         tests = trc.get_all_test_results()
#         print(f"Running {len(tests)} tests")
#
#     print("Tests: ")
#     for test in tests:
#         automate(test, interface=iface)
#
#     print(f"\n{Fore.CYAN}All tests finished")
#     print("********\n" * 3)
#     print(f"{Fore.GREEN}Successful tests:")
#
#     maxLength = max([len(test.name) for test in tests])
#     for test in tests:
#         if test.result:
#             print(f"{Fore.GREEN}{test.name}:{' ' * (maxLength + 1 - len(test.name))}{test.result}{Style.RESET_ALL}")
#
#     print(f"\n{Fore.RED}Failed tests:")
#     for test in tests:
#         if not test.result:
#             print(f"{Fore.RED}{test.name}:{' ' * (maxLength + 1 - len(test.name))}{test.result}{Style.RESET_ALL}")
