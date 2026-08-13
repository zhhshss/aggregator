#!/usr/bin/env python3
"""合并并行 CN2 扫描进度并重新生成报告。"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path


def load_finder():
    path = Path(__file__).with_name("find_cn2.py")
    spec = importlib.util.spec_from_file_location("find_cn2", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--local", type=Path, required=True)
    parser.add_argument("--remote", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    finder = load_finder()
    local = finder.load_state(args.local)
    remote = finder.load_state(args.remote)
    candidates = list(finder.merge_completed_states(remote, local).values())
    finder.write_outputs(
        candidates,
        [item for item in candidates if item.baidu_delay_ms is not None],
        type("Args", (), {"output_dir": args.output_dir, "max_candidates": 0})(),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
