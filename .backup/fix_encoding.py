#!/usr/bin/env python3
"""
Fix encoding issues in finetuning.py
Replaces corrupted emoji characters with proper Unicode
"""

# Read the file
with open('finetuning.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Count original corrupted characters
corrupted_count = sum(content.count(old) for old in ['ð', 'Ã', 'â'])

# Define replacements - corrupted to correct
replacements = [
    # Emojis
    ('ðŸ§ ', '🧠'),  # Brain
    ('âš™ï¸', '⚙️'),  # Gear
    ('âœ¨', '✨'),  # Sparkles
    ('ðŸ"š', '📚'),  # Books
    ('ðŸŒ', '🌍'),  # Globe
    ('ðŸ'»', '💻'),  # Computer
    ('ðŸ"¬', '🔬'),  # Microscope
    ('ðŸ"–', '📖'),  # Open book
    ('ðŸ'¡', '💡'),  # Light bulb
    ('ðŸ"¥', '📥'),  # Inbox
    ('ðŸ"¤', '📤'),  # Outbox
    ('ðŸ'¾', '💾'),  # Floppy disk
    ('ðŸŽ¯', '🎯'),  # Dart
    ('ðŸ"Š', '📊'),  # Chart
    ('ðŸ"ˆ', '📈'),  # Chart up
    ('ðŸŽ‰', '🎉'),  # Party
    ('ðŸŽ¬', '🎬'),  # Clapper
    ('ðŸ"', '🔍'),  # Magnifying glass
    ('â˜ï¸', '☁️'),  # Cloud
    ('ðŸ'»', '💻'),  # Laptop
    # Symbols
    ('â€¢', '•'),    # Bullet
    ('â†'', '→'),    # Right arrow
    ('âœ"', '✓'),    # Check mark
    ('â†', '←'),     # Left arrow
    ('â"', '❓'),    # Question mark
    ('âŒ', '❌'),    # Cross mark
    ('âœ…', '✅'),   # Check mark button
    ('âš ï¸', '⚠️'),  # Warning
    ('â¸', '⏸'),     # Pause
    # Math symbols
    ('â„'', 'ℒ'),     # Script L (Loss function)
    ('Î£', 'Σ'),     # Sigma
    ('Å·', 'ŷ'),     # y-hat
    ('âˆ‡', '∇'),    # Nabla (gradient)
    ('Î±', 'α'),     # Alpha
    ('â‰ˆ', '≈'),    # Approximately equal
    # Text
    ('Ã©', 'é'),     # e with accent
]

# Apply all replacements
for old, new in replacements:
    content = content.replace(old, new)

# Write back
with open('finetuning.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed encoding issues in finetuning.py")
print(f"✅ Applied {len(replacements)} replacement patterns")
print(f"✅ Original corrupted character occurrences: ~{corrupted_count}")
