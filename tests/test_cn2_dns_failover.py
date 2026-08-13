import csv
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SPEC = importlib.util.spec_from_file_location(
    "cn2_dns_failover", Path(__file__).parents[1] / "scripts" / "cn2_dns_failover.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class Cn2DnsFailoverTest(unittest.TestCase):
    def test_groups_and_sorts_by_country(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "cn2.csv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=("ip", "country", "baidu_delay_ms", "route_class"),
                )
                writer.writeheader()
                writer.writerows(
                    (
                        {"ip": "192.0.2.2", "country": "JP", "baidu_delay_ms": "20", "route_class": "cn2_gia"},
                        {"ip": "192.0.2.1", "country": "JP", "baidu_delay_ms": "10", "route_class": "cn2_gt"},
                        {"ip": "198.51.100.1", "country": "SG", "baidu_delay_ms": "5", "route_class": "telecom_163_direct"},
                    )
                )
            grouped = MODULE.load_candidates(path)
        self.assertEqual([item.ip for item in grouped["JP"]], ["192.0.2.2", "192.0.2.1"])
        self.assertEqual([item.ip for item in grouped["SG"]], ["198.51.100.1"])

    def test_current_ip_is_tested_first(self):
        candidates = [
            MODULE.Candidate("192.0.2.1", "JP", 1, "cn2_gia"),
            MODULE.Candidate("192.0.2.2", "JP", 2, "cn2_gt"),
        ]
        tested = []
        original = MODULE.test_ip
        MODULE.test_ip = lambda ip, timeout: (tested.append(ip) or (True, 1))
        try:
            selected, _, _ = MODULE.choose_ip(candidates, "192.0.2.2", 1)
        finally:
            MODULE.test_ip = original
        self.assertEqual(tested, ["192.0.2.2"])
        self.assertEqual(selected.ip, "192.0.2.2")

    def test_managed_record_pattern(self):
        cloudflare = object.__new__(MODULE.Cloudflare)
        cloudflare.request = lambda method, path: {
            "result": [
                {"name": "cn2-tw.example.com", "content": "192.0.2.1"},
                {"name": "other.example.com", "content": "192.0.2.2"},
            ]
        }
        records = cloudflare.managed_records("zone", "cn2", "example.com")
        self.assertEqual(records["TW"]["content"], "192.0.2.1")

    def test_route_record_pattern(self):
        cloudflare = object.__new__(MODULE.Cloudflare)
        cloudflare.request = lambda method, path: {
            "result": [
                {"name": "cn2-gia-jp.example.com", "content": "192.0.2.1"},
                {"name": "cn2-gt-jp.example.com", "content": "192.0.2.2"},
                {"name": "telecom-163-direct-sg.example.com", "content": "198.51.100.1"},
            ]
        }
        records = cloudflare.route_records("zone", "example.com")
        self.assertEqual(records[("cn2_gia", "JP")]["content"], "192.0.2.1")
        self.assertEqual(records[("cn2_gt", "JP")]["content"], "192.0.2.2")
        self.assertEqual(records[("telecom_163_direct", "SG")]["content"], "198.51.100.1")

    def test_tier_hostname(self):
        self.assertEqual(
            MODULE.hostname("cn2_gia", "JP", "example.com"),
            "cn2-gia-jp.example.com",
        )


if __name__ == "__main__":
    unittest.main()
