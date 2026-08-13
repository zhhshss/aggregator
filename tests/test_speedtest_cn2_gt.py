import csv
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SPEC = importlib.util.spec_from_file_location(
    "speedtest_cn2_gt", Path(__file__).parents[1] / "scripts" / "speedtest_cn2_gt.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class SpeedtestCn2GtTest(unittest.TestCase):
    def test_loads_only_cn2_gt(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "progress.csv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=("ip", "port", "country", "datacenter", "route_class"),
                )
                writer.writeheader()
                writer.writerows(
                    (
                        {"ip": "192.0.2.1", "port": 443, "country": "JP", "route_class": "cn2_gt"},
                        {"ip": "192.0.2.2", "port": 443, "country": "JP", "route_class": "other"},
                    )
                )
            candidates = MODULE.load_candidates(path, "cn2_gt")
        self.assertEqual([item["ip"] for item in candidates], ["192.0.2.1"])

    def test_loads_non_cn2_other_class(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "progress.csv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=("ip", "port", "country", "datacenter", "route_class"),
                )
                writer.writeheader()
                writer.writerows(
                    (
                        {"ip": "192.0.2.1", "port": 443, "country": "JP", "route_class": "cn2_gt"},
                        {"ip": "192.0.2.2", "port": 443, "country": "JP", "route_class": "other"},
                    )
                )
            candidates = MODULE.load_candidates(path, "other")
        self.assertEqual([item["ip"] for item in candidates], ["192.0.2.2"])

    def test_report_sorts_fastest_first(self):
        results = [
            MODULE.Result("192.0.2.1", 443, "JP", "NRT", "other", "ok", 1.0, 0.125, 100, 1.0),
            MODULE.Result("192.0.2.2", 443, "JP", "NRT", "other", "ok", 2.0, 0.25, 100, 0.5),
            MODULE.Result("192.0.2.3", 443, "JP", "NRT", "other", "failed", None, None, 0, None),
        ]
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            MODULE.write_outputs(results, output, 100, "other")
            with (output / "other_speedtest.csv").open(encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
        self.assertEqual([row["ip"] for row in rows], ["192.0.2.2", "192.0.2.1", "192.0.2.3"])


if __name__ == "__main__":
    unittest.main()
