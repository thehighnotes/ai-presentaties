#!/usr/bin/env python3
"""
Script to scale all hardcoded font sizes in presentation files for 4K displays
Multiplies all fontsize values by 2.0x
"""

import re
import glob
from pathlib import Path

def scale_fontsize(match):
    """Replace fontsize value with 2x scaled version"""
    param = match.group(1)
    original_size = int(match.group(2))
    scaled_size = int(original_size * 2.0)
    return f'{param}={scaled_size}'

def process_file(filepath):
    """Process a single Python file to scale font sizes"""
    print(f"Processing {filepath}...")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all fontsize parameters (fontsize=XX or font_size=XX)
    # Match fontsize=number or fontsize = number
    pattern = r'(fontsize\s*=\s*)(\d+)'

    modified_content = re.sub(pattern, scale_fontsize, content)

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

if __name__ == '__main__':
    main()
