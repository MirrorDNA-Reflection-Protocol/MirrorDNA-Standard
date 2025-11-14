#!/usr/bin/env python3
"""
MirrorDNA Ecosystem Repository Lister

Simple script to print all repositories in the MirrorDNA ecosystem
with their roles and descriptions.

Usage:
    python scripts/list_repos.py
"""

def main():
    print("=" * 70)
    print("MirrorDNA Ecosystem Repositories")
    print("=" * 70)
    print()

    repos = [
        {
            "name": "MirrorDNA-Standard",
            "role": "Constitutional spec and semantic law",
            "layer": "Protocol"
        },
        {
            "name": "MirrorDNA",
            "role": "Protocol and persistence architecture",
            "layer": "Protocol"
        },
        {
            "name": "MirrorDNA-Lattice",
            "role": "Symbolic lattice architecture and reflection topology",
            "layer": "Foundation"
        },
        {
            "name": "ActiveMirrorOS",
            "role": "Product layer, intelligence that remembers",
            "layer": "Product"
        },
        {
            "name": "LingOS",
            "role": "Language-native operating system for reflection",
            "layer": "Language"
        },
        {
            "name": "LingOS-Private",
            "role": "Private LingOS development and experimental features",
            "layer": "Language"
        },
        {
            "name": "LingOS Vault Manager",
            "role": "Vault management system (inside LingOS repo)",
            "layer": "Language"
        },
        {
            "name": "TrustByDesign",
            "role": "Governance and safety patterns",
            "layer": "Governance"
        },
        {
            "name": "BeaconGlyphs",
            "role": "Visual and symbolic glyph system",
            "layer": "Visual"
        },
        {
            "name": "Glyphtrail",
            "role": "Continuity logs and interaction lineage",
            "layer": "Visual"
        },
        {
            "name": "AgentDNA",
            "role": "Agent personality and identity encoding",
            "layer": "Agent"
        },
        {
            "name": "SanatanaTech",
            "role": "R&D sandbox for experimental reflection tech",
            "layer": "R&D"
        },
        {
            "name": "MirrorDNA-Gauntlet",
            "role": "Coding challenge and competency testbed",
            "layer": "R&D"
        },
        {
            "name": "DominancePlaybook",
            "role": "Internal strategy codex (Sovereign Strategy Codex)",
            "layer": "Strategy"
        },
    ]

    # Group by layer
    layers = {}
    for repo in repos:
        layer = repo["layer"]
        if layer not in layers:
            layers[layer] = []
        layers[layer].append(repo)

    # Print by layer
    layer_order = ["Foundation", "Protocol", "Language", "Product",
                   "Governance", "Visual", "Agent", "R&D", "Strategy"]

    for layer in layer_order:
        if layer in layers:
            print(f"[{layer} Layer]")
            print("-" * 70)
            for repo in layers[layer]:
                print(f"  • {repo['name']:<30} — {repo['role']}")
            print()

    print("=" * 70)
    print(f"Total repositories: {len(repos)}")
    print("=" * 70)
    print()
    print("For more details:")
    print("  • Ecosystem overview: docs/ecosystem-overview.md")
    print("  • Stack map: docs/stack-map.md")
    print("  • Roadmap: docs/roadmap.md")
    print()


if __name__ == "__main__":
    main()
