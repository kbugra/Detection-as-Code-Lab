#!/usr/bin/env python3
"""Run sigma-cli with a repo-local cache and ATT&CK data source."""

from __future__ import annotations

import sys
from pathlib import Path

from sigma.data import mitre_attack, mitre_d3fend


ROOT = Path(__file__).resolve().parents[1]
CACHE_DIR = ROOT / ".cache" / "pysigma" / "mitre_attack"
ATTACK_STUB = ROOT / "tools" / "mitre_attack_stub.json"
D3FEND_CACHE_DIR = ROOT / ".cache" / "pysigma" / "mitre_d3fend"
D3FEND_STUB = ROOT / "tools" / "mitre_d3fend_stub.json"


def main() -> int:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    D3FEND_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    mitre_attack.set_cache_dir(str(CACHE_DIR))
    mitre_attack.set_url(str(ATTACK_STUB))
    mitre_d3fend.set_cache_dir(str(D3FEND_CACHE_DIR))
    mitre_d3fend.set_url(str(D3FEND_STUB))

    from sigma.cli.main import main as sigma_main

    return sigma_main()


if __name__ == "__main__":
    sys.exit(main())
