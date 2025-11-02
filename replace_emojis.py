#!/usr/bin/env python3
"""
Script to replace emojis with Unicode characters that work in matplotlib
"""

from pathlib import Path

# Mapping of emojis to safe Unicode alternatives
EMOJI_REPLACEMENTS = {
    '✨': '*',           # Sparkles -> asterisk
    '🎯': '>>',          # Target -> arrows
    '💡': '[i]',         # Lightbulb -> info
    '📊': '[#]',         # Chart -> hash
    '📈': '[^]',         # Trending up -> caret
    '⚠️': '(!)',        # Warning -> exclamation in parens
    '☁️': '[~]',        # Cloud -> tilde
    '💻': '[PC]',        # Computer -> PC
    '⚖️': '[=]',        # Scale -> equals
    '🔵': '[O]',         # Blue circle -> O
    '🟢': '[O]',         # Green circle -> O
    '🔴': '[O]',         # Red circle -> O
    '🔢': '[#]',         # Numbers -> hash
}

def replace_emojis_in_file(filepath):
    """Replace emojis in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Replace each emoji
        for emoji, replacement in EMOJI_REPLACEMENTS.items():
            content = content.replace(emoji, replacement)

        # Check if anything changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            # Count replacements
            count = sum(original_content.count(emoji) for emoji in EMOJI_REPLACEMENTS.keys())
            print(f"  ✓ Replaced {count} emojis in {filepath}")
            return True
        else:
            print(f"  - No emojis in {filepath}")
            return False

    except Exception as e:
        print(f"  ✗ Error processing {filepath}: {e}")
        return False

def main():
    """Process all Python files"""
    # Focus on active presentation files
    files_to_process = [
        Path('presentations/vector_presentation.py'),
        Path('presentations/finetuning_presentation.py'),
        Path('presentations/quality_presentation.py'),
        Path('presentations/rag_presentation.py'),
        Path('presentations/neural_network_presentation.py'),
        Path('core/controls.py'),
        Path('presentation.py'),
    ]

    print(f"Processing {len(files_to_process)} files\n")

    updated_count = 0
    for filepath in files_to_process:
        if filepath.exists():
            if replace_emojis_in_file(filepath):
                updated_count += 1
        else:
            print(f"  ! File not found: {filepath}")

    print(f"\n✓ Complete! Replaced emojis in {updated_count} files")
    print("\nEmoji replacements:")
    for emoji, replacement in EMOJI_REPLACEMENTS.items():
        print(f"  {emoji} -> {replacement}")

if __name__ == '__main__':
    main()
