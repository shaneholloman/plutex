# fix_unions.py
import re
import sys
import os
from pathlib import Path

# Safest initial regex: Target only the most common simple cases seen
# Target: `type | None` where type is float, str, or bool.
patterns = {
    r"\bfloat\s*\|\s*None\b": "Union[float, None]",
    r"\bstr\s*\|\s*None\b": "Union[str, None]",
    r"\bbool\s*\|\s*None\b": "Union[bool, None]",
    # NOTE: Does not handle dict | str | None or other complex cases yet.
}


def fix_file(filepath):
    """Reads a file, applies regex replacements, adds import if needed, and writes back."""
    p = Path(filepath)
    if not p.is_file():
        print(f"Error: File not found {filepath}", file=sys.stderr)
        return

    try:
        content = p.read_text()
        original_content = content
        needs_union_import = False

        for pattern, replacement in patterns.items():
            new_content, count = re.subn(pattern, replacement, content)
            if count > 0:
                content = new_content
                needs_union_import = (
                    True  # If any replacement happened, we need the import
                )

        # Check if import needs to be added
        has_union_import = "from typing import Union" in content or re.search(
            r"from typing import.*Union", content
        )

        if needs_union_import and not has_union_import:
            # Try to add import to an existing 'from typing import ...' line
            modified_import = False
            lines = content.splitlines()
            for i, line in enumerate(lines):
                if line.startswith("from typing import"):
                    if "Union" not in line:  # Avoid adding if already there somehow
                        lines[i] = line.replace("import", "import Union,", 1)
                        content = "\n".join(lines)
                        modified_import = True
                        break  # Assume only one typing import line needs modification

            # If no existing typing import line was found or modified, prepend
            if not modified_import:
                content = "from typing import Union\n" + content

        if content != original_content:
            print(f"Modifying {filepath}...")
            p.write_text(content)
        else:
            print(f"No changes needed for {filepath}.")

    except Exception as e:
        print(f"Error processing file {filepath}: {e}", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_unions.py <file1.py> [file2.py] ...", file=sys.stderr)
        sys.exit(1)

    filepaths = sys.argv[1:]
    print(f"Running script on: {filepaths}")
    for fp in filepaths:
        fix_file(fp)

    print("Script finished.")
