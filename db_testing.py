from DatabaseAccess import DatabaseAccess
from Device import Device
from TestResultsContainer import TestResultsContainer
from TestsFileImporter import TestsFileImporter

# tests = {
#     # Sanity checks
#     "ping": ("sc1", False),
#     "ping I,E,E": ("sc2", False),
#     # Basic device behaviour
#     "ping I,E,E --delay 1": ("bdb1", False),
#     "ping-frag-sep": ("bdb2", False),
#     "ping-frag-sep --pn-per-qos": ("bdb3", False),
#     # A-MSDU attacks
#     "ping I,E --amsdu": ("amsdu1", False),
#     "amsdu-inject": ("amsdu2", False),
#     "amsdu-inject-bad": ("amsdu3", False),
#     # Mixed key attacks (nie dzialaja jak na razie)
#     #"ping I,F,BE,AE": ("mk1", False),
#     #"ping I,F,BE,AE --pn-per-qos": ("mk2", False),
#     # Cache attacks
#     "ping I,E,R,AE": ("ca1", False),
#     "ping I,E,R,E": ("ca2", False),
#     "ping I,E,R,AE --full-recon": ("ca3", False),
#     "ping I,E,R,E --full-recon": ("ca4", False),
#     # Non-consecutive PNs attack
#     "ping I,E,E --inc-pn 2": ("ncpn1", False),
#     # Mixed plain/encrypt attack
#     "ping I,E,P": ("mpe1", False),
#     "ping I,P,E": ("mpe2", False),
#     "ping I,P": ("mpe3", False),
#     "ping I,P,P": ("mpe4", False),
#     "linux-plain": ("mpe5", False),
#     # Broadcast fragment attack
#     "ping I,D,P --bcast-ra": ("bfa1", False),
#     "ping D,BP --bcast-ra": ("bfa2", False),
#     # A-MSDU EAPOL attack
#     "eapol-amsdu I,P": ("eapol1", False),
#     "eapol-amsdu BP": ("eapol2", False),
#     "eapol-amsdu-bad I,P": ("eapol3", False),
#     "eapol-amsdu-bad BP": ("eapol4", False),
# }

example_results = TestsFileImporter().get_test_results()

print(example_results)

trc = TestResultsContainer(example_results)

db = DatabaseAccess()
db.create_database()
device = Device("test device name", "test description", "1.0.0")
print(device)
id1 = db.export_device(device)
device = Device("test device name 2", "test description 2", "1.1.0")
id2 = db.export_device(device)
db.print_devices()

db.export_test_results(trc, id1, id2)
print(db.import_test_results())
db.print_test_results()
