#!/usr/bin/env python3
"""将自定义中文 CSV 转换为通用测速输入并执行下载测速。"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import sys
from pathlib import Path


def load_speedtest_module():
    path = Path(__file__).with_name("speedtest_cn2_gt.py")
    spec = importlib.util.spec_from_file_location("speedtest_cn2_gt", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def convert_input(source: Path, target: Path) -> int:
    rows: list[dict[str, str]] = []
    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            ip = (row.get("IP地址") or "").strip()
            port = (row.get("端口") or row.get("端口号") or "").strip()
            if not ip or not port:
                continue
            rows.append(
                {
                    "ip": ip,
                    "port": port,
                    "country": (row.get("城市") or row.get("地区") or "").strip(),
                    "datacenter": (row.get("数据中心") or "").strip(),
                    "route_class": "custom",
                }
            )
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("ip", "port", "country", "datacenter", "route_class"),
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--bytes", type=int, default=2_097_152)
    parser.add_argument("--timeout", type=int, default=45)
    parser.add_argument("--concurrency", type=int, default=10)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    normalized = args.output_dir / "normalized.csv"
    count = convert_input(args.input, normalized)
    if not count:
        raise SystemExit("没有有效的自定义候选")

    speedtest = load_speedtest_module()
    candidates = speedtest.load_candidates(normalized, "custom")
    results = []
    from concurrent.futures import ThreadPoolExecutor, as_completed

    with ThreadPoolExecutor(max_workers=max(1, args.concurrency)) as executor:
        futures = {
            executor.submit(speedtest.speedtest, item, args.bytes, args.timeout): item
            for item in candidates
        }
        for index, future in enumerate(as_completed(futures), 1):
            result = future.result()
            results.append(result)
            print(
                f"[{index}/{len(candidates)}] {result.ip}:{result.port}: "
                f"{result.speed_mbytes_s if result.speed_mbytes_s is not None else '-'} MB/s"
            )
    speedtest.write_outputs(results, args.output_dir, args.bytes, "custom")
    normalized.unlink()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
