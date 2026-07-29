#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCANNER = ROOT / "scripts" / "check_public_safety.py"


def run_scan(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCANNER), "--root", str(path)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def main() -> int:
    clean = run_scan(ROOT)
    if clean.returncode != 0:
        print(clean.stdout)
        print("Expected the repository scan to pass.")
        return 1

    tmp = Path(tempfile.mkdtemp(prefix="awesome-tools-safety-test-"))
    try:
        (tmp / "README.md").write_text("safe public text\n", encoding="utf-8")
        (tmp / "leak.md").write_text(
            "\n".join(
                [
                    "path=" + "C:" + "\\Users\\" + "Dell" + "\\private",
                    "account=" + "wxid_" + "example123456",
                    "token=" + "gho_" + "A" * 32,
                ]
            ),
            encoding="utf-8",
        )
        (tmp / "manifest.csv").write_text("generated export metadata\n", encoding="utf-8")
        failed = run_scan(tmp)
        if failed.returncode == 0:
            print(failed.stdout)
            print("Expected synthetic private artifacts to fail the scan.")
            return 1
        required = {"windows-user-path", "wechat-account-id", "github-token", "export-manifest"}
        missing = {rule for rule in required if rule not in failed.stdout}
        if missing:
            print(failed.stdout)
            print(f"Missing expected rule hits: {sorted(missing)}")
            return 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("Public safety scanner tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
