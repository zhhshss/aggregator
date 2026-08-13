#!/usr/bin/env python3
"""通过百度代理对指定线路档位执行 Cloudflare 下载测速。"""

from __future__ import annotations

import argparse
import csv
import ipaddress
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass
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
TEST_HOST = "speed.cloudflare.com"


@dataclass(frozen=True)
class Result:
    ip: str
    port: int
    country: str
    datacenter: str
    route_class: str
    status: str
    speed_mbps: float | None
    speed_mbytes_s: float | None
    bytes_downloaded: int
    elapsed_seconds: float | None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", default=Path("cn2-speedtest"), type=Path)
    parser.add_argument("--route-class", default="cn2_gt")
    parser.add_argument("--bytes", type=int, default=2_097_152)
    parser.add_argument("--timeout", type=int, default=45)
    parser.add_argument("--concurrency", type=int, default=10)
    return parser.parse_args()


def load_candidates(path: Path, route_class: str = "cn2_gt") -> list[dict[str, str]]:
    candidates: list[dict[str, str]] = []
    seen: set[tuple[str, int]] = set()
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            try:
                ip = str(ipaddress.ip_address(row["ip"].strip()))
                port = int(row["port"])
            except (KeyError, ValueError):
                continue
            if row.get("route_class") != route_class or (ip, port) in seen:
                continue
            seen.add((ip, port))
            candidates.append(
                {
                    "ip": ip,
                    "port": str(port),
                    "country": row.get("country", ""),
                    "datacenter": row.get("datacenter", ""),
                    "route_class": row.get("route_class", ""),
                }
            )
    return candidates


def speedtest(row: dict[str, str], size: int, timeout: int) -> Result:
    command = [
        "curl",
        "--silent",
        "--show-error",
        "--output",
        "/dev/null",
        "--connect-timeout",
        str(timeout),
        "--max-time",
        str(timeout + 5),
        "--proxy",
        BAIDU_PROXY,
    ]
    for header in BAIDU_HEADERS:
        command.extend(("--proxy-header", header))
    command.extend(
        (
            "--connect-to",
            f"{TEST_HOST}:443:{row['ip']}:{row['port']}",
            "--write-out",
            "%{http_code}\t%{size_download}\t%{time_total}\t%{speed_download}",
            f"https://{TEST_HOST}/__down?bytes={size}",
        )
    )
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout + 10,
        )
        status, downloaded, elapsed, bytes_per_second = completed.stdout.strip().split("\t")
        downloaded_bytes = int(downloaded)
        speed = float(bytes_per_second)
        successful = completed.returncode == 0 and status == "200" and downloaded_bytes == size
        return Result(
            row["ip"],
            int(row["port"]),
            row["country"],
            row["datacenter"],
            row["route_class"],
            "ok" if successful else "failed",
            round(speed * 8 / 1_000_000, 3) if successful else None,
            round(speed / 1_000_000, 3) if successful else None,
            downloaded_bytes,
            round(float(elapsed), 3),
        )
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return Result(
            row["ip"], int(row["port"]), row["country"], row["datacenter"],
            row["route_class"],
            "failed", None, None, 0, None,
        )


def write_outputs(
    results: list[Result], output_dir: Path, size: int, route_class: str = "cn2_gt"
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    ordered = sorted(
        results,
        key=lambda item: (
            item.status != "ok",
            -(item.speed_mbps or 0),
            item.country,
            item.ip,
        ),
    )
    with (output_dir / f"{route_class}_speedtest.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=Result.__dataclass_fields__, lineterminator="\n")
        writer.writeheader()
        writer.writerows(asdict(item) for item in ordered)

    successful = [item for item in ordered if item.status == "ok"]
    lines = [
        f"# {route_class} Cloudflare 下载测速",
        "",
        f"- 测速候选：{len(ordered)}",
        f"- 成功：{len(successful)}",
        f"- 失败：{len(ordered) - len(successful)}",
        f"- 单次下载：{size} bytes",
        "",
        "| 排名 | IP | 国家 | 数据中心 | Mbps | MB/s | 耗时 | 状态 |",
        "|---:|---|---|---|---:|---:|---:|---|",
    ]
    for index, item in enumerate(ordered, 1):
        lines.append(
            f"| {index} | `{item.ip}` | {item.country} | {item.datacenter} | "
            f"{item.speed_mbps if item.speed_mbps is not None else '-'} | "
            f"{item.speed_mbytes_s if item.speed_mbytes_s is not None else '-'} | "
            f"{item.elapsed_seconds if item.elapsed_seconds is not None else '-'} s | {item.status} |"
        )
    (output_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    candidates = load_candidates(args.input, args.route_class)
    if not candidates:
        raise SystemExit(f"没有 {args.route_class} 候选")
    results: list[Result] = []
    with ThreadPoolExecutor(max_workers=max(1, args.concurrency)) as executor:
        futures = {
            executor.submit(speedtest, candidate, args.bytes, args.timeout): candidate
            for candidate in candidates
        }
        for index, future in enumerate(as_completed(futures), 1):
            result = future.result()
            results.append(result)
            print(
                f"[{index}/{len(candidates)}] {result.ip}: "
                f"{result.speed_mbytes_s if result.speed_mbytes_s is not None else '-'} MB/s"
            )
    write_outputs(results, args.output_dir, args.bytes, args.route_class)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
