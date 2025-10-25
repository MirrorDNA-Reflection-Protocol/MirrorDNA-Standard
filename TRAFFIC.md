# Adoption & Usage Signals (Owner‑Only)

This repo is privacy‑respecting. We do not fingerprint users. To estimate usage:

## 1) GitHub Traffic (owner only)
- Repo → Insights → Traffic (clones, views, unique visitors).
- API: `GET /repos/{owner}/{repo}/traffic/clones` and `/traffic/views`.

## 2) Release Downloads (optional)
- If you attach assets to Releases, GitHub counts per‑asset downloads.

## 3) Short‑Link Redirects (optional)
- Use a redirect (e.g., GitHub Pages or a worker) to the raw Master Citation. Count hits server‑side.

## 4) Voluntary Check‑In
- Add an Issue template: “I’m using MirrorDNA” with non‑identifying checkboxes.

## 5) Beacon (opt‑in only)
- Provide a 1x1 image URL in README for **contributors only**. Do **not** force on end users.

Principle: **Trust by Design** — no dark patterns, no hidden tracking.
