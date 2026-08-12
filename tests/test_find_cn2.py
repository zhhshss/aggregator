import csv
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SPEC = importlib.util.spec_from_file_location(
    "find_cn2", Path(__file__).parents[1] / "scripts" / "find_cn2.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class FindCn2Test(unittest.TestCase):
    def test_load_candidates_prioritizes_cn2_asn(self):
        fields = [
            "IP地址", "端口号", "IP位置", "城市(中文)", "数据中心",
            "ASN号码", "ASN组织", "网络延迟",
        ]
        rows = [
            ["1.1.1.1", "443", "HK", "香港", "HKG", "13335", "Cloudflare", "1 ms"],
            ["202.55.27.177", "443", "JP", "东京", "NRT", "4809", "CTGNet", "73 ms"],
            ["9.9.9.9", "443", "US", "", "LAX", "19281", "Quad9", "2 ms"],
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.csv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.writer(handle)
                writer.writerow(fields)
                writer.writerows(rows)
            result = MODULE.load_candidates(path, {"HK", "JP"})
        self.assertEqual([item.ip for item in result], ["202.55.27.177", "1.1.1.1"])

    def test_evaluate_trace_requires_59_43_hop(self):
        candidate = MODULE.Candidate("202.55.27.177", 443, "JP", "东京", "NRT", 4809, "CTGNet", 73)
        measurement = {
            "results": [
                {
                    "probe": {"city": "Nanjing"},
                    "result": {"rawOutput": "7  59.43.132.149  13 ms\n8  202.55.27.177 44 ms"},
                }
            ]
        }
        MODULE.evaluate_trace(candidate, measurement)
        self.assertTrue(candidate.cn2)
        self.assertIn("59.43.132.149", candidate.cn2_evidence)


if __name__ == "__main__":
    unittest.main()
