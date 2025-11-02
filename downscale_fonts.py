#!/usr/bin/env python3
"""
Script to downscale all hardcoded font sizes in presentation files
Reduces font sizes by 25% (multiplies by 0.75) for better readability
"""

import re
import glob
from pathlib import Path


def downscale_fontsize(match):
    """Replace fontsize value with 0.75x scaled version (25% reduction)"""
    param = match.group(1)
    original_size = int(match.group(2))
    scaled_size = int(original_size * 0.75)
    return f'{param}{scaled_size}'


def process_file(filepath):
    """Process a single Python file to downscale font sizes"""
    print(f"Processing {filepath}...")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all fontsize parameters (fontsize=XX)
    # Match fontsize=number or fontsize = number
    pattern = r'(fontsize\s*=\s*)(\d+)'

    modified_content = re.sub(pattern, downscale_fontsize, content)

    # Check if anything changed
    if content != modified_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        print(f"  ✓ Updated {filepath}")
        return True
    else:
        print(f"  - No changes needed for {filepath}")
        return False


def main():
    """Process all presentation files"""
    # Get all Python files in presentations directory
    presentation_files = list(Path('presentations').glob('*.py'))

    print(f"Found {len(presentation_files)} presentation files\n")

    updated_count = 0
    for filepath in presentation_files:
        if process_file(filepath):
            updated_count += 1

    print(f"\n✓ Complete! Updated {updated_count} files")
    print(f"Font sizes have been reduced by 25% for better readability")


if __name__ == '__main__':
    main()
