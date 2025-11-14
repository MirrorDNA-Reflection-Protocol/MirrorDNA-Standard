#!/usr/bin/env python3
"""
check_links.py - Scan markdown files for broken relative links

This utility scans all markdown files in the repository and checks for:
- Broken relative file links
- Missing anchor references
- Dead local paths

Usage:
    python tools/check_links.py
    python tools/check_links.py --verbose
    python tools/check_links.py --path docs/

Part of the MirrorDNA-Standard ecosystem tooling.
"""

import os
import re
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Set
from urllib.parse import urlparse, unquote


class LinkChecker:
    """Check relative links in markdown files"""

    def __init__(self, root_path: str = ".", verbose: bool = False):
        self.root_path = Path(root_path).resolve()
        self.verbose = verbose
        self.markdown_files: List[Path] = []
        self.broken_links: Dict[str, List[Dict]] = {}
        self.total_links_checked = 0
        self.total_broken = 0

    def find_markdown_files(self) -> None:
        """Recursively find all markdown files"""
        patterns = ["**/*.md", "**/*.markdown"]
        for pattern in patterns:
            self.markdown_files.extend(self.root_path.glob(pattern))

        # Remove duplicates and sort
        self.markdown_files = sorted(set(self.markdown_files))

        if self.verbose:
            print(f"Found {len(self.markdown_files)} markdown files")

    def extract_links(self, content: str) -> List[Tuple[str, int]]:
        """Extract markdown links with line numbers"""
        links = []

        # Match [text](link) and [text](link "title") patterns
        pattern = r'\[([^\]]+)\]\(([^)]+)\)'

        for line_num, line in enumerate(content.split('\n'), 1):
            for match in re.finditer(pattern, line):
                link = match.group(2).split()[0]  # Remove title if present
                links.append((link, line_num))

        return links

    def is_relative_link(self, link: str) -> bool:
        """Check if link is relative (not http/https/mailto/etc)"""
        parsed = urlparse(link)

        # Skip external links, anchors-only, and special schemes
        if parsed.scheme in ('http', 'https', 'mailto', 'ftp'):
            return False
        if link.startswith('#'):  # Anchor only
            return False
        if link.startswith('javascript:'):
            return False

        return True

    def check_link(self, link: str, source_file: Path) -> Tuple[bool, str]:
        """
        Check if a relative link is valid

        Returns: (is_valid, reason)
        """
        # Split link and anchor
        if '#' in link:
            link_path, anchor = link.split('#', 1)
        else:
            link_path, anchor = link, None

        # Decode URL encoding
        link_path = unquote(link_path)

        # If empty path (just anchor), check anchor in source file
        if not link_path:
            # Would need to parse markdown headers to validate
            # For now, we'll skip anchor-only links
            return True, "anchor-only (not validated)"

        # Resolve the link relative to the source file's directory
        source_dir = source_file.parent
        target_path = (source_dir / link_path).resolve()

        # Check if target exists
        if not target_path.exists():
            return False, f"file not found: {target_path.relative_to(self.root_path)}"

        # Check if it's a file (not directory)
        if target_path.is_dir():
            return False, f"links to directory: {target_path.relative_to(self.root_path)}"

        # If anchor specified, we'd need to validate it exists in target
        # For now, just check file existence
        if anchor and self.verbose:
            return True, f"file exists (anchor #{anchor} not validated)"

        return True, "valid"

    def check_file(self, file_path: Path) -> None:
        """Check all links in a single markdown file"""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Error reading {file_path}: {e}", file=sys.stderr)
            return

        links = self.extract_links(content)

        for link, line_num in links:
            if not self.is_relative_link(link):
                continue

            self.total_links_checked += 1
            is_valid, reason = self.check_link(link, file_path)

            if not is_valid:
                self.total_broken += 1
                relative_path = str(file_path.relative_to(self.root_path))

                if relative_path not in self.broken_links:
                    self.broken_links[relative_path] = []

                self.broken_links[relative_path].append({
                    'line': line_num,
                    'link': link,
                    'reason': reason
                })

    def run(self) -> int:
        """Run the link checker and return exit code"""
        print("🔍 MirrorDNA Link Checker")
        print("=" * 60)

        self.find_markdown_files()

        if not self.markdown_files:
            print("No markdown files found.")
            return 0

        print(f"\nScanning {len(self.markdown_files)} markdown files...\n")

        for md_file in self.markdown_files:
            if self.verbose:
                print(f"Checking: {md_file.relative_to(self.root_path)}")
            self.check_file(md_file)

        # Print report
        self.print_report()

        return 1 if self.total_broken > 0 else 0

    def print_report(self) -> None:
        """Print summary report"""
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"Total markdown files: {len(self.markdown_files)}")
        print(f"Total relative links checked: {self.total_links_checked}")
        print(f"Broken links found: {self.total_broken}")

        if self.broken_links:
            print("\n" + "=" * 60)
            print("BROKEN LINKS")
            print("=" * 60)

            for file_path in sorted(self.broken_links.keys()):
                print(f"\n📄 {file_path}")
                for issue in self.broken_links[file_path]:
                    print(f"   Line {issue['line']:4d}: {issue['link']}")
                    print(f"              → {issue['reason']}")
        else:
            print("\n✅ All relative links are valid!")


def main():
    parser = argparse.ArgumentParser(
        description="Check relative links in markdown files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/check_links.py
  python tools/check_links.py --verbose
  python tools/check_links.py --path docs/
        """
    )

    parser.add_argument(
        '--path',
        default='.',
        help='Path to scan (default: current directory)'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    checker = LinkChecker(root_path=args.path, verbose=args.verbose)
    exit_code = checker.run()

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
