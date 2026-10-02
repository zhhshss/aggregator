#!/usr/bin/env python3
"""按国家测试已确认 CN2 IP，并同步 Cloudflare DNS。"""

from __future__ import annotations

import argparse
import csv
import ipaddress
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

BAIDU_PROXY = "http://cloudnproxy.baidu.com:443"
BAIDU_HEADERS = (
    "Host: ascdn.baidu.com",
    "Proxy-Connection: Keep-Alive",
    "X-T5-Auth: 1951164069",
    "User-Agent: okhttp/3.11.0 SP-engine/2.71.0 Dalvik/2.1.0 "
    "(Linux; U; Android 9; HMA-AL00 Build/PQ3B.190801.002) "
    "baiduboxapp/13.33.0.11 (Baidu; P1 9)",
)
TEST_HOST = "cp.cloudflare.com"
TEST_URL = f"https://{TEST_HOST}/"
ROUTE_PRIORITY = ("cn2_gia", "cn2_gt", "telecom_163_direct")


@dataclass(frozen=True)
class Candidate:
    ip: str
    country: str
    delay_ms: int
    route_class: str


def hostname(route_class: str, country: str, zone: str) -> str:
    prefix = route_class.replace("_", "-")
    return f"{prefix}-{country.lower()}.{zone}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--zone", required=True)
    parser.add_argument("--prefix", default="cn2")
    parser.add_argument("--report", default=Path("cn2-dns/status.json"), type=Path)
    parser.add_argument("--timeout", type=int, default=12)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--cf-api-token", default=os.getenv("CF_API_TOKEN", ""))
    parser.add_argument("--cf-api-key", default=os.getenv("CF_API_KEY", ""))
    parser.add_argument("--cf-api-email", default=os.getenv("CF_API_EMAIL", ""))
    return parser.parse_args()


def load_candidates(path: Path) -> dict[str, list[Candidate]]:
    grouped: dict[str, list[Candidate]] = {}
    seen: set[tuple[str, str]] = set()
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            try:
                ip = str(ipaddress.ip_address(row["ip"].strip()))
                country = row["country"].strip().upper()
                delay = int(row.get("baidu_delay_ms") or 10**9)
                route_class = row.get("route_class", "")
            except (KeyError, ValueError):
                continue
            if route_class not in ROUTE_PRIORITY or not country or (country, ip) in seen:
                continue
            seen.add((country, ip))
            grouped.setdefault(country, []).append(Candidate(ip, country, delay, route_class))
    for candidates in grouped.values():
        candidates.sort(
            key=lambda item: (ROUTE_PRIORITY.index(item.route_class), item.delay_ms, item.ip)
        )
    return grouped


def test_ip(ip: str, timeout: int) -> tuple[bool, int | None]:
    base_command = [
        "curl",
        "--silent",
        "--show-error",
        "--output",
        "/dev/null",
        "--connect-timeout",
        str(timeout),
        "--max-time",
        str(timeout + 3),
        "--proxy",
        BAIDU_PROXY,
    ]
    for header in BAIDU_HEADERS:
        base_command.extend(("--proxy-header", header))
    for _ in range(3):
        command = base_command + [
            "--connect-to",
            f"{TEST_HOST}:443:{ip}:443",
            "--write-out",
            "%{http_code} %{time_total}",
            TEST_URL,
        ]
        try:
            result = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
                timeout=timeout + 8,
            )
            status, elapsed = result.stdout.strip().split()
            if result.returncode == 0 and status in {"200", "204"}:
                return True, max(1, round(float(elapsed) * 1000))
        except (OSError, ValueError, subprocess.TimeoutExpired):
            continue
    return False, None


