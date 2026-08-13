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
        self.assertEqual(candidate.route_class, "cn2_gia")

    def test_evaluate_trace_classifies_cn2_gt_and_163_direct(self):
        cn2_gt = MODULE.Candidate(
            "192.0.2.1", 443, "JP", "", "NRT", 13335, "", 1
        )
        MODULE.evaluate_trace(
            cn2_gt,
            {
                "results": [
                    {
                        "probe": {"city": "Nanjing"},
                        "result": {"rawOutput": "7 59.43.132.149 13 ms"},
                    }
                ]
            },
        )
        telecom = MODULE.Candidate(
            "192.0.2.2", 443, "JP", "", "NRT", 4134, "", 1
        )
        MODULE.evaluate_trace(telecom, {"results": []})
        self.assertEqual(cn2_gt.route_class, "cn2_gt")
        self.assertEqual(telecom.route_class, "telecom_163_direct")

    def test_unlimited_candidate_selection(self):
        candidates = [
            MODULE.Candidate(str(ip), 443, "JP", "", "NRT", 0, "", 1)
            for ip in ("192.0.2.1", "192.0.2.2", "192.0.2.3")
        ]
        args = type("Args", (), {"max_candidates": 0, "concurrency": 1, "timeout_ms": 1})()
        original = MODULE.test_candidate
        MODULE.test_candidate = lambda candidate, timeout_ms: 1
        try:
            result = MODULE.validate_via_baidu(candidates, args)
        finally:
            MODULE.test_candidate = original
        self.assertEqual(len(result), 3)

    def test_baidu_validation_refreshes_restored_candidate(self):
        candidate = MODULE.Candidate(
            "192.0.2.1", 443, "JP", "", "NRT", 0, "", 1,
            baidu_delay_ms=None, tested=True,
        )
        args = type("Args", (), {"max_candidates": 0, "concurrency": 1, "timeout_ms": 1})()
        calls = []
        original = MODULE.test_candidate
        MODULE.test_candidate = lambda item, timeout_ms: calls.append(item.ip) or 8
        try:
            result = MODULE.validate_via_baidu([candidate], args)
        finally:
            MODULE.test_candidate = original
        self.assertEqual(calls, ["192.0.2.1"])
        self.assertEqual(result[0].baidu_delay_ms, 8)

    def test_legacy_cn2_csv_is_a_completed_checkpoint(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "cn2.csv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=[
                        "ip", "port", "country", "city", "datacenter", "asn",
                        "organization", "source_latency_ms", "baidu_delay_ms",
                        "tested", "cn2", "cn2_evidence", "trace_url",
                    ],
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "ip": "192.0.2.1", "port": 443, "country": "JP",
                        "cn2": "True", "tested": "True",
                    }
                )
            state = MODULE.load_state(path)
        restored = state["192.0.2.1:443"]
        self.assertTrue(restored.cn2)
        self.assertEqual(restored.trace_status, "cn2_gt")

    def test_progress_state_restores_trace_result(self):
        candidate = MODULE.Candidate("192.0.2.1", 443, "JP", "", "NRT", 4809, "", 1)
        previous = MODULE.Candidate(
            "192.0.2.1",
            443,
            "JP",
            "",
            "NRT",
            4809,
            "",
            1,
            baidu_delay_ms=20,
            tested=True,
            cn2=True,
            trace_status="cn2",
            traced_at="2026-08-13T00:00:00Z",
        )
        MODULE.merge_state([candidate], {MODULE.candidate_key(previous): previous})
        self.assertTrue(candidate.tested)
        self.assertTrue(candidate.cn2)
        self.assertEqual(candidate.trace_status, "cn2")

    def test_confirm_skips_completed_candidates(self):
        completed = MODULE.Candidate(
            "192.0.2.1", 443, "JP", "", "NRT", 0, "", 1,
            baidu_delay_ms=1, tested=True, trace_status="not_cn2",
        )
        args = type("Args", (), {"max_traces": 0, "globalping_token": ""})()
        original = MODULE.create_measurement
        MODULE.create_measurement = lambda candidate, token: self.fail("不应重复追踪已完成候选")
        try:
            MODULE.confirm_cn2([completed], args)
        finally:
            MODULE.create_measurement = original

    def test_confirm_checkpoints_each_finished_trace(self):
        candidates = [
            MODULE.Candidate(
                "192.0.2.1", 443, "JP", "", "NRT", 0, "", 1,
                baidu_delay_ms=1, tested=True,
            ),
            MODULE.Candidate(
                "192.0.2.2", 443, "JP", "", "NRT", 0, "", 1,
                baidu_delay_ms=2, tested=True,
            ),
        ]
        args = type("Args", (), {"max_traces": 0, "globalping_token": ""})()
        checkpoints = []
        original_create = MODULE.create_measurement
        original_wait = MODULE.wait_measurement
        MODULE.create_measurement = lambda candidate, token: candidate.ip
        MODULE.wait_measurement = lambda measurement_id, token: {
            "status": "finished", "results": []
        }
        try:
            MODULE.confirm_cn2(
                candidates,
                args,
                lambda: checkpoints.append([item.trace_status for item in candidates]),
            )
        finally:
            MODULE.create_measurement = original_create
            MODULE.wait_measurement = original_wait
        self.assertEqual(len(checkpoints), 2)
        self.assertEqual([item.trace_status for item in candidates], ["other", "other"])

    def test_unfinished_trace_remains_pending_for_next_run(self):
        candidate = MODULE.Candidate(
            "192.0.2.1", 443, "JP", "", "NRT", 0, "", 1,
            baidu_delay_ms=1, tested=True,
        )
        args = type("Args", (), {"max_traces": 0, "globalping_token": ""})()
        original_create = MODULE.create_measurement
        original_wait = MODULE.wait_measurement
        MODULE.create_measurement = lambda item, token: "measurement-id"
        MODULE.wait_measurement = lambda measurement_id, token: {"status": "in-progress"}
        try:
            MODULE.confirm_cn2([candidate], args)
        finally:
            MODULE.create_measurement = original_create
            MODULE.wait_measurement = original_wait
        self.assertEqual(candidate.trace_status, "pending")
        self.assertTrue(candidate.traced_at)

    def test_two_batches_resume_from_saved_progress(self):
        first_batch = [
            MODULE.Candidate(
                "192.0.2.1", 443, "JP", "", "NRT", 0, "", 1,
                baidu_delay_ms=1, tested=True,
            ),
            MODULE.Candidate(
                "192.0.2.2", 443, "JP", "", "NRT", 0, "", 1,
                baidu_delay_ms=2, tested=True,
            ),
        ]
        args = type("Args", (), {"max_traces": 1, "globalping_token": ""})()
        traced_ips = []
        original_create = MODULE.create_measurement
        original_wait = MODULE.wait_measurement
        MODULE.create_measurement = lambda item, token: traced_ips.append(item.ip) or item.ip
        MODULE.wait_measurement = lambda measurement_id, token: {
            "status": "finished", "results": []
        }
        try:
            with tempfile.TemporaryDirectory() as directory:
                progress_path = Path(directory) / "progress.csv"
                MODULE.confirm_cn2(
                    first_batch,
                    args,
                    lambda: MODULE.write_progress(first_batch, progress_path),
                )
                restored = [
                    MODULE.Candidate(
                        "192.0.2.1", 443, "JP", "", "NRT", 0, "", 1,
                        baidu_delay_ms=1, tested=True,
                    ),
                    MODULE.Candidate(
                        "192.0.2.2", 443, "JP", "", "NRT", 0, "", 1,
                        baidu_delay_ms=2, tested=True,
                    ),
                ]
                MODULE.merge_state(restored, MODULE.load_state(progress_path))
                MODULE.confirm_cn2(restored, args)
        finally:
            MODULE.create_measurement = original_create
            MODULE.wait_measurement = original_wait
        self.assertEqual(traced_ips, ["192.0.2.1", "192.0.2.2"])

    def test_unavailable_candidate_retries_after_new_candidate(self):
        candidates = [
            MODULE.Candidate(
                "192.0.2.1", 443, "JP", "", "NRT", 0, "", 1,
                baidu_delay_ms=1, tested=True, trace_status="unavailable",
                traced_at="2026-08-13T00:00:00Z",
            ),
            MODULE.Candidate(
                "192.0.2.2", 443, "JP", "", "NRT", 0, "", 1,
                baidu_delay_ms=2, tested=True,
            ),
        ]
        args = type("Args", (), {"max_traces": 1, "globalping_token": ""})()
        traced_ips = []
        original = MODULE.create_measurement
        MODULE.create_measurement = lambda item, token: traced_ips.append(item.ip) or "quota"
        try:
            MODULE.confirm_cn2(candidates, args)
        finally:
            MODULE.create_measurement = original
        self.assertEqual(traced_ips, ["192.0.2.2"])


if __name__ == "__main__":
    unittest.main()
