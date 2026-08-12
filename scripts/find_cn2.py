#!/usr/bin/env python3
"""从代理 CSV 中筛选并验证电信 CN2 回程。"""

from __future__ import annotations

import argparse
import csv
import ipaddress
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from pathlib import Path

CN2_ASNS = {4809, 23764}
DEFAULT_REGIONS = {"HK", "JP", "SG", "TW", "KR"}
TRACE_LOCATIONS = (
    {"country": "CN", "city": "Guangzhou"},
    {"country": "CN", "city": "Nanjing"},
    {"country": "CN", "city": "Beijing"},
    {"country": "CN", "asn": 4134},
)


@dataclass
class Candidate:
    ip: str
    port: int
    country: str
    city: str
    datacenter: str
    asn: int
    organization: str
    source_latency_ms: float | None
    baidu_delay_ms: int | None = None
    tested: bool = False
    cn2: bool = False
    cn2_evidence: str = ""
    trace_url: str = ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="输入 CSV")
    parser.add_argument("--output-dir", default=Path("output"), type=Path)
    parser.add_argument("--regions", default=",".join(sorted(DEFAULT_REGIONS)))
    parser.add_argument("--max-candidates", type=int, default=300)
    parser.add_argument("--preselect", type=int, default=80)
    parser.add_argument("--max-traces", type=int, default=50)
    parser.add_argument("--timeout-ms", type=int, default=8000)
    parser.add_argument("--concurrency", type=int, default=100)
    parser.add_argument("--globalping-token", default=os.getenv("GLOBALPING_TOKEN", ""))
    parser.add_argument("--github-run-id", default=os.getenv("GITHUB_RUN_ID", ""))
    return parser.parse_args()


def parse_latency(value: str) -> float | None:
    match = re.search(r"[\d.]+", value or "")
    return float(match.group()) if match else None


def load_candidates(path: Path, regions: set[str]) -> list[Candidate]:
    candidates: list[Candidate] = []
    seen: set[tuple[str, int]] = set()
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            try:
                ip = str(ipaddress.ip_address(row["IP地址"].strip()))
                port = int(row["端口号"])
            except (KeyError, ValueError):
                continue
            country = row.get("IP位置", "").upper()
            if country not in regions or (ip, port) in seen:
                continue
            seen.add((ip, port))
            try:
                asn = int(row.get("ASN号码") or 0)
            except ValueError:
                asn = 0
            candidates.append(
                Candidate(
                    ip=ip,
                    port=port,
                    country=country,
                    city=row.get("城市(中文)") or row.get("城市", ""),
                    datacenter=row.get("数据中心", ""),
                    asn=asn,
                    organization=row.get("ASN组织", ""),
                    source_latency_ms=parse_latency(row.get("网络延迟", "")),
                )
            )
    candidates.sort(
        key=lambda item: (
            item.asn not in CN2_ASNS,
            item.source_latency_ms is None,
            item.source_latency_ms or 10**9,
            item.country,
            item.ip,
        )
    )
    return candidates


def api_request(url: str, timeout: float, headers: dict[str, str] | None = None) -> dict:
    request = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)


