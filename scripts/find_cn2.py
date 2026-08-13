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
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from pathlib import Path
from threading import Lock
from typing import Callable

CN2_ASNS = {4809, 23764}
ROUTE_CLASSES = ("cn2_gia", "cn2_gt", "telecom_163_direct", "other")
TELECOM_163_ASNS = {4134, 4812, 4813, 4816, 4817, 4818, 4819, 58461}
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
    trace_status: str = "pending"
    traced_at: str = ""
    route_class: str = ""
    route_evidence: str = ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="输入 CSV")
    parser.add_argument("--output-dir", default=Path("output"), type=Path)
    parser.add_argument("--regions", default=",".join(sorted(DEFAULT_REGIONS)))
    parser.add_argument(
        "--max-candidates",
        type=int,
        default=0,
        help="百度前置测试上限；0 表示测试地区内全部候选",
    )
    parser.add_argument(
        "--max-traces",
        type=int,
        default=0,
        help="回程路由追踪上限；0 表示追踪全部可用候选",
    )
    parser.add_argument("--timeout-ms", type=int, default=8000)
    parser.add_argument("--concurrency", type=int, default=100)
    parser.add_argument("--trace-concurrency", type=int, default=1)
    parser.add_argument("--globalping-token", default=os.getenv("GLOBALPING_TOKEN", ""))
    parser.add_argument(
        "--globalping-proxy-file",
        type=Path,
        default=Path(os.getenv("GLOBALPING_PROXY_FILE", "")) if os.getenv("GLOBALPING_PROXY_FILE") else None,
        help="Globalping API HTTP 代理池文件，每行一个代理 URL",
    )
    parser.add_argument("--github-run-id", default=os.getenv("GITHUB_RUN_ID", ""))
    return parser.parse_args()


def parse_latency(value: str) -> float | None:
    match = re.search(r"[\d.]+", value or "")
    return float(match.group()) if match else None


def candidate_key(candidate: Candidate) -> str:
    return f"{candidate.ip}:{candidate.port}"


