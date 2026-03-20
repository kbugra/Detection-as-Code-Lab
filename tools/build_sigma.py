#!/usr/bin/env python3
"""Build Sigma rules into SIEM-ready artifacts."""

from __future__ import annotations

import subprocess
import sys
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RULES_DIR = ROOT / "rules" / "sigma"
SIGMA_WRAPPER = ROOT / "tools" / "run_sigma_cli.py"
BUILD_TARGETS = (
    ("splunk", ROOT / "build" / "splunk" / "windows_detections.spl"),
    ("lucene", ROOT / "build" / "elastic" / "windows_detections.txt"),
)


def run_build() -> int:
    if importlib.util.find_spec("sigma.cli.main") is None:
        print(
            "sigma CLI was not found in PATH. Install sigma-cli and the required plugins "
            "before running this build.",
            file=sys.stderr,
        )
        return 1

    for target, output_path in BUILD_TARGETS:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8", newline="\n") as handle:
            subprocess.run(
                [
                    sys.executable,
                    str(SIGMA_WRAPPER),
                    "convert",
                    "-t",
                    target,
                    "-p",
                    "sysmon",
                    str(RULES_DIR),
                ],
                check=True,
                stdout=handle,
                cwd=ROOT,
            )
        print(f"Built {target} output -> {output_path.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    sys.exit(run_build())
