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
end

if [[ ${#ARGS[@]} -eq 0 ]]; then
  echo "Error: at least one file must be provided" >&2
  usage >&2
  exit 1
fi

mkdir -p "$(dirname "$OUTPUT")"
TIMESTAMP="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

for TARGET in "${ARGS[@]}"; do
  if [[ ! -f "$TARGET" ]]; then
    echo "Error: $TARGET is not a readable file" >&2
    exit 1
  fi

  CHECKSUM="$(sha256sum "$TARGET" | awk '{print $1}')"
  ENTRY="timestamp=$TIMESTAMP chain=$CHAIN file=$TARGET checksum_sha256=$CHECKSUM"
  if [[ -n "$TXID" ]]; then
    ENTRY+=" txid=$TXID"
  else
    ENTRY+=" txid=[pending]"
  fi

  {
    echo "# MirrorDNA blockchain anchor entry"
    echo "$ENTRY"
    echo ""
  } | tee -a "$OUTPUT"
done

echo "Anchor data appended to $OUTPUT"
if [[ -z "$TXID" ]]; then
  cat <<'NEXT_STEPS'
Next steps:
  1. Submit the checksum as transaction memo or calldata on your chosen chain.
  2. Once confirmed, re-run this script with --txid <transaction_hash> to
     replace the placeholder entry.
NEXT_STEPS
fi
