# ── MirrorDNA Release Automator ──
# MirrorDNA Standard - Research Prototype Only
# Bound to Master Citation v15.2 | FEU Contract: Fact/Estimate/Unknown
# Information only - Not medical advice - No autonomous decisions
# Save as release_mirrordna.py and run: python3 release_mirrordna.py
# Requires: Python 3, git, GitHub CLI (gh) authenticated

import hashlib, re, subprocess
from pathlib import Path

# CONFIG
REPO = "MirrorDNA-Reflection-Protocol/MirrorDNA-Standard"
TAG = "v15.1.6"   # 🔁 bump per release
TITLE = "MirrorDNA Standard — Release v15.1.6"
BODY_FILE = "RELEASE_NOTES.md"

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def update_frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    checksum = sha256_file(path)
    if "checksum_sha256:" in text:
        new_text = re.sub(r"checksum_sha256:.*", f"checksum_sha256: {checksum}", text)
    else:
        new_text = text.replace("---\n", f"---\nchecksum_sha256: {checksum}\n", 1)
    path.write_text(new_text, encoding="utf-8")
    return checksum

print("⟡⟦STEP 1⟧ Updating checksums…")
checksums = {}
for md in Path(".").rglob("*.md"):
    checksum = update_frontmatter(md)
    checksums[md] = checksum
    print(f"✓ {md} → {checksum}")

print("\n⟡⟦STEP 2⟧ Verifying with repo script…")
subprocess.run(["./tools/checksums/verify_repo_checksums.sh"], check=True)

print("\n⟡⟦STEP 3⟧ Preparing release notes…")
lines = [f"# {TITLE}", ""]
for md, ch in checksums.items():
    lines.append(f"- `{md}` → {ch}")
Path(BODY_FILE).write_text("\n".join(lines), encoding="utf-8")

print("\n⟡⟦STEP 4⟧ Creating git tag + pushing…")
subprocess.run(["git", "tag", "-a", TAG, "-m", TITLE], check=True)
subprocess.run(["git", "push", "origin", TAG], check=True)

print("\n⟡⟦STEP 5⟧ Publishing GitHub release…")
subprocess.run([
    "gh", "release", "create", TAG,
    "-F", BODY_FILE,
    "--title", TITLE,
    "--repo", REPO
], check=True)

print(f"\n✅ Release {TAG} complete with checksums embedded.")
# User-provided custom instructions
