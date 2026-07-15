#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Upload aggregator outputs to Cloudflare R2 (S3-compatible)."""

from __future__ import annotations

import argparse
import mimetypes
import os
import sys
from pathlib import Path

import boto3
from botocore.client import Config
from botocore.exceptions import BotoCoreError, ClientError

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

DEFAULT_FILES = [
    "clash.yaml",
    "v2ray.txt",
    "singbox.json",
    "subscribes.txt",
    "mainstream-clash.yaml",
    "mainstream-list.txt",
    "valid-domains.txt",
]


def content_type(path: Path) -> str:
    if path.suffix.lower() in {".yaml", ".yml"}:
        return "text/yaml; charset=utf-8"
    if path.suffix.lower() == ".json":
        return "application/json; charset=utf-8"
    if path.suffix.lower() == ".txt":
        return "text/plain; charset=utf-8"
    guess, _ = mimetypes.guess_type(str(path))
    return guess or "application/octet-stream"


def main() -> int:
    ap = argparse.ArgumentParser(description="Upload files to Cloudflare R2")
    ap.add_argument("--endpoint", default=os.environ.get("R2_ENDPOINT", ""))
    ap.add_argument("--access-key", default=os.environ.get("R2_ACCESS_KEY_ID", ""))
    ap.add_argument("--secret-key", default=os.environ.get("R2_SECRET_ACCESS_KEY", ""))
    ap.add_argument("--bucket", default=os.environ.get("R2_BUCKET", "aggregator"))
    ap.add_argument("--prefix", default=os.environ.get("R2_PREFIX", "").strip("/"))
    ap.add_argument("--public-base", default=os.environ.get("R2_PUBLIC_BASE", "").rstrip("/"))
    ap.add_argument("--dir", default=str(DATA), help="local directory containing outputs")
    ap.add_argument("files", nargs="*", help="filenames under --dir; default common outputs")
    args = ap.parse_args()

    missing = [n for n, v in [
        ("R2_ENDPOINT/--endpoint", args.endpoint),
        ("R2_ACCESS_KEY_ID/--access-key", args.access_key),
        ("R2_SECRET_ACCESS_KEY/--secret-key", args.secret_key),
        ("R2_BUCKET/--bucket", args.bucket),
    ] if not v]
    if missing:
        print("missing required config:", ", ".join(missing), file=sys.stderr)
        return 2

    names = args.files or DEFAULT_FILES
    directory = Path(args.dir)
    # also accept files from CWD / data if present
    candidates = []
    for name in names:
        p = directory / name
        if p.is_file():
            candidates.append(p)
            continue
        alt = ROOT / "data" / name
        if alt.is_file():
            candidates.append(alt)

    if not candidates:
        print("no local output files found to upload", file=sys.stderr)
        return 0

    s3 = boto3.client(
        "s3",
        endpoint_url=args.endpoint,
        aws_access_key_id=args.access_key,
        aws_secret_access_key=args.secret_key,
        region_name="auto",
        config=Config(signature_version="s3v4"),
    )

    uploaded = []
    for path in candidates:
        key = f"{args.prefix}/{path.name}" if args.prefix else path.name
        body = path.read_bytes()
        try:
            s3.put_object(
                Bucket=args.bucket,
                Key=key,
                Body=body,
                ContentType=content_type(path),
                CacheControl="public, max-age=60",
            )
        except (BotoCoreError, ClientError) as e:
            print(f"upload failed {path.name}: {e}", file=sys.stderr)
            return 1
        url = f"{args.public_base}/{key}" if args.public_base else key
        print(f"uploaded s3://{args.bucket}/{key} ({len(body)} bytes) -> {url}")
        uploaded.append((key, url, len(body)))

    # index file for convenience
    lines = ["# aggregator outputs", ""]
    for key, url, size in uploaded:
        lines.append(f"- {key} ({size} bytes): {url}")
    index_body = ("\n".join(lines) + "\n").encode()
    index_key = f"{args.prefix}/index.txt" if args.prefix else "index.txt"
    try:
        s3.put_object(
            Bucket=args.bucket,
            Key=index_key,
            Body=index_body,
            ContentType="text/plain; charset=utf-8",
            CacheControl="public, max-age=60",
        )
        print(f"uploaded index -> {args.public_base + '/' + index_key if args.public_base else index_key}")
    except Exception as e:
        print(f"index upload skipped: {e}", file=sys.stderr)

    print(f"done, files={len(uploaded)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
