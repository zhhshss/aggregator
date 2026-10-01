#!/usr/bin/env python3
"""从 zip.cm.edu.kg 实时拉取 Cloudflare 反代 IP 列表并生成扫描输入 CSV。

数据源：https://zip.cm.edu.kg/ip.zip
压缩包内按端口/国家分文件，例如 443/HK.txt 每行一个 IP。
本脚本只负责实时拉取并输出与 find_cn2.py 兼容的 CSV，不写死任何 IP。
"""

from __future__ import annotations

import argparse
import csv
import io
import ipaddress
import sys
import urllib.request
import zipfile
from pathlib import Path

DEFAULT_ZIP_URL = "https://zip.cm.edu.kg/ip.zip"
DEFAULT_PORT = 443
# 默认地区与 find-cn2.yml 的 workflow_dispatch 默认值保持一致
DEFAULT_REGIONS = "HK,JP,SG,TW,KR,US,GB,DE,NL,FR,CA,AU,IN,TH,VN,MY,ID,PH"

CSV_HEADERS = [
    "IP数据来源",
    "IP地址",
    "端口号",
    "TLS",
    "数据中心",
    "IP位置",
    "地区",
    "城市",
    "地区(中文)",
    "出站IP位置",
    "城市(中文)",
    "国旗",
    "网络延迟",
    "出站IP",
    "出站IP类型",
    "IPS类型",
    "ASN号码",
    "ASN组织",
    "访问协议",
    "TLS版本",
    "SNI",
    "HTTP版本",
    "WARP",
    "Gateway",
    "RBI",
    "密钥交换",
    "时间戳",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zip-url", default=DEFAULT_ZIP_URL, help="IP zip 下载地址")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="只提取该端口目录")
    parser.add_argument(
        "--regions",
        default=DEFAULT_REGIONS,
        help="国家代码，逗号分隔；特殊值 ALL 表示提取全部",
    )
    parser.add_argument("--output", required=True, type=Path, help="输出 CSV 路径")
    parser.add_argument("--timeout", type=float, default=30.0, help="下载超时秒数")
    return parser.parse_args()


def normalize_regions(value: str) -> set[str] | None:
    parts = {item.strip().upper() for item in value.split(",") if item.strip()}
    if not parts or "ALL" in parts:
        return None
    return parts


def iter_port_entries(zf: zipfile.ZipFile, port: int):
    prefix = f"{port}/"
    for name in zf.namelist():
        if not name.startswith(prefix) or not name.lower().endswith(".txt"):
            continue
        country = name[len(prefix) : -4].strip().upper()
        if not country:
            continue
        yield country, name


def is_valid_ip(value: str) -> bool:
    try:
        ipaddress.ip_address(value)
    except ValueError:
        return False
    return True


def build_row(ip: str, port: int, country: str) -> dict[str, str]:
    row = {header: "" for header in CSV_HEADERS}
    row.update(
        {
            "IP数据来源": "zip.cm.edu.kg",
            "IP地址": ip,
            "端口号": str(port),
            "TLS": "true",
            "数据中心": country,
            "IP位置": country,
            "地区": "Asia Pacific" if country in {"HK", "JP", "SG", "TW", "KR"} else "",
            "城市": "",
            "地区(中文)": "",
            "出站IP位置": "",
            "城市(中文)": "",
            "国旗": "",
            "网络延迟": "",
            "出站IP": "",
            "出站IP类型": "IPv4" if ":" not in ip else "IPv6",
            "IPS类型": "",
            "ASN号码": "",
            "ASN组织": "",
            "访问协议": "https",
            "TLS版本": "TLSv1.3",
            "SNI": "",
            "HTTP版本": "http/1.1",
            "WARP": "off",
            "Gateway": "off",
            "RBI": "off",
            "密钥交换": "",
            "时间戳": "",
        }
    )
    return row


def main() -> int:
    args = parse_args()
    regions = normalize_regions(args.regions)

    request = urllib.request.Request(
        args.zip_url,
        headers={"User-Agent": "cf-ip-fetcher/1.0 (+https://github.com/)"},
    )
    try:
        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            payload = response.read()
    except Exception as exc:  # noqa: BLE001
        print(f"下载 {args.zip_url} 失败: {exc}", file=sys.stderr)
        return 1

    try:
        zf = zipfile.ZipFile(io.BytesIO(payload))
    except zipfile.BadZipFile as exc:
        print(f"非法 zip 文件: {exc}", file=sys.stderr)
        return 1

    seen: set[tuple[str, int]] = set()
    rows: list[dict[str, str]] = []
    for country, name in sorted(iter_port_entries(zf, args.port)):
        if regions is not None and country not in regions:
            continue
        text = zf.read(name).decode("utf-8", errors="ignore")
        for line in text.splitlines():
            ip = line.strip()
            if not ip or not is_valid_ip(ip):
                continue
            key = (ip, args.port)
            if key in seen:
                continue
            seen.add(key)
            rows.append(build_row(ip, args.port, country))

    if not rows:
        print("未提取到任何 IP", file=sys.stderr)
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_HEADERS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"已写入 {args.output}，共 {len(rows)} 条记录，地区: {sorted(regions) if regions else 'ALL'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
