import string

from TestResult import TestResult


class TestResultsContainer:
    def __init__(self, test_results: """list[TestResult]"""):
        self.test_results = test_results
        self.sanity_checks = []
        self.basic_device_behaviour = []
        self.amsdu_attacks = []
        self.mixed_key_attacks = []
        self.cache_attacks = []
        self.non_consecutive_pns_attack = []
        self.mixed_plain_encrypt_attack = []
        self.broadcast_fragment_attack = []
        self.amsdu_eapol_attack = []
        self.aliases = []
        self.__sort_test_results()

    def add_test_to_group(self, test_result: TestResult):
        if test_result.get_type() == "sanity_checks":
            self.sanity_checks.append(test_result)
        elif test_result.get_type() == "basic_device_behaviour":
            self.basic_device_behaviour.append(test_result)
        elif test_result.get_type() == "a_msdu_attacks":
            self.amsdu_attacks.append(test_result)
        elif test_result.get_type() == "mixed_key_attacks":
            self.mixed_key_attacks.append(test_result)
        elif test_result.get_type() == "cache_attacks":
            self.cache_attacks.append(test_result)
        elif test_result.get_type() == "non_consecutive_pns_attack":
            self.non_consecutive_pns_attack.append(test_result)
        elif test_result.get_type() == "mixed_plain_encrypt_attack":
            self.mixed_plain_encrypt_attack.append(test_result)
        elif test_result.get_type() == "broadcast_fragment_attack":
            self.broadcast_fragment_attack.append(test_result)
        elif test_result.get_type() == "a_msdu_eapol_attack":
            self.amsdu_eapol_attack.append(test_result)

    def __sort_test_results(self):
        for test_result in self.test_results:
            self.add_test_to_group(test_result)
            if test_result.get_alias() not in self.aliases:
                self.aliases.append(test_result.get_alias())

    def get_sanity_checks(self):
        return self.sanity_checks

    def get_basic_device_behaviour(self):
        return self.basic_device_behaviour

    def get_amsdu_attacks(self):
        return self.amsdu_attacks

    def get_mixed_key_attacks(self):
        return self.mixed_key_attacks

    def get_cache_attacks(self):
        return self.cache_attacks

    def get_non_consecutive_pns_attack(self):
        return self.non_consecutive_pns_attack

    def get_mixed_plain_encrypt_attack(self):
        return self.mixed_plain_encrypt_attack

    def get_broadcast_fragment_attack(self):
        return self.broadcast_fragment_attack

    def get_amsdu_eapol_attack(self):
        return self.amsdu_eapol_attack

    def get_all_test_results(self):
        return self.test_results

    def get_test_results_from_group(self, group: string):
        if group == "sanity_checks":
            return self.sanity_checks
        elif group == "basic_device_behaviour":
            return self.basic_device_behaviour
        elif group == "a_msdu_attacks":
            return self.amsdu_attacks
        elif group == "mixed_key_attacks":
            return self.mixed_key_attacks
        elif group == "cache_attacks":
            return self.cache_attacks
        elif group == "non_consecutive_pns_attack":
            return self.non_consecutive_pns_attack
        elif group == "mixed_plain_encrypt_attack":
            return self.mixed_plain_encrypt_attack
        elif group == "broadcast_fragment_attack":
            return self.broadcast_fragment_attack
        elif group == "a_msdu_eapol_attack":
            return self.amsdu_eapol_attack
        else:
            return None

    def get_test_result_by_name(self, test_name: string):
        for test_result in self.test_results:
            if test_result.get_name() == test_name:
                return test_result
        return None

    def get_test_result_by_alias(self, alias: string):
        for test_result in self.test_results:
            if test_result.get_alias() == alias:
                return test_result
        return None

    def add_test_result(self, test_result: TestResult):
        self.test_results.append(test_result)
        self.add_test_to_group(test_result)

    def get_aliases_as_string(self):
        return ", ".join(self.aliases)

    def get_test_results_as_bit_string(self):
        return ", ".join([str(int(test_result.get_result())) for test_result in self.test_results])

    def get_json(self):
        json = {"tests": []}
        for test_result in self.test_results:
            json["tests"].append([test_result.get_name(), str(test_result.get_result()).lower()])
        return json
