#!/usr/bin/env python3
"""
Check Markdown Links

Walks through markdown files in the repository and checks for broken
relative links, reporting any issues found.
"""

import os
import re
from pathlib import Path
from urllib.parse import unquote, urlparse


def find_markdown_files(root_dir):
    """Find all markdown files in the repository."""
    markdown_files = []
    root_path = Path(root_dir)

    for file_path in root_path.rglob("*.md"):
        # Skip files in .git, node_modules, etc.
        if any(part.startswith('.') or part in ['node_modules', 'venv', '__pycache__']
               for part in file_path.parts):
            continue
        markdown_files.append(file_path)

    return sorted(markdown_files)


def extract_links(content):
    """Extract relative links from markdown content."""
    links = []

    # Match markdown links: [text](url)
    md_links = re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', content)
    for match in md_links:
        url = match.group(2)
        links.append((url, match.start()))

    # Match HTML links: <a href="url">
    html_links = re.finditer(r'<a\s+[^>]*href=["\']([^"\']+)["\']', content, re.IGNORECASE)
    for match in html_links:
        url = match.group(1)
        links.append((url, match.start()))

    # Match reference-style links: [text][ref] and [ref]: url
    ref_defs = re.finditer(r'^\[([^\]]+)\]:\s*(.+)$', content, re.MULTILINE)
    for match in ref_defs:
        url = match.group(2).strip()
        links.append((url, match.start()))

    return links


def is_relative_link(url):
    """Check if a URL is a relative link (not http/https/mailto/etc)."""
    if not url:
        return False

    # Remove anchor/fragment
    url_without_anchor = url.split('#')[0]
    if not url_without_anchor:
        return False  # It's just an anchor

    parsed = urlparse(url)
    # If it has a scheme (http, https, mailto, etc), it's not relative
    if parsed.scheme and parsed.scheme not in ['', 'file']:
        return False

    return True


def check_link_exists(source_file, link_url):
    """Check if a relative link target exists."""
    # Remove anchor/query
    url_path = link_url.split('#')[0].split('?')[0]
    if not url_path:
        return True  # Just an anchor or query, no path to check

    # Decode URL encoding
    url_path = unquote(url_path)

    source_dir = source_file.parent

    # Resolve the path
    if url_path.startswith('/'):
        # Absolute path from repo root
        # Find repo root (where .git is)
        repo_root = source_file
        while repo_root.parent != repo_root:
            if (repo_root / '.git').exists():
                break
            repo_root = repo_root.parent
        target_path = repo_root / url_path.lstrip('/')
    else:
        # Relative path from source file directory
        target_path = source_dir / url_path

    # Normalize the path
    try:
        target_path = target_path.resolve()
    except (OSError, RuntimeError):
        return False

    return target_path.exists()


def check_markdown_links(root_dir):
    """Check all markdown files for broken links."""
    markdown_files = find_markdown_files(root_dir)

    if not markdown_files:
        print("No markdown files found!")
        return

    print("\n" + "=" * 80)
    print("MARKDOWN LINK CHECK".center(80))
    print("=" * 80 + "\n")

    total_files = 0
    total_links = 0
    broken_links = []

    for md_file in markdown_files:
        try:
            content = md_file.read_text(encoding='utf-8')
        except Exception as e:
            print(f"⚠️  Error reading {md_file}: {e}")
            continue

        links = extract_links(content)
        relative_links = [(url, pos) for url, pos in links if is_relative_link(url)]

        if not relative_links:
            continue

        total_files += 1
        file_has_broken = False

        for url, position in relative_links:
            total_links += 1
            if not check_link_exists(md_file, url):
                if not file_has_broken:
                    print(f"\n📄 {md_file.relative_to(root_dir)}")
                    file_has_broken = True

                # Find line number
                line_num = content[:position].count('\n') + 1
                print(f"   ❌ Line {line_num}: {url}")
                broken_links.append((md_file, line_num, url))

    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY".center(80))
    print("=" * 80)
    print(f"\n  Total markdown files scanned:    {len(markdown_files)}")
    print(f"  Files with relative links:       {total_files}")
    print(f"  Total relative links checked:    {total_links}")
    print(f"  Broken links found:              {len(broken_links)}")

    if broken_links:
        print(f"\n  ⚠️  {len(broken_links)} broken link(s) found!")
    else:
        print(f"\n  ✅ All links are valid!")

    print("\n" + "=" * 80 + "\n")

    return len(broken_links)


def main():
    # Get repository root (parent of tools directory)
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    broken_count = check_markdown_links(repo_root)
    return 1 if broken_count > 0 else 0


if __name__ == "__main__":
    exit(main())
