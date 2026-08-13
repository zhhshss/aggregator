import csv
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SPEC = importlib.util.spec_from_file_location(
    "speedtest_custom_csv", Path(__file__).parents[1] / "scripts" / "speedtest_custom_csv.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class SpeedtestCustomCsvTest(unittest.TestCase):
    def test_converts_chinese_csv(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "input.csv"
            target = Path(directory) / "output.csv"
            source.write_text(
                "IP地址,端口,TLS,数据中心,地区,城市,网络延迟\n"
                "192.0.2.1,8443,true,NRT,亚太,日本东京,1 ms\n",
                encoding="utf-8",
            )
            count = MODULE.convert_input(source, target)
            with target.open(encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
        self.assertEqual(count, 1)
        self.assertEqual(rows[0]["port"], "8443")
        self.assertEqual(rows[0]["country"], "日本东京")
        self.assertEqual(rows[0]["route_class"], "custom")


if __name__ == "__main__":
    unittest.main()