def parse_bool(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes"}


def load_state(path: Path) -> dict[str, Candidate]:
    if not path.is_file():
        return {}
    state: dict[str, Candidate] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            try:
                is_cn2 = parse_bool(row.get("cn2", ""))
                route_class = row.get("route_class", "")
                if not route_class and is_cn2:
                    try:
                        legacy_asn = int(row.get("asn") or 0)
                    except ValueError:
                        legacy_asn = 0
                    route_class = "cn2_gia" if legacy_asn in CN2_ASNS else "cn2_gt"
                trace_status = row.get("trace_status") or route_class or ("cn2_gia" if is_cn2 else "pending")
                candidate = Candidate(
                    ip=str(ipaddress.ip_address(row["ip"].strip())),
                    port=int(row["port"]),
                    country=row.get("country", ""),
                    city=row.get("city", ""),
                    datacenter=row.get("datacenter", ""),
                    asn=int(row.get("asn") or 0),
                    organization=row.get("organization", ""),
                    source_latency_ms=parse_latency(row.get("source_latency_ms", "")),
                    baidu_delay_ms=int(row["baidu_delay_ms"]) if row.get("baidu_delay_ms") else None,
                    tested=parse_bool(row.get("tested", "")),
                    cn2=is_cn2,
                    cn2_evidence=row.get("cn2_evidence", ""),
                    trace_url=row.get("trace_url", ""),
                    trace_status=trace_status,
                    traced_at=row.get("traced_at", ""),
                    route_class=route_class,
                    route_evidence=row.get("route_evidence", ""),
                )
            except (KeyError, ValueError):
                continue
            state[candidate_key(candidate)] = candidate
    return state


def merge_state(candidates: list[Candidate], state: dict[str, Candidate]) -> None:
    for candidate in candidates:
        previous = state.get(candidate_key(candidate))
        if previous is None:
            continue
        candidate.baidu_delay_ms = previous.baidu_delay_ms
        candidate.tested = previous.tested
        candidate.cn2 = previous.cn2
        candidate.cn2_evidence = previous.cn2_evidence
        candidate.trace_url = previous.trace_url
        candidate.trace_status = previous.trace_status
        candidate.traced_at = previous.traced_at
        candidate.route_class = previous.route_class
        candidate.route_evidence = previous.route_evidence


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


def proxy_opener(proxy_url: str = "") -> urllib.request.OpenerDirector:
    if not proxy_url:
        return urllib.request.build_opener()
    handlers = [urllib.request.ProxyHandler({"http": proxy_url, "https": proxy_url})]
    return urllib.request.build_opener(*handlers)


def api_request(
    url: str,
    timeout: float,
    headers: dict[str, str] | None = None,
    proxy_url: str = "",
) -> dict:
    request = urllib.request.Request(url, headers=headers or {})
    with proxy_opener(proxy_url).open(request, timeout=timeout) as response:
        return json.load(response)


def load_proxy_pool(path: Path | None) -> list[str]:
    if path is None or not path.is_file():
        return []
    proxies: list[str] = []
    seen: set[str] = set()
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        value = line.strip()
        if not value or value.startswith("#"):
            continue
        if "://" not in value:
            value = f"http://{value}"
        parsed = urllib.parse.urlsplit(value)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname or not parsed.port:
            continue
        normalized = urllib.parse.urlunsplit(parsed)
        if normalized not in seen:
            seen.add(normalized)
            proxies.append(normalized)
    return proxies


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
    selected = candidates[: args.max_candidates] if args.max_candidates > 0 else candidates
    with ThreadPoolExecutor(max_workers=args.concurrency) as executor:
        futures = {
            executor.submit(test_candidate, candidate, args.timeout_ms): candidate
            for candidate in selected
        }
        for future in as_completed(futures):
            candidate = futures[future]
            candidate.tested = True
            candidate.baidu_delay_ms = future.result()
    return sorted(
        (item for item in selected if item.baidu_delay_ms is not None),
        key=lambda item: (item.baidu_delay_ms or 10**9, item.ip),
    )


def globalping_headers(token: str) -> dict[str, str]:
    headers = {"Content-Type": "application/json", "User-Agent": "cn2-proxy-finder/1.0"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def create_measurement(candidate: Candidate, token: str, proxy_url: str = "") -> str:
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
        with proxy_opener(proxy_url).open(request, timeout=20) as response:
            return str(json.load(response).get("id", ""))
    except urllib.error.HTTPError as error:
        if error.code in {402, 429}:
            return "quota"
        if error.code == 400:
            return "unavailable"
        raise


def wait_measurement(measurement_id: str, token: str, proxy_url: str = "") -> dict:
    endpoint = f"https://api.globalping.io/v1/measurements/{measurement_id}"
    deadline = time.monotonic() + 45
    last: dict = {}
    while time.monotonic() < deadline:
        try:
            last = api_request(endpoint, 20, globalping_headers(token), proxy_url)
        except (OSError, urllib.error.URLError, json.JSONDecodeError):
            time.sleep(2)
            continue
        if last.get("status") == "finished":
            break
        time.sleep(2)
    return last


def evaluate_trace(candidate: Candidate, measurement: dict) -> None:
    evidence: list[str] = []
    telecom_direct_evidence: list[str] = []
    for result in measurement.get("results", []):
        probe = result.get("probe", {})
        raw = result.get("result", {}).get("rawOutput", "")
        hops = sorted(set(re.findall(r"59\.43\.\d{1,3}\.\d{1,3}", raw)))
        telecom_asns = sorted(
            set(re.findall(r"AS(4134|4812|4813|4816|4817|4818|4819|58461)\b", raw, re.IGNORECASE))
        )
        if hops:
            location = probe.get("city") or probe.get("country") or str(probe.get("asn", "CN"))
            evidence.append(f"{location}: {', '.join(hops)}")
        elif telecom_asns:
            location = probe.get("city") or probe.get("country") or str(probe.get("asn", "CN"))
            telecom_direct_evidence.append(
                f"{location}: {', '.join(f'AS{asn}' for asn in telecom_asns)}"
            )
    candidate.cn2 = bool(evidence)
    candidate.cn2_evidence = "; ".join(evidence)
    if candidate.cn2:
        candidate.route_class = "cn2_gia" if candidate.asn in CN2_ASNS else "cn2_gt"
        candidate.route_evidence = candidate.cn2_evidence
    elif candidate.asn in TELECOM_163_ASNS or telecom_direct_evidence:
        candidate.route_class = "telecom_163_direct"
        candidate.route_evidence = "; ".join(telecom_direct_evidence) or f"目标 ASN: AS{candidate.asn}"
    else:
        candidate.route_class = "other"
        candidate.route_evidence = ""


def confirm_cn2(
    candidates: list[Candidate],
    args: argparse.Namespace,
    checkpoint: Callable[[], None] | None = None,
) -> None:
    proxy_pool = load_proxy_pool(getattr(args, "globalping_proxy_file", None))
    trace_targets = sorted(
        (
            candidate
            for candidate in candidates
            if candidate.trace_status in {"pending", "unavailable"}
        ),
        key=lambda item: (
            item.trace_status != "pending",
            bool(item.traced_at),
            item.traced_at,
            item.asn not in CN2_ASNS,
            item.baidu_delay_ms or 10**9,
        ),
    )
    if args.max_traces > 0:
        trace_targets = trace_targets[: args.max_traces]
    trace_concurrency = max(1, min(getattr(args, "trace_concurrency", 1), len(trace_targets) or 1))
    proxy_locks = [Lock() for _ in proxy_pool]
    proxy_quota = [False for _ in proxy_pool]
    checkpoint_lock = Lock()
    proxy_quota_lock = Lock()

    def save_checkpoint() -> None:
        if checkpoint:
            with checkpoint_lock:
                checkpoint()

    def trace_one(index: int, candidate: Candidate) -> str:
        try:
            measurement_id = "quota"
            measurement_proxy = ""
            attempts = len(proxy_pool) + (1 if args.globalping_token or not proxy_pool else 0)
            assigned_index = (index - 1) % len(proxy_pool) if proxy_pool else -1
            for attempt in range(max(1, attempts)):
                if args.globalping_token and attempt == 0:
                    measurement_proxy = ""
                    proxy_index = -1
                elif not proxy_pool:
                    measurement_proxy = ""
                    proxy_index = -1
                else:
                    proxy_offset = attempt - (1 if args.globalping_token else 0)
                    proxy_index = (assigned_index + proxy_offset) % len(proxy_pool)
                    measurement_proxy = proxy_pool[proxy_index]
                try:
                    if proxy_index >= 0:
                        with proxy_quota_lock:
                            if proxy_quota[proxy_index]:
                                continue
                        with proxy_locks[proxy_index]:
                            with proxy_quota_lock:
                                if proxy_quota[proxy_index]:
                                    continue
                            measurement_id = create_measurement(
                                candidate, args.globalping_token, measurement_proxy
                            )
                            if measurement_id == "quota":
                                with proxy_quota_lock:
                                    proxy_quota[proxy_index] = True
                    else:
                        measurement_id = create_measurement(
                            candidate, args.globalping_token, measurement_proxy
                        )
                except (OSError, urllib.error.URLError, json.JSONDecodeError):
                    if not proxy_pool:
                        raise
                    continue
                if measurement_id != "quota":
                    break
            if measurement_id == "quota":
                return "quota"
            if measurement_id == "unavailable":
                print(f"没有适合 {candidate.ip} 的路由探针，留待后续重试", file=sys.stderr)
                candidate.trace_status = "unavailable"
                candidate.traced_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                save_checkpoint()
                return "done"
            if not measurement_id:
                print(f"未取得 {candidate.ip} 的路由任务编号，保留待重试", file=sys.stderr)
                candidate.traced_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                save_checkpoint()
                return "done"
            candidate.trace_url = f"https://globalping.io?measurement={measurement_id}"
            measurement = wait_measurement(
                measurement_id, args.globalping_token, measurement_proxy
            )
            candidate.traced_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            if measurement.get("status") != "finished":
                print(f"路由追踪未完成 {candidate.ip}，保留待重试", file=sys.stderr)
                save_checkpoint()
                return "done"
            evaluate_trace(candidate, measurement)
            candidate.trace_status = candidate.route_class
            save_checkpoint()
            print(f"[{index}/{len(trace_targets)}] {candidate.ip}: CN2={candidate.cn2}")
            return "done"
        except (OSError, urllib.error.URLError, json.JSONDecodeError) as error:
            print(f"路由追踪失败 {candidate.ip}: {error}", file=sys.stderr)
            candidate.traced_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            save_checkpoint()
            return "done"

    quota_hits = 0
    with ThreadPoolExecutor(max_workers=trace_concurrency) as executor:
        futures = {
            executor.submit(trace_one, index, candidate): candidate
            for index, candidate in enumerate(trace_targets, 1)
        }
        for future in as_completed(futures):
            if future.result() == "quota":
                quota_hits += 1
    if quota_hits:
        print(
            f"Globalping 代理池配额不足，{quota_hits} 个候选保留待续扫",
            file=sys.stderr,
        )


def write_progress(candidates: list[Candidate], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(f"{path.suffix}.tmp")
    headers = list(Candidate.__dataclass_fields__)
    with temporary_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, lineterminator="\n")
        writer.writeheader()
        writer.writerows(asdict(item) for item in candidates)
    temporary_path.replace(path)


def write_outputs(all_candidates: list[Candidate], alive: list[Candidate], args: argparse.Namespace) -> None:
    args.output_dir.mkdir(parents=True, exist_ok=True)
    state_path = args.output_dir / "progress.csv"
    classified = [item for item in all_candidates if item.route_class in ROUTE_CLASSES]
    confirmed = [item for item in classified if item.cn2]
    traced = classified
    pending = [item for item in alive if item.trace_status in {"pending", "unavailable"}]
    headers = list(Candidate.__dataclass_fields__)
    write_progress(all_candidates, state_path)
    with (args.output_dir / "cn2.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, lineterminator="\n")
        writer.writeheader()
        writer.writerows(asdict(item) for item in confirmed)
    (args.output_dir / "cn2.json").write_text(
        json.dumps([asdict(item) for item in confirmed], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    for route_class in ROUTE_CLASSES:
        members = [item for item in classified if item.route_class == route_class]
        with (args.output_dir / f"{route_class}.csv").open(
            "w", encoding="utf-8", newline=""
        ) as handle:
            writer = csv.DictWriter(handle, fieldnames=headers, lineterminator="\n")
            writer.writeheader()
            writer.writerows(asdict(item) for item in members)
    report = [
        "# CN2 代理筛选报告",
        "",
        f"- CSV 地区候选数：{len(all_candidates)}",
        f"- 经百度前置测试数：{len(all_candidates) if args.max_candidates <= 0 else min(len(all_candidates), args.max_candidates)}",
        f"- 可用数：{len(alive)}",
        f"- 已完成路由追踪：{len(traced)}",
        f"- 待路由追踪：{len(pending)}",
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
    state_path = args.output_dir / "progress.csv"
    state = load_state(state_path)
    if not state:
        state = load_state(args.output_dir / "cn2.csv")
    merge_state(candidates, state)
    print(f"载入地区内 {len(candidates)} 个候选，恢复 {len(state)} 条进度")
    alive = validate_via_baidu(candidates, args)
    write_progress(candidates, state_path)
    pending = sum(
        candidate.trace_status in {"pending", "unavailable"}
        for candidate in alive
    )
    print(f"百度前置可用候选 {len(alive)} 个，待路由追踪 {pending} 个")
    confirm_cn2(alive, args, lambda: write_progress(candidates, state_path))
    write_outputs(candidates, alive, args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