def test_candidate(candidate: Candidate, timeout_ms: int) -> int | None:
    target = "cp.cloudflare.com"
    base_command = [
        "curl",
        "--silent",
        "--show-error",
        "--output",
        "/dev/null",
        "--connect-timeout",
        str(max(1, timeout_ms // 1000)),
        "--max-time",
        str(max(2, timeout_ms // 1000 + 3)),
        "--proxy",
        "http://cloudnproxy.baidu.com:443",
        "--proxy-header",
        "Host: ascdn.baidu.com",
        "--proxy-header",
        "Proxy-Connection: Keep-Alive",
        "--proxy-header",
        "X-T5-Auth: 1951164069",
        "--proxy-header",
        "User-Agent: okhttp/3.11.0 SP-engine/2.71.0 Dalvik/2.1.0 (Linux; U; Android 9; HMA-AL00 Build/PQ3B.190801.002) baiduboxapp/13.33.0.11 (Baidu; P1 9)",
    ]
    for _ in range(3):
        command = base_command + [
            "--connect-to",
            f"{target}:443:{candidate.ip}:{candidate.port}",
            "--write-out",
            "%{http_code} %{time_total}",
            f"https://{target}/",
        ]
        try:
            result = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
                timeout=timeout_ms / 1000 + 8,
            )
            status, elapsed = result.stdout.strip().split()
            if result.returncode == 0 and status in {"200", "204"}:
                return max(1, round(float(elapsed) * 1000))
        except (OSError, ValueError, subprocess.TimeoutExpired):
            continue
    return None


def validate_via_baidu(candidates: list[Candidate], args: argparse.Namespace) -> list[Candidate]:
    selected = candidates[: args.max_candidates]
    if not selected:
        return []
    with ThreadPoolExecutor(max_workers=args.concurrency) as executor:
        futures = {
            executor.submit(test_candidate, candidate, args.timeout_ms): index
            for index, candidate in enumerate(selected)
        }
        for future in as_completed(futures):
            index = futures[future]
            selected[index].tested = True
            selected[index].baidu_delay_ms = future.result()
    return sorted(
        (item for item in selected if item.baidu_delay_ms is not None),
        key=lambda item: (item.baidu_delay_ms or 10**9, item.ip),
    )


def preselect_candidates(candidates: list[Candidate], limit: int) -> list[Candidate]:
    """均匀保留地区候选，同时始终包含已知 CN2 ASN。"""
    if len(candidates) <= limit:
        return candidates
    selected = [item for item in candidates if item.asn in CN2_ASNS]
    selected_keys = {(item.ip, item.port) for item in selected}
    countries = sorted({item.country for item in candidates})
    per_country = max(1, (limit - len(selected)) // max(1, len(countries)))
    for country in countries:
        pool = [
            item
            for item in candidates
            if item.country == country and (item.ip, item.port) not in selected_keys
        ]
        selected.extend(pool[:per_country])
        selected_keys.update((item.ip, item.port) for item in pool[:per_country])
    if len(selected) < limit:
        selected.extend(
            item
            for item in candidates
            if (item.ip, item.port) not in selected_keys
        )
    return selected[:limit]


def globalping_headers(token: str) -> dict[str, str]:
    headers = {"Content-Type": "application/json", "User-Agent": "cn2-proxy-finder/1.0"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def create_measurement(candidate: Candidate, token: str) -> str:
    payload = json.dumps(
        {
            "type": "traceroute",
            "target": candidate.ip,
            "locations": list(TRACE_LOCATIONS),
            "limit": 4,
            "measurementOptions": {"protocol": "ICMP"},
        }
    ).encode()
    request = urllib.request.Request(
        "https://api.globalping.io/v1/measurements",
        data=payload,
        headers=globalping_headers(token),
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return str(json.load(response).get("id", ""))
    except urllib.error.HTTPError as error:
        if error.code in {402, 429}:
            return "quota"
        if error.code == 400:
            return "unavailable"
        raise


def wait_measurement(measurement_id: str, token: str) -> dict:
    endpoint = f"https://api.globalping.io/v1/measurements/{measurement_id}"
    deadline = time.monotonic() + 45
    last: dict = {}
    while time.monotonic() < deadline:
        try:
            last = api_request(endpoint, 20, globalping_headers(token))
        except (OSError, urllib.error.URLError, json.JSONDecodeError):
            time.sleep(2)
            continue
        if last.get("status") == "finished":
            break
        time.sleep(2)
    return last


def evaluate_trace(candidate: Candidate, measurement: dict) -> None:
    evidence: list[str] = []
    for result in measurement.get("results", []):
        probe = result.get("probe", {})
        raw = result.get("result", {}).get("rawOutput", "")
        hops = sorted(set(re.findall(r"59\.43\.\d{1,3}\.\d{1,3}", raw)))
        if hops:
            location = probe.get("city") or probe.get("country") or str(probe.get("asn", "CN"))
            evidence.append(f"{location}: {', '.join(hops)}")
    candidate.cn2 = bool(evidence)
    candidate.cn2_evidence = "; ".join(evidence)


def confirm_cn2(candidates: list[Candidate], args: argparse.Namespace) -> None:
    trace_targets = sorted(
        candidates,
        key=lambda item: (item.asn not in CN2_ASNS, item.baidu_delay_ms or 10**9),
    )[: args.max_traces]
    for index, candidate in enumerate(trace_targets, 1):
        try:
            measurement_id = create_measurement(candidate, args.globalping_token)
            if measurement_id == "quota":
                print("Globalping 配额不足，停止新增路由追踪", file=sys.stderr)
                break
            if measurement_id == "unavailable":
                print(f"没有适合 {candidate.ip} 的路由探针，跳过", file=sys.stderr)
                continue
            candidate.trace_url = f"https://globalping.io?measurement={measurement_id}"
            evaluate_trace(candidate, wait_measurement(measurement_id, args.globalping_token))
            print(f"[{index}/{len(trace_targets)}] {candidate.ip}: CN2={candidate.cn2}")
        except (OSError, urllib.error.URLError, json.JSONDecodeError) as error:
            print(f"路由追踪失败 {candidate.ip}: {error}", file=sys.stderr)


def write_outputs(all_candidates: list[Candidate], alive: list[Candidate], args: argparse.Namespace) -> None:
    args.output_dir.mkdir(parents=True, exist_ok=True)
    confirmed = [item for item in alive if item.cn2]
    headers = list(Candidate.__dataclass_fields__)
    with (args.output_dir / "cn2.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(asdict(item) for item in confirmed)
    (args.output_dir / "cn2.json").write_text(
        json.dumps([asdict(item) for item in confirmed], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    report = [
        "# CN2 代理筛选报告",
        "",
        f"- CSV 候选数：{len(all_candidates)}",
        f"- 经百度前置测试数：{min(len(all_candidates), args.max_candidates)}",
        f"- 可用数：{len(alive)}",
        f"- CN2 路由确认数：{len(confirmed)}",
        "",
        "判断标准：经给定百度 HTTP CONNECT 前置可连接目标代理，且中国电信探针的回程 traceroute 出现 `59.43.0.0/16`。",
        "",
        "| IP | 端口 | 地区 | ASN | 延迟 | CN2 证据 | 路由 |",
        "|---|---:|---|---:|---:|---|---|",
    ]
    for item in confirmed:
        report.append(
            f"| `{item.ip}` | {item.port} | {item.country}/{item.datacenter} | AS{item.asn} "
            f"| {item.baidu_delay_ms} ms | {item.cn2_evidence} | [查看]({item.trace_url}) |"
        )
    if not confirmed:
        report.append("| - | - | - | - | - | 本轮未确认到 CN2 | - |")
    (args.output_dir / "README.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    regions = {item.strip().upper() for item in args.regions.split(",") if item.strip()}
    candidates = load_candidates(args.input, regions)
    candidates = preselect_candidates(candidates, args.preselect)
    print(f"预选 {len(candidates)} 个候选，开始经百度前置验证")
    alive = validate_via_baidu(candidates, args)
    print(f"百度前置可用候选 {len(alive)} 个，开始确认 CN2 路由")
    confirm_cn2(alive, args)
    write_outputs(candidates, alive, args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
