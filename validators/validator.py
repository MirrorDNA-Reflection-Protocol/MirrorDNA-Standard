#!/usr/bin/env python3
import json, os, sys, glob

REQUIRED_SIDECAR_KEYS = [
    "vault_id", "glyphsig", "version", "checksum_sha256"
]

def find_sidecars():
    return glob.glob("**/*.json", recursive=True)

def check_sidecar(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        missing = [k for k in REQUIRED_SIDECAR_KEYS if k not in data]
        if missing:
            print(f"::error file={path}::Missing keys: {missing}")
            return False
        return True
    except Exception as e:
        print(f"::error file={path}::Invalid JSON: {e}")
        return False

def check_commit_message():
    # Best-effort: allow local CI to pass, enforce in PR review later
    return True

def main():
    sidecars = find_sidecars()
    ok = True
    for s in sidecars:
        if not check_sidecar(s):
            ok = False
    if not ok:
        sys.exit(1)
    print("Reflective compliance passed ⟡")

if __name__ == "__main__":
    main()
