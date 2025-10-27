#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob

# Usage: tools/add_version_sidecars.sh 1.0.0
VER="${1:-1.0.0}"

paths=(kernel/**/*.json kernel/*.json **/*sidecar.json)
edited=0
for p in "${paths[@]}"; do
  if [[ -f "$p" ]]; then
    # check if file contains "version" at top-level (best-effort)
    if ! grep -q '"version"' "$p"; then
      tmp="$(mktemp)"
      # Prepend version safely for simple JSON objects
      # If jq is available, use it; otherwise, do a naive insert.
      if command -v jq >/dev/null 2>&1; then
        jq --arg v "$VER" '. + {version: $v}' "$p" > "$tmp" && mv "$tmp" "$p"
      else
        # naive: insert just after first '{'
        awk -v ver="$VER" 'BEGIN{added=0} {if(!added && $0 ~ /{[[:space:]]*$/){print; print "  \"version\": \"" ver "\","; added=1} else if (!added && $0 ~ /{.*}/) {sub(/{/, "{\n  \"version\": \"" ver "\","); print; added=1} else {print}}' "$p" > "$tmp"
        mv "$tmp" "$p"
      fi
      echo "Added version to: $p"
      edited=$((edited+1))
    fi
  fi
done

echo "Done. Files edited: $edited"
