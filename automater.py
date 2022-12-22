import os
import sys
import threading
from time import sleep

import pyshark as pyshark
from colorama import Fore, Style

research_dir = os.getcwd()
iface = "wlp0s20f3"
should_capture = True

tests = {
    # Sanity checks
    "ping": ("sc1", False),
    "ping I,E,E": ("sc2", False),
    # Basic device behaviour
    "ping I,E,E --delay 1": ("bdb1", False),
    "ping-frag-sep": ("bdb2", False),
    "ping-frag-sep --pn-per-qos": ("bdb3", False),
    # A-MSDU attacks
    "ping I,E --amsdu": ("amsdu1", False),
    "amsdu-inject": ("amsdu2", False),
    "amsdu-inject-bad": ("amsdu3", False),
    # Mixed key attacks (nie dzialaja jak na razie)
    #"ping I,F,BE,AE": ("mk1", False),
    #"ping I,F,BE,AE --pn-per-qos": ("mk2", False),
    # Cache attacks
    "ping I,E,R,AE": ("ca1", False),
    "ping I,E,R,E": ("ca2", False),
    "ping I,E,R,AE --full-recon": ("ca3", False),
    "ping I,E,R,E --full-recon": ("ca4", False),
    # Non-consecutive PNs attack
    "ping I,E,E --inc-pn 2": ("ncpn1", False),
    # Mixed plain/encrypt attack
    "ping I,E,P": ("mpe1", False),
    "ping I,P,E": ("mpe2", False),
    "ping I,P": ("mpe3", False),
    "ping I,P,P": ("mpe4", False),
    "linux-plain": ("mpe5", False),
    # Broadcast fragment attack
    "ping I,D,P --bcast-ra": ("bfa1", False),
    "ping D,BP --bcast-ra": ("bfa2", False),
    # A-MSDU EAPOL attack
    "eapol-amsdu I,P": ("eapol1", False),
    "eapol-amsdu BP": ("eapol2", False),
    "eapol-amsdu-bad I,P": ("eapol3", False),
    "eapol-amsdu-bad BP": ("eapol4", False),
}


def attack(attackType="ping", interface="wlp0s20f3"):
    command = f"{research_dir}/fragattack.py {interface} {attackType}"
    # os.system(command)
    log = os.popen(command).read()
    if ">>> TEST COMPLETED SUCCESSFULLY" in log:
        tests[attackType][1] = True
        return True
    return False


def sniff(capture):
    # for raw_packet in capture.sniff_continuously():
    #     print(raw_packet)
    capture.sniff(timeout=20)


def automate(testName, interface="wlp0s20f3"):
    if should_capture:
        file = f"{research_dir}/captures/capture_{test}.pcap"
        output = open(file, "w")
        capture = pyshark.LiveCapture(interface=interface, output_file=file)
        print(f"Starting capture on {Fore.YELLOW}{interface}{Style.RESET_ALL}...")
        sniff_thread = threading.Thread(target=sniff, args=(capture,), daemon=True)
        sniff_thread.start()

    print(f"Starting attack {Fore.YELLOW}{testName}{Style.RESET_ALL} "
          f"on interface {Fore.YELLOW}{interface}{Style.RESET_ALL}")

    results = attack(attackType=testName, interface=interface)
    if results:
        print(f"{Fore.GREEN}Attack {testName} was successful")
    else:
        print(f"{Fore.LIGHTRED_EX}Attack {testName} failed")
    print(Style.RESET_ALL, end="")
    if should_capture:
        sniff_thread.join()
        capture.close()
        print(f"Capture finished\n")
        output.close()


def initialize():
    if os.geteuid() != 0:
        print("Please run this script as root")
        exit(1)
    if not os.path.exists(f"{research_dir}/captures"):
        os.mkdir(f"{research_dir}/captures")
    if "--no-capture" in sys.argv:
        global should_capture
        should_capture = False
        print("Not capturing packets")
    if "--iface" in sys.argv:
        global iface
        iface = sys.argv[sys.argv.index("--iface") + 1]

initialize()
for test in tests:
    automate(test, interface=iface)

print(f"\n{Fore.CYAN}All tests finished")
print("********\n" * 3)
print(f"{Fore.GREEN}Successful tests:")
maxLength = max([len(test) for test in tests])
for test in tests:
    if tests[test][1]:
        print(f"{Fore.GREEN}{test}:{' ' * (maxLength + 1 - len(test))}{tests[test][1]}{Style.RESET_ALL}")

print(f"\n{Fore.RED}Failed tests:")
for test in tests:
    if not tests[test][1]:
        print(f"{Fore.RED}{test}:{' ' * (maxLength + 1 - len(test))}{tests[test][1]}{Style.RESET_ALL}")
