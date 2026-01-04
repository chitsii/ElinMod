#!/usr/bin/env python3
"""
Scenario files cleanup script:
1. Remove all .wait() calls
2. Fix undefined flags
"""

import re
from pathlib import Path

SCENARIOS_DIR = Path(__file__).parent / 'common' / 'scenarios'

def remove_waits(content):
    """Remove .wait() lines"""
    # Remove entire lines containing just .wait(...) \
    content = re.sub(r'^\s*\.wait\([^)]*\)\s*\\\s*\n', '', content, flags=re.MULTILINE)
    # Fix double backslash continuation (\ \) -> single backslash (\)
    content = re.sub(r'\\ \\', r'\\', content)
    return content

def fix_flags(filename, content):
    """Fix flag values according to flags.md"""

    if '05_1_lily_experiment.py' in filename:
        # Remove undefined flag
        content = re.sub(
            r'^\s*\.set_flag\("sukutsu_lily_experiment_done", 1\)\s*\\\s*\n',
            '',
            content,
            flags=re.MULTILINE
        )

    elif '05_2_zek_steal_bottle.py' in filename:
        # Fix bottle_choice: 0 -> "refused", 1 -> "swapped"
        content = content.replace(
            '.set_flag("chitsii.arena.player.bottle_choice", 0)',
            '.set_flag("chitsii.arena.player.bottle_choice", "refused")'
        )
        content = content.replace(
            '.set_flag("chitsii.arena.player.bottle_choice", 1)',
            '.set_flag("chitsii.arena.player.bottle_choice", "swapped")'
        )

    elif '06_2_zek_steal_soulgem.py' in filename:
        # Fix kain_soul_choice: 0 -> "returned", 1 -> "sold"
        content = content.replace(
            '.set_flag("chitsii.arena.player.kain_soul_choice", 0)',
            '.set_flag("chitsii.arena.player.kain_soul_choice", "returned")'
        )
        content = content.replace(
            '.set_flag("chitsii.arena.player.kain_soul_choice", 1)',
            '.set_flag("chitsii.arena.player.kain_soul_choice", "sold")'
        )

    return content

def process_file(filepath):
    """Process a single file"""
    print(f"Processing: {filepath.name}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove waits
    content = remove_waits(content)

    # Fix flags
    content = fix_flags(filepath.name, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  [OK] Completed: {filepath.name}")

def main():
    files_to_process = [
        '05_1_lily_experiment.py',
        '05_2_zek_steal_bottle.py',
        '06_2_zek_steal_soulgem.py',
        '08_lily_private.py',
        '09_balgas_training.py',
    ]

    for filename in files_to_process:
        filepath = SCENARIOS_DIR / filename
        if filepath.exists():
            process_file(filepath)
        else:
            print(f"  [ERROR] Not found: {filename}")

    print("\nAll files processed!")

if __name__ == '__main__':
    main()
