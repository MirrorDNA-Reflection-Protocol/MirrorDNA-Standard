#!/usr/bin/env python3
"""
print_ecosystem.py - Display MirrorDNA ecosystem map

This utility reads ecosystem_map.json and displays the MirrorDNA constellation
in various formats (table, list, JSON, graph).

Usage:
    python tools/print_ecosystem.py
    python tools/print_ecosystem.py --format table
    python tools/print_ecosystem.py --format list
    python tools/print_ecosystem.py --format json
    python tools/print_ecosystem.py --filter role=spec
    python tools/print_ecosystem.py --filter status=public

Part of the MirrorDNA-Standard ecosystem tooling.
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Any


class EcosystemPrinter:
    """Display MirrorDNA ecosystem information"""

    def __init__(self, map_path: str = "tools/ecosystem_map.json"):
        self.map_path = Path(map_path)
        self.data: Dict[str, Any] = {}
        self.repositories: List[Dict] = []

    def load_map(self) -> bool:
        """Load ecosystem map from JSON file"""
        if not self.map_path.exists():
            print(f"Error: Ecosystem map not found at {self.map_path}", file=sys.stderr)
            return False

        try:
            with open(self.map_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
                self.repositories = self.data.get('repositories', [])
            return True
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {self.map_path}: {e}", file=sys.stderr)
            return False
        except Exception as e:
            print(f"Error loading {self.map_path}: {e}", file=sys.stderr)
            return False

    def filter_repositories(self, filter_spec: str) -> List[Dict]:
        """Filter repositories by key=value"""
        if not filter_spec:
            return self.repositories

        try:
            key, value = filter_spec.split('=', 1)
            key = key.strip()
            value = value.strip()

            filtered = [
                repo for repo in self.repositories
                if str(repo.get(key, '')).lower() == value.lower()
            ]
            return filtered
        except ValueError:
            print(f"Warning: Invalid filter format '{filter_spec}', use key=value", file=sys.stderr)
            return self.repositories

    def print_header(self) -> None:
        """Print ecosystem header"""
        version = self.data.get('ecosystem_version', 'unknown')
        updated = self.data.get('last_updated', 'unknown')

        print("⟡ MirrorDNA Ecosystem Map")
        print("=" * 80)
        print(f"Version: {version} | Last Updated: {updated}")
        print(f"Total Repositories: {len(self.repositories)}")
        print("=" * 80)

    def print_table(self, repositories: List[Dict] = None) -> None:
        """Print repositories as a formatted table"""
        if repositories is None:
            repositories = self.repositories

        self.print_header()

        # Define column widths
        col_widths = {
            'name': 30,
            'role': 12,
            'status': 10,
            'layer': 12,
            'compliance': 25
        }

        # Print header row
        print()
        print(f"{'NAME':<{col_widths['name']}} "
              f"{'ROLE':<{col_widths['role']}} "
              f"{'STATUS':<{col_widths['status']}} "
              f"{'LAYER':<{col_widths['layer']}} "
              f"{'COMPLIANCE':<{col_widths['compliance']}}")
        print("-" * 80)

        # Print repository rows
        for repo in repositories:
            name = repo.get('name', 'Unknown')[:col_widths['name']]
            role = repo.get('role', 'N/A')[:col_widths['role']]
            status = repo.get('status', 'N/A')[:col_widths['status']]
            layer = repo.get('layer', 'N/A')[:col_widths['layer']]
            compliance = repo.get('compliance_level', 'N/A')[:col_widths['compliance']]

            # Add status emoji
            status_emoji = {
                'public': '🌐',
                'private': '🔒',
                'planned': '📋'
            }.get(status.lower(), '❓')

            print(f"{name:<{col_widths['name']}} "
                  f"{role:<{col_widths['role']}} "
                  f"{status_emoji} {status:<{col_widths['status']-2}} "
                  f"{layer:<{col_widths['layer']}} "
                  f"{compliance:<{col_widths['compliance']}}")

        print()

    def print_list(self, repositories: List[Dict] = None) -> None:
        """Print repositories as a detailed list"""
        if repositories is None:
            repositories = self.repositories

        self.print_header()
        print()

        for i, repo in enumerate(repositories, 1):
            status_emoji = {
                'public': '🌐',
                'private': '🔒',
                'planned': '📋'
            }.get(repo.get('status', '').lower(), '❓')

            print(f"{i}. {status_emoji} {repo.get('name', 'Unknown')}")
            print(f"   Description: {repo.get('description', 'N/A')}")
            print(f"   Role: {repo.get('role', 'N/A')} | Layer: {repo.get('layer', 'N/A')}")
            print(f"   Status: {repo.get('status', 'N/A')} | Compliance: {repo.get('compliance_level', 'N/A')}")

            if repo.get('repository_url'):
                print(f"   URL: {repo['repository_url']}")
            elif repo.get('location'):
                print(f"   Location: {repo['location']}")

            if repo.get('key_features'):
                print(f"   Key Features: {', '.join(repo['key_features'][:3])}")

            print()

    def print_json(self, repositories: List[Dict] = None) -> None:
        """Print repositories as JSON"""
        if repositories is None:
            repositories = self.repositories

        output = {
            'ecosystem_version': self.data.get('ecosystem_version'),
            'last_updated': self.data.get('last_updated'),
            'repository_count': len(repositories),
            'repositories': repositories
        }

        print(json.dumps(output, indent=2))

    def print_stats(self) -> None:
        """Print ecosystem statistics"""
        self.print_header()

        # Count by role
        roles = {}
        for repo in self.repositories:
            role = repo.get('role', 'unknown')
            roles[role] = roles.get(role, 0) + 1

        # Count by status
        statuses = {}
        for repo in self.repositories:
            status = repo.get('status', 'unknown')
            statuses[status] = statuses.get(status, 0) + 1

        # Count by layer
        layers = {}
        for repo in self.repositories:
            layer = repo.get('layer', 'unknown')
            layers[layer] = layers.get(layer, 0) + 1

        print("\n📊 REPOSITORIES BY ROLE")
        print("-" * 40)
        for role, count in sorted(roles.items()):
            print(f"  {role:<20} {count:>3}")

        print("\n📊 REPOSITORIES BY STATUS")
        print("-" * 40)
        for status, count in sorted(statuses.items()):
            emoji = {'public': '🌐', 'private': '🔒', 'planned': '📋'}.get(status, '❓')
            print(f"  {emoji} {status:<18} {count:>3}")

        print("\n📊 REPOSITORIES BY LAYER")
        print("-" * 40)
        for layer, count in sorted(layers.items()):
            print(f"  {layer:<20} {count:>3}")

        # Print layer descriptions
        if 'ecosystem_layers' in self.data:
            print("\n📚 LAYER DESCRIPTIONS")
            print("-" * 80)
            for layer, desc in self.data['ecosystem_layers'].items():
                print(f"  {layer:<15} → {desc}")

        print()

    def print_graph(self) -> None:
        """Print a simple ASCII dependency graph"""
        self.print_header()
        print("\n🌐 DEPENDENCY GRAPH")
        print("-" * 80)

        # Build dependency map
        dep_map = {}
        for repo in self.repositories:
            name = repo.get('name')
            deps = repo.get('dependencies', [])
            dep_map[name] = deps

        # Print dependencies
        for repo_name in sorted(dep_map.keys()):
            deps = dep_map[repo_name]
            if deps:
                print(f"\n{repo_name}")
                for dep in deps:
                    print(f"  └─→ {dep}")
            else:
                print(f"\n{repo_name} (no dependencies)")

        print()


def main():
    parser = argparse.ArgumentParser(
        description="Display MirrorDNA ecosystem map",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/print_ecosystem.py
  python tools/print_ecosystem.py --format table
  python tools/print_ecosystem.py --format list
  python tools/print_ecosystem.py --format stats
  python tools/print_ecosystem.py --format graph
  python tools/print_ecosystem.py --filter role=spec
  python tools/print_ecosystem.py --filter status=public
        """
    )

    parser.add_argument(
        '--format',
        choices=['table', 'list', 'json', 'stats', 'graph'],
        default='table',
        help='Output format (default: table)'
    )

    parser.add_argument(
        '--filter',
        type=str,
        help='Filter repositories by key=value (e.g., role=spec, status=public)'
    )

    parser.add_argument(
        '--map',
        default='tools/ecosystem_map.json',
        help='Path to ecosystem map JSON file'
    )

    args = parser.parse_args()

    printer = EcosystemPrinter(map_path=args.map)

    if not printer.load_map():
        sys.exit(1)

    # Apply filter if specified
    repositories = printer.filter_repositories(args.filter) if args.filter else None

    # Print in requested format
    if args.format == 'table':
        printer.print_table(repositories)
    elif args.format == 'list':
        printer.print_list(repositories)
    elif args.format == 'json':
        printer.print_json(repositories)
    elif args.format == 'stats':
        printer.print_stats()
    elif args.format == 'graph':
        printer.print_graph()


if __name__ == '__main__':
    main()
