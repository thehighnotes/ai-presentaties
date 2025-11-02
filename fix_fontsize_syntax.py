#!/usr/bin/env python3
"""
Script to fix fontsize== syntax errors to fontsize=
"""

import re
from pathlib import Path

def fix_fontsize_syntax(filepath):
    """Fix fontsize== to fontsize= in a file"""
    print(f"Processing {filepath}...")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace fontsize== with fontsize=
    modified_content = content.replace('fontsize==', 'fontsize=')

    # Check if anything changed
    if content != modified_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(modified_content)

        # Count how many were fixed
        count = content.count('fontsize==')
        print(f"  ✓ Fixed {count} fontsize== errors in {filepath}")
        return True
    else:
        print(f"  - No syntax errors in {filepath}")
        return False

def main():
    """Process all Python files"""
    python_files = list(Path('presentations').glob('*.py'))
    python_files.extend(Path('core').glob('*.py'))

    print(f"Found {len(python_files)} Python files\n")

    updated_count = 0
    for filepath in python_files:
        if fix_fontsize_syntax(filepath):
            updated_count += 1

    print(f"\n✓ Complete! Fixed syntax errors in {updated_count} files")

if __name__ == '__main__':
    main()
