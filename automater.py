import os
import threading
from time import sleep

import pyshark as pyshark

research_dir = "/home/dev/fragattacks/research"

tests = {
        # Sanity checks
    "ping": False,
    "ping I,E,E": False,
        # Basic device behaviour
    "ping I,E,E --delay 1": False,
    "ping-frag-sep": False,
    "ping-frag-sep --pn-per-qos": False,
        # A-MSDU attacks
    "ping I,E --amsdu": False,
    "amsdu-inject": False,
    "amsdu-inject-bad": False,
        # Mixed key attacks (nie dzialaja jak na razie)
    # "ping I,F,BE,AE": False,
    # "ping I,F,BE,AE --pn-per-qos": False,
        # Cache attacks
    "ping I,E,R,AE": False,
    "ping I,E,R,E": False,
    "ping I,E,R,AE --full-recon": False,
    "ping I,E,R,E --full-recon": False,
        # Non-consecutive PNs attack
    "ping I,E,E --inc-pn 2": False,
        # Mixed plain/encrypt attack
    "ping I,E,P": False,
    "ping I,P,E": False,
    "ping I,P": False,
    "ping I,P,P": False,
    "linux-plain": False,
        # Broadcast fragment attack
    "ping I,D,P --bcast-ra": False,
    "ping D,BP --bcast-ra": False,
        # A-MSDU EAPOL attack
    "eapol-amsdu I,P": False,
    "eapol-amsdu BP": False,
    "eapol-amsdu-bad I,P": False,
    "eapol-amsdu-bad BP": False,

}

def attack(interface="wlp0s20f3", attackType="ping"):
    command = f"/{research_dir}/fragattack.py {interface} {attackType}"
    # os.system(command)
    log = os.popen(command).read()
    if ">>> TEST COMPLETED SUCCESSFULLY" in log:
        tests[attackType] = True

def sniff(capture):
    # for raw_packet in capture.sniff_continuously():
    #     print(raw_packet)
    capture.sniff(timeout=20)

def automate(test):
    file = f"{research_dir}/captures/capture_{test}.pcap"
    output = open(file, "w")

    capture = pyshark.LiveCapture(interface="wlp0s20f3", output_file=file)
    print("Starting capture")

    # start sniffing packets in a separate thread
    # then start the attack
    print(f"Starting attack {test}")
    sniff_thread = threading.Thread(target=sniff, args=(capture,), daemon=True)
    sniff_thread.start()
    attack(attackType=test)
    print("Attack finished")
    # close the async capture
    # wait for the sniffing thread to finish
    sleep(1)
    sniff_thread.join()
    capture.close()
    print("Capture finished")
    print("Capture closed")
    output.close()
    print("Output closed")

def initialize():
    if os.geteuid() != 0:
        print("Please run this script as root")
        exit(1)
    if not os.path.exists(f"{research_dir}/captures"):
        os.mkdir(f"{research_dir}/captures")

initialize()
for test in tests:
    automate(test)


print("Tests finished")
print("********\n"*10)
for test in tests:
    print(f"{test}: {tests[test]}")

