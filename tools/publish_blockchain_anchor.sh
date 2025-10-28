#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: tools/publish_blockchain_anchor.sh [options] <file> [<file> ...]

Compute SHA-256 hashes for canonical MirrorDNA artifacts and log the
information needed to notarize them on a public blockchain. The script
produces a human-auditable entry you can paste into your preferred
anchoring tool (e.g., Ethereum/Polygon transaction memo services).

Options:
  -c, --chain <name>     Name of the blockchain (default: ethereum)
  -o, --output <path>    File to append anchor metadata to
                         (default: tools/checksums/blockchain_anchors.log)
  -t, --txid <hash>      Optional transaction hash to record alongside the
                         checksum. If omitted, the entry will include a
                         placeholder so you can update it later once the
                         transaction is confirmed.
  -h, --help             Show this help message and exit

Examples:
  ./tools/publish_blockchain_anchor.sh spec/Reflection_Chain_Manifest_v1.0.md
  ./tools/publish_blockchain_anchor.sh -c polygon -t 0xabc... 00_MASTER_CITATION.md
USAGE
}

CHAIN="ethereum"
OUTPUT="tools/checksums/blockchain_anchors.log"
TXID=""

PYTHON_BIN=""
if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "Error: python3 (or python) is required to run this script" >&2
  exit 1
fi

compute_checksum() {
  local target="$1"
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$target" | awk '{print $1}'
  elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$target" | awk '{print $1}'
  else
    echo "Error: neither sha256sum nor shasum is available" >&2
    exit 1
  fi
}

relative_path() {
  local target="$1"
  local root
  if root=$(git rev-parse --show-toplevel 2>/dev/null); then
    "$PYTHON_BIN" - "$root" "$target" <<'PY'
import os, sys
root, path = sys.argv[1:3]
print(os.path.relpath(os.path.abspath(path), root))
PY
  else
    "$PYTHON_BIN" - "$target" <<'PY'
import os, sys
print(os.path.relpath(os.path.abspath(sys.argv[1]), os.getcwd()))
PY
  fi
}

ARGS=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    -c|--chain)
      [[ $# -ge 2 ]] || { echo "Error: missing value for $1" >&2; exit 1; }
      CHAIN="$2"
      shift 2
      ;;
    -o|--output)
      [[ $# -ge 2 ]] || { echo "Error: missing value for $1" >&2; exit 1; }
      OUTPUT="$2"
      shift 2
      ;;
    -t|--txid)
      [[ $# -ge 2 ]] || { echo "Error: missing value for $1" >&2; exit 1; }
      TXID="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      while [[ $# -gt 0 ]]; do
        ARGS+=("$1")
        shift
      done
      ;;
    -*)
      echo "Error: unknown option $1" >&2
      usage >&2
      exit 1
      ;;
    *)
      ARGS+=("$1")
      shift
      ;;
  esac
done

if [[ ${#ARGS[@]} -eq 0 ]]; then
  echo "Error: at least one file must be provided" >&2
  usage >&2
  exit 1
fi

mkdir -p "$(dirname "$OUTPUT")"
COMMIT="$(git rev-parse HEAD 2>/dev/null || echo '[Unknown — update not fetched]')"

update_placeholder() {
  local output="$1"
  local file_line="$2"
  local checksum_line="$3"
  local txid="$4"

  [[ -f "$output" ]] || return 1

  "$PYTHON_BIN" - "$output" "$file_line" "$checksum_line" "$txid" <<'PY'
import pathlib, re, sys
output, file_line, checksum_line, txid = sys.argv[1:5]
path = pathlib.Path(output)
text = path.read_text()
pattern = (
    r"(# MirrorDNA blockchain anchor entry\n"
    r"timestamp=.*\n"
    r"chain=.*\n"
    + re.escape(file_line) + r"\n"
    + re.escape(checksum_line) + r"\n"
    r"txid=)\[pending\](\ncommit=.*\n---\n\n)"
)
replacement = r"\g<1>" + txid + r"\g<2>"
new_text, count = re.subn(pattern, replacement, text)
if count:
    path.write_text(new_text)
    sys.exit(0)
sys.exit(1)
PY
  local status=$?
  return $status
}

for TARGET in "${ARGS[@]}"; do
  if [[ ! -f "$TARGET" ]]; then
    echo "Error: $TARGET is not a readable file" >&2
    exit 1
  fi

  RELATIVE="$(relative_path "$TARGET")"
  CHECKSUM="$(compute_checksum "$TARGET")"
  FILE_LINE="file=$RELATIVE"
  CHECKSUM_LINE="checksum_sha256=$CHECKSUM"

  if [[ -n "$TXID" ]] && update_placeholder "$OUTPUT" "$FILE_LINE" "$CHECKSUM_LINE" "$TXID"; then
    echo "Updated pending entry for $RELATIVE with txid $TXID"
    continue
  fi

  if [[ -n "$TXID" ]]; then
    echo "Warning: no pending anchor entry matched $RELATIVE ($CHECKSUM). Appending a fresh record." >&2
  fi

  TIMESTAMP="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

  {
    echo "# MirrorDNA blockchain anchor entry"
    echo "timestamp=$TIMESTAMP"
    echo "chain=$CHAIN"
    echo "$FILE_LINE"
    echo "$CHECKSUM_LINE"
    if [[ -n "$TXID" ]]; then
      echo "txid=$TXID"
    else
      echo "txid=[pending]"
    fi
    echo "commit=$COMMIT"
    echo "---"
    echo
  } >> "$OUTPUT"

  if [[ -n "$TXID" ]]; then
    echo "Anchor entry recorded for $RELATIVE with txid $TXID"
  else
    echo "Anchor entry recorded for $RELATIVE (txid pending)"
  fi

done

echo "Anchor data written to $OUTPUT"
if [[ -z "$TXID" ]]; then
  cat <<'NEXT_STEPS'
Next steps:
  1. Submit the checksum as transaction memo or calldata on your chosen chain.
  2. Once confirmed, re-run this script with --txid <transaction_hash> to
     replace the placeholder entry.
NEXT_STEPS
fi
