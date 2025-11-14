#!/usr/bin/env python3
"""
Print MirrorDNA Ecosystem Map

Reads ecosystem_map.json and displays a formatted view of all repositories
grouped by role with visibility statistics.
"""

import json
import os
from collections import defaultdict
from pathlib import Path


def load_ecosystem_map():
    """Load the ecosystem map JSON file."""
    script_dir = Path(__file__).parent
    map_file = script_dir / "ecosystem_map.json"

    if not map_file.exists():
        print(f"Error: {map_file} not found!")
        return None

    with open(map_file, 'r') as f:
        return json.load(f)


def print_ecosystem(repos):
    """Print ecosystem map grouped by role."""
    # Group repos by role
    by_role = defaultdict(list)
    for repo in repos:
        by_role[repo['role']].append(repo)

    # Define role order for display
    role_order = ['spec', 'product', 'sdk', 'docs', 'playground', 'r&d']
    role_names = {
        'spec': 'Specifications',
        'product': 'Products',
        'sdk': 'SDKs',
        'docs': 'Documentation',
        'playground': 'Playgrounds & Examples',
        'r&d': 'Research & Development'
    }

    print("\n" + "=" * 80)
    print("MirrorDNA ECOSYSTEM MAP".center(80))
    print("=" * 80 + "\n")

    # Print repos grouped by role
    for role in role_order:
        if role not in by_role:
            continue

        repos_in_role = by_role[role]
        print(f"\n{role_names[role].upper()}")
        print("-" * 80)

        for repo in sorted(repos_in_role, key=lambda x: x['name']):
            visibility_icon = "🔓" if repo['visibility'] == "public" else "🔒"
            print(f"  {visibility_icon} {repo['name']:<40} [{repo['visibility']:>7}]")
            print(f"     {repo['description']}")
            print()

    # Print summary statistics
    print("\n" + "=" * 80)
    print("SUMMARY".center(80))
    print("=" * 80)

    public_count = sum(1 for r in repos if r['visibility'] == 'public')
    private_count = sum(1 for r in repos if r['visibility'] == 'private')
    total_count = len(repos)

    print(f"\n  Total Repositories: {total_count}")
    print(f"  Public:             {public_count}")
    print(f"  Private:            {private_count}")

    # Count by role
    print(f"\n  By Role:")
    for role in role_order:
        if role in by_role:
            count = len(by_role[role])
            print(f"    {role_names[role]:<30} {count:>3}")

    print("\n" + "=" * 80 + "\n")


def main():
    repos = load_ecosystem_map()
    if repos is None:
        return 1

    print_ecosystem(repos)
    return 0


if __name__ == "__main__":
    exit(main())
