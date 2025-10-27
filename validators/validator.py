#!/usr/bin/env python3
import sys, re, json
from pathlib import Path

def load_front_matter(text: str):
    if not text.startswith('---'):
        raise ValueError("Front matter must start with '---' at the first line")
    # find closing '---' on its own line
    end_idx = text.find('\n---', 3)
    if end_idx == -1:
        raise ValueError("Closing '---' for front matter not found")
    block = text[3:end_idx].strip()
    # parse with yaml if available
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(block) or {}
        if not isinstance(data, dict):
            data = {}
        return data
    except Exception:
        data = {}
        for line in block.splitlines():
            if not line.strip() or line.strip().startswith('#'):
                continue
            if ':' in line:
                k, v = line.split(':', 1)
                data[k.strip()] = v.strip().strip('"\'')
        return data

def validate_md(file_path: str) -> int:
    text = Path(file_path).read_text(encoding='utf-8')
    fm = load_front_matter(text)
    errors, notes = [], []

    required = ["title", "vault_id", "glyphsig", "author", "date", "status", "predecessor", "successor", "checksum_sha256"]
    for k in required:
        if k not in fm or fm.get(k) in (None, "", []):
            errors.append(f"Missing required key: '{k}'")

    # version: optional, infer from title if absent
    ver = str(fm.get("version", "")).strip()
    if not ver:
        m = re.search(r'v(\d+\.\d+(?:\.\d+)?)', str(fm.get("title","")))
        if m:
            fm["version"] = m.group(1)
            notes.append(f"Note: Auto-inferred version = {fm['version']}")
        else:
            notes.append("Warning: 'version' missing and could not be inferred")

    chk = str(fm.get("checksum_sha256", ""))
    if not re.fullmatch(r'[0-9a-fA-F]{64}', chk):
        errors.append("Invalid 'checksum_sha256' (must be 64 hex chars)")

    for n in notes: print(n)
    if errors:
        for e in errors: print("Error:", e)
        return 1
    print("Validation passed.")
    print(json.dumps({"version": fm.get("version"), "title": fm.get("title")}, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validators/validator.py <file.md>")
        sys.exit(2)
    sys.exit(validate_md(sys.argv[1]))