def choose_ip(candidates: list[Candidate], current_ip: str | None, timeout: int) -> tuple[Candidate | None, int | None, list[dict]]:
    ordered = candidates
    if current_ip:
        ordered = sorted(candidates, key=lambda item: (item.ip != current_ip, item.delay_ms, item.ip))
    attempts: list[dict] = []
    for candidate in ordered:
        alive, delay = test_ip(candidate.ip, timeout)
        attempts.append(
            {
                "ip": candidate.ip,
                "route_class": candidate.route_class,
                "alive": alive,
                "delay_ms": delay,
            }
        )
        if alive:
            return candidate, delay, attempts
    return None, None, attempts


def choose_preferred_ip(
    candidates: list[Candidate], current_ip: str | None, timeout: int
) -> tuple[Candidate | None, int | None, list[dict]]:
    """综合域名先保证最高可用档位；同档位内保持当前 IP。"""
    attempts: list[dict] = []
    for route_class in ROUTE_PRIORITY:
        tier = [item for item in candidates if item.route_class == route_class]
        tier_current_ip = current_ip if any(item.ip == current_ip for item in tier) else None
        chosen, delay, tier_attempts = choose_ip(tier, tier_current_ip, timeout)
        attempts.extend(tier_attempts)
        if chosen:
            return chosen, delay, attempts
    return None, None, attempts


