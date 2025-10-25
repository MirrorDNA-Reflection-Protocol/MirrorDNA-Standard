#!/usr/bin/env python3
""" MirrorDNA — checksum helper
Computes SHA-256 over a JSON sidecar **excluding** the `checksum_sha256` field,
then writes the resulting hex digest back to `checksum_sha256` (in-place).

Usage:
  # Single file
  python scripts/generate_checksum.py examples/minimal-artifact.md.json

  # Many files
  python scripts/generate_checksum.py examples/*.json

  # Verify only (non-zero exit if mismatch)
  python scripts/generate_checksum.py --verify examples/*.json
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

REQUIRED_KEYS = ["vault_id", "glyphsig", "version", "checksum_sha256"]

def compute_checksum(obj: dict) -> str:
    """Compute sha256 of JSON with `checksum_sha256` blanked out, sorted keys."""
    # Make a shallow copy and blank out checksum
    data = dict(obj)
    data["checksum_sha256"] = ""
    blob = json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()

def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path: Path, obj: dict) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")

def verify(path: Path) -> bool:
    obj = load_json(path)
    missing = [k for k in REQUIRED_KEYS if k not in obj]
    if missing:
        print(f"::error file={path}::Missing required keys: {missing}")
        return False
    expected = compute_checksum(obj)
    ok = (obj.get("checksum_sha256", "") == expected)
    if not ok:
        print(f"::error file={path}::Checksum mismatch. expected={expected} actual={obj.get('checksum_sha256','')}")
    else:
        print(f"OK  {path}  sha256={expected}")
    return ok

def write(path: Path) -> bool:
    obj = load_json(path)
    missing = [k for k in REQUIRED_KEYS if k not in obj]
    if missing:
        print(f"::error file={path}::Missing required keys: {missing}")
        return False
    new_sum = compute_checksum(obj)
    obj["checksum_sha256"] = new_sum
    save_json(path, obj)
    print(f"WROTE  {path}  sha256={new_sum}")
    return True

def main():
    ap = argparse.ArgumentParser(description="MirrorDNA checksum helper")
    ap.add_argument("files", nargs="+", help="JSON sidecars to process (supports shell globs)")
    ap.add_argument("--verify", action="store_true", help="Verify only; do not write changes")
    args = ap.parse_args()

    ok_all = True
    for pattern in args.files:
        for path in sorted(Path().glob(pattern)):
            if not path.is_file():
                continue
            if args.verify:
                ok_all = verify(path) and ok_all
            else:
                ok_all = write(path) and ok_all
    sys.exit(0 if ok_all else 1)

if __name__ == "__main__":
    main()
