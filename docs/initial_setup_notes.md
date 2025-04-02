# Initial Setup & Troubleshooting Notes (Post-Poetry Migration)

This document outlines the steps taken to get the application running after migrating from Poetry to `uv` using `uvx migrate-to-uv`.

## 1. Initial State & Migration

- The project was migrated from Poetry using `uvx migrate-to-uv`.
- An initial attempt was made to set up a Python 3.9 environment using `uv venv --python=3.9` and `uv sync`.

## 2. Problem: `NotOpenSSLWarning`

- Running `python src/main.py --help` resulted in a `NotOpenSSLWarning` from `urllib3`.

    ```sh
    NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'.
    ```

- **Diagnosis:** Running `source .venv/bin/activate && which python && python -c "import ssl; print(ssl.OPENSSL_VERSION)"` confirmed the Python 3.9 interpreter being used by the virtual environment was linked against LibreSSL 2.8.3 (likely the system/Xcode Python), which is incompatible with `urllib3` v2+.
- **Workaround:** To get the application running quickly while respecting constraints against system-wide Python installs at the time, `urllib3` was pinned to `<2.0` in `pyproject.toml`, and `uv sync` was run. This resolved the SSL warning.

## 3. Problem: `TypeError` for `|` Type Hints

- After fixing the SSL warning, running `python src/main.py --help` resulted in `TypeError: unsupported operand type(s) for |: ...` errors.
- **Diagnosis:** The codebase used the `|` operator for type unions (e.g., `float | None`), which is a Python 3.10+ feature, but the environment was still Python 3.9.
- **Initial Fixes:** The `|` syntax was replaced with `typing.Union` syntax in `src/data/cache.py` and `src/data/models.py`.
- **Programmatic Attempt:** A script (`fix_unions.py`, now archived) was created and run to attempt replacing simple `Type | None` patterns across multiple files (`api.py`, `models.py`, agent files).
- **Further Errors:** The script didn't catch all cases, and the `TypeError` persisted, appearing next in `src/llm/models.py`.

## 4. Solution: Upgrade to Python 3.11 using `uv`

- It was confirmed that `uv` can manage Python installations directly (`uv python install`, `uv python list`).
- It was noted that Python 3.11 was already installed and managed by `uv`.
- **Decision:** Upgrade the project to Python 3.11 to natively support the `|` syntax and remove the need for workarounds.
- **Steps:**
    1. Modified `pyproject.toml`:
        - Changed `requires-python` to `~=3.11`.
        - Removed the `"urllib3<2.0"` pin.
        - Updated `[tool.black]` `target-version` to `['py311']`.
    2. Recreated the virtual environment using the `uv`-managed Python 3.11: `rm -rf .venv && uv venv --python 3.11 && source .venv/bin/activate && uv sync`.
    3. Verified successful execution with `python src/main.py --help`.
    4. Archived the `fix_unions.py` script: `mkdir -p archive && mv fix_unions.py archive/`.

## 5. Current Status

- The project now runs successfully on Python 3.11 managed by `uv`.
- The `NotOpenSSLWarning` and `TypeError` issues related to type hints are resolved.
- The project is ready for further modernization steps.