class Cloudflare:
    def __init__(self, args: argparse.Namespace) -> None:
        if args.cf_api_token:
            self.headers = {"Authorization": f"Bearer {args.cf_api_token}"}
        elif args.cf_api_key and args.cf_api_email:
            self.headers = {
                "X-Auth-Key": args.cf_api_key,
                "X-Auth-Email": args.cf_api_email,
            }
        else:
            raise ValueError("缺少 Cloudflare API 凭据")
        self.headers["Content-Type"] = "application/json"
        self.base = "https://api.cloudflare.com/client/v4"

    def request(self, method: str, path: str, payload: dict | None = None) -> dict:
        data = json.dumps(payload).encode() if payload is not None else None
        request = urllib.request.Request(
            self.base + path,
            data=data,
            headers=self.headers,
            method=method,
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                result = json.load(response)
        except urllib.error.HTTPError as error:
            detail = error.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Cloudflare HTTP {error.code}: {detail}") from error
        if not result.get("success"):
            raise RuntimeError(f"Cloudflare API 失败: {result.get('errors')}")
        return result

    def zone_id(self, zone: str) -> str:
        encoded = urllib.parse.quote(zone)
        result = self.request("GET", f"/zones?name={encoded}&status=active")
        zones = result.get("result", [])
        if len(zones) != 1:
            raise RuntimeError(f"无法唯一定位 Cloudflare Zone: {zone}")
        return zones[0]["id"]

    def record(self, zone_id: str, name: str) -> dict | None:
        encoded = urllib.parse.quote(name)
        result = self.request("GET", f"/zones/{zone_id}/dns_records?type=A&name={encoded}")
        records = result.get("result", [])
        return records[0] if records else None

    def managed_records(self, zone_id: str, prefix: str, zone: str) -> dict[str, dict]:
        result = self.request("GET", f"/zones/{zone_id}/dns_records?type=A&per_page=500")
        pattern = re.compile(
            rf"^{re.escape(prefix)}-([a-z]{{2}})\.{re.escape(zone)}$",
            re.IGNORECASE,
        )
        records: dict[str, dict] = {}
        for record in result.get("result", []):
            match = pattern.match(record.get("name", ""))
            if match:
                records[match.group(1).upper()] = record
        return records

    def route_records(self, zone_id: str, zone: str) -> dict[tuple[str, str], dict]:
        result = self.request("GET", f"/zones/{zone_id}/dns_records?type=A&per_page=500")
        patterns = {
            route_class: re.compile(
                rf"^{re.escape(route_class.replace('_', '-'))}-([a-z]{{2}})\.{re.escape(zone)}$",
                re.IGNORECASE,
            )
            for route_class in ROUTE_PRIORITY
        }
        records: dict[tuple[str, str], dict] = {}
        for record in result.get("result", []):
            for route_class, pattern in patterns.items():
                match = pattern.match(record.get("name", ""))
                if match:
                    records[(route_class, match.group(1).upper())] = record
                    break
        return records

    def upsert_a(self, zone_id: str, name: str, ip: str, record: dict | None) -> str:
        payload = {"type": "A", "name": name, "content": ip, "ttl": 60, "proxied": False}
        if record:
            if record.get("content") == ip and record.get("proxied") is False:
                return "unchanged"
            self.request("PUT", f"/zones/{zone_id}/dns_records/{record['id']}", payload)
            return "updated"
        self.request("POST", f"/zones/{zone_id}/dns_records", payload)
        return "created"


def main() -> int:
    args = parse_args()
    grouped = load_candidates(args.input)
    if not grouped:
        raise SystemExit("CN2 结果为空；保留现有 DNS，不做变更")
    cloudflare = None if args.dry_run else Cloudflare(args)
    zone_id = "" if args.dry_run else cloudflare.zone_id(args.zone)
    managed = {} if args.dry_run else cloudflare.managed_records(zone_id, args.prefix, args.zone)
    route_records = {} if args.dry_run else cloudflare.route_records(zone_id, args.zone)
    results: list[dict] = []
    failures = 0
    for country in sorted(set(grouped) | set(managed)):
        name = f"{args.prefix}-{country.lower()}.{args.zone}"
        record = managed.get(country) if not args.dry_run else None
        current_ip = record.get("content") if record else None
        candidates = grouped.get(country, [])
        if current_ip and all(item.ip != current_ip for item in candidates):
            candidates = [Candidate(current_ip, country, 10**9, "current"), *candidates]
        chosen, delay, attempts = choose_preferred_ip(candidates, current_ip, args.timeout)
        if chosen is None:
            failures += 1
            action = "kept-current" if current_ip else "no-record"
            selected_ip = current_ip
        elif args.dry_run:
            action = "dry-run"
            selected_ip = chosen.ip
        else:
            action = cloudflare.upsert_a(zone_id, name, chosen.ip, record)
            selected_ip = chosen.ip
        print(f"{country}: {name} -> {selected_ip or '-'} ({action})")
        tier_updates: dict[str, dict] = {}
        for route_class in ROUTE_PRIORITY:
            tier_candidates = [item for item in candidates if item.route_class == route_class]
            tier_record = route_records.get((route_class, country))
            tier_current_ip = tier_record.get("content") if tier_record else None
            if tier_current_ip and all(item.ip != tier_current_ip for item in tier_candidates):
                tier_candidates = [
                    Candidate(tier_current_ip, country, 10**9, route_class),
                    *tier_candidates,
                ]
            tier_chosen, tier_delay, tier_attempts = choose_ip(
                tier_candidates, tier_current_ip, args.timeout
            )
            tier_name = hostname(route_class, country, args.zone)
            if tier_chosen is None:
                tier_action = "kept-current" if tier_current_ip else "no-record"
                tier_selected_ip = tier_current_ip
            elif args.dry_run:
                tier_action = "dry-run"
                tier_selected_ip = tier_chosen.ip
            else:
                tier_action = cloudflare.upsert_a(
                    zone_id, tier_name, tier_chosen.ip, tier_record
                )
                tier_selected_ip = tier_chosen.ip
            print(
                f"{country}/{route_class}: {tier_name} -> "
                f"{tier_selected_ip or '-'} ({tier_action})"
            )
            tier_updates[route_class] = {
                "hostname": tier_name,
                "previous_ip": tier_current_ip,
                "selected_ip": tier_selected_ip,
                "delay_ms": tier_delay,
                "action": tier_action,
                "attempts": tier_attempts,
            }
        results.append(
            {
                "country": country,
                "hostname": name,
                "previous_ip": current_ip,
                "selected_ip": selected_ip,
                "delay_ms": delay,
                "route_class": chosen.route_class if chosen else None,
                "action": action,
                "attempts": attempts,
                "tiers": tier_updates,
            }
        )
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if failures:
        print(f"警告：{failures} 个国家当前没有可用候选，未覆盖已有 DNS", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
