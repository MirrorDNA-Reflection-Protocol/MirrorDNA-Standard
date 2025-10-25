#!/usr/bin/env python3
import sys, re, json

def load_front_matter(text: str):
    # Extract YAML-like front matter between leading --- blocks
    start = text.find('---')
    if start != 0:
        raise ValueError("Front matter must start with '---' at the first line")
    end = text.find('\n---', 3)
    if end == -1:
        raise ValueError("Closing '---' for front matter not found")
    block = text[3:end].strip()
    # Try PyYAML if available
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(block) or {}
        if not isinstance(data, dict):
            data = {}
        return data
    except Exception:
        # Fallback: very simple key: value parser (scalars only)
        data = {}
        for line in block.splitlines():
            if not line.strip() or line.strip().startswith('#'):
                continue
            if ':' in line:
                k, v = line.split(':', 1)
                k = k.strip()
                v = v.strip().strip('"\'')
                data[k] = v
        return data

def validate(file_path: str) -> int:
    text = Path(file_path).read_text(encoding='utf-8')
    fm = load_front_matter(text)
    errors = []
    notes = []

    required_keys = ["title", "vault_id", "glyphsig", "author", "date", "status", "predecessor", "successor", "checksum_sha256"]
    for k in required_keys:
        if k not in fm or fm.get(k) in (None, "", []):
            errors.append(f"Missing required key: '{k}'")

    # Version handling: optional; infer from title if absent
    if "version" not in fm or not str(fm.get("version")).strip():
        m = re.search(r'v(\d+\.\d+(?:\.\d+)?)', str(fm.get("title", "")), re.IGNORECASE)
        if m:
            fm["version"] = m.group(1)
            notes.append(f"Note: Auto-inferred version = {fm['version']}")
        else:
            notes.append("Warning: 'version' missing and could not be inferred from title")

    # checksum sanity (64 hex chars)
    chk = str(fm.get("checksum_sha256", ""))
    if not re.fullmatch(r'[0-9a-fA-F]{64}', chk):
        errors.append("Invalid 'checksum_sha256' (must be 64 hex chars)")

    # print results
    for n in notes:
        print(n)
    if errors:
        for e in errors:
            print("Error:", e)
        return 1
    print("Validation passed.")
    # Emit minimal JSON for tooling if needed
    print(json.dumps({"version": fm.get("version"), "title": fm.get("title")}, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    from pathlib import Path
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = "00_MASTER_CITATION.md"
    try:
        exit_code = validate(target)
        sys.exit(exit_code)
    except Exception as e:
        print("Error:", str(e))
        sys.exit(1)
