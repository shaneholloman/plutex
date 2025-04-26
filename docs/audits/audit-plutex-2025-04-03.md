# plutex Project Audit: Modernization & PyPI Readiness (2025-04-03)

**Objective:** Assess the plutex project's current state and outline steps required to meet 2025 standards, ensure compatibility with Python 3.10-3.13, prepare for PyPI publication with automated testing/deployment and secure practices, and consolidate tooling with Ruff.

## 1. Executive Summary

plutex is an innovative AI-powered trading system proof-of-concept with a multi-agent architecture. While functional, the project requires significant modernization to meet current standards, ensure broader Python compatibility (3.10-3.13), and become a dependable PyPI package. Key findings indicate outdated dependencies (especially Langchain), a need for code quality improvements (acknowledged in README), incomplete PyPI metadata, lack of automated testing/deployment, and opportunities to consolidate tooling using Ruff. Security practices around API key handling also require review. This audit recommends a phased approach focusing on establishing robust testing and CI/CD, migrating to Ruff, updating dependencies incrementally, refactoring code, completing PyPI requirements, and enhancing security and documentation.

## 2. Current State Analysis

- **Project Goal:** Educational proof-of-concept for an AI-powered trading system using multiple agents (e.g., Warren Buffett, Cathie Wood) to generate trading signals.
- **Technology Stack:**
  - Python: Currently requires `~=3.11`.
  - Package Management: `uv`.
  - Core Libraries: `langchain`, `langgraph`, `pandas`, `numpy`, `matplotlib`.
  - External APIs: Requires keys for LLMs (Anthropic, OpenAI, Google, Groq, Deepseek) and Financial Datasets, managed via `.env` and `python-dotenv`.
  - Development Tools: `pytest`, `black`, `isort`, `flake8`.
- **Structure:** Source code in `src/` with distinct modules for agents (`agents/`), data (`data/`), graph state (`graph/`), LLM interaction (`llm/`), tools (`tools/`), utilities (`utils/`), main entry point (`main.py`), and backtester (`backtester.py`). Documentation in `docs/`.
- **Acknowledged Issues:** The `README.md` explicitly states: "> Project is in REALLY poor state. Python code needs to be cleaned up and modernized."

## 3. Python 3.10-3.13 Compatibility Assessment

- **Challenge:** Current `requires-python = "~=3.11"` specification is narrow. Expanding to 3.10-3.13 requires verification across four minor versions.
- **Dependency Impact:** Pinned dependencies (e.g., `langchain==0.3.0`, `pandas<3`) must be checked for compatibility across the target Python range. Newer versions of dependencies might drop support for older Python versions (like 3.10).
- **Code Impact:** The codebase needs scanning for:
  - Syntax or features introduced _after_ 3.10 that are currently used.
  - Features deprecated _before_ or _in_ 3.13.
  - The presence of `archive/fix_unions.py` suggests previous compatibility work (likely related to `|` union syntax introduced in 3.10).
- **Recommendations:**
  - Implement a test matrix in CI (see Section 5) to run tests against Python 3.10, 3.11, 3.12, and 3.13.
  - Update `requires-python` in `pyproject.toml` to `>=3.10, <3.14` once compatibility is confirmed.
  - Adjust `tool.black.target-version` (or equivalent Ruff setting) to reflect the supported range.

## 4. Dependency Modernization (2025 Standards)

- **Challenge:** Several dependencies have restrictive upper version caps (e.g., `langchain==0.3.0`, `langchain-openai<0.4`, `pandas<3`, `matplotlib<4`). The AI/LLM ecosystem (Langchain, Langgraph) evolves rapidly, meaning current versions are likely significantly outdated, missing features, performance improvements, and bug fixes.
- **Risk:** Sticking to old versions increases technical debt, hinders adoption of new capabilities, and may pose security risks if vulnerabilities are discovered in older packages. Breaking changes are highly likely during updates, especially for Langchain/Langgraph.
- **Recommendations:**
  - Plan for **incremental** dependency updates. Start with less complex libraries, testing thoroughly after each update.
  - Tackle Langchain/Langgraph updates carefully, consulting their migration guides and expecting significant code changes.
  - Remove upper version caps where feasible, relying on `uv.lock` for reproducible environments, or use compatible release specifiers (e.g., `~=1.2`, `>=1.2,<2.0`).
  - Utilize `uv`'s dependency resolution capabilities.
  - Consider using GitHub's Dependabot for ongoing vulnerability scanning (check `uv` documentation for any native auditing features as they emerge).
  - Define a strategy for regularly reviewing and updating dependencies.

## 5. PyPI Publication Readiness & Automation

- **Metadata (`pyproject.toml`):**
  - _Present:_ `name`, `version`, `description`, `authors`, `readme`, `requires-python`.
  - _Needs Adding/Enhancement:_
    - `license = "MIT"` (or confirm from `LICENSE` file).
    - `classifiers` (e.g., `Programming Language :: Python :: 3`, `License :: OSI Approved :: MIT License`, `Operating System :: OS Independent`, `Topic :: Office/Business :: Financial :: Investment`, `Intended Audience :: Developers`, `Development Status :: 3 - Alpha`). [See PyPI classifiers list](https://pypi.org/classifiers/).
    - `keywords` (e.g., `trading`, `AI`, `LLM`, `langchain`, `finance`, `investment`, `agent`).
    - `project_urls` (e.g., `Homepage = "https://github.com/shaneholloman/plutex"`, `Repository = "https://github.com/shaneholloman/plutex"`, `Issues = "https://github.com/shaneholloman/plutex/issues"`).
- **Packaging:**

  - _Build System:_ `hatchling` is suitable.
  - _License File:_ Ensure `LICENSE` is included in the distribution (check `hatchling` config or add explicitly if needed).
  - _Entry Points:_ Add console script entry points for easier execution:

    ```toml
    [project.scripts]
    plutex = "src.main:main" # Assuming main function exists in src/main.py
    plutex-backtest = "src.backtester:main" # Assuming main function exists
    ```

- **Testing Strategy:**
  - **Local Test Suite:** Expand the existing `pytest` setup. Create comprehensive unit and integration tests covering core logic, agent interactions, data handling, and utility functions. Aim for high code coverage (e.g., using `pytest-cov`).
  - **Continuous Integration (CI):** Implement GitHub Actions workflow (`.github/workflows/ci.yml`):
    - Trigger on push/pull_request to main branches.
    - Set up Python versions (3.10, 3.11, 3.12, 3.13).
    - Install dependencies using `uv sync`.
    - Run linters/formatters (Ruff).
    - Run tests using `pytest` across all target Python versions.
    - Optionally report code coverage.
- **Deployment Strategy:**
  - **Continuous Deployment (CD):** Implement GitHub Actions workflow (`.github/workflows/publish.yml`):
    - Trigger on creating Git tags (e.g., `v*.*.*`).
    - Build source distribution and wheel using `hatchling`.
    - Publish to PyPI using an API token stored securely as a GitHub secret.
- **Documentation:**
  - README provides basic setup/usage.
  - Needs dedicated, user-friendly documentation (e.g., using Sphinx or MkDocs) covering:
    - Installation from PyPI.
    - Detailed usage examples.
    - API reference for core modules/classes.
    - Explanation of agent configurations.
    - Secure API key setup.

## 6. Code Quality, Security, Tooling & Best Practices (2025 Standards)

- **Challenge:** README note ("REALLY poor state"). Current disparate tooling (`black`, `isort`, `flake8`). Non-standard line length (420). Reliance on external API keys necessitates security focus.
- **Areas for Review:**
  - Adherence to PEP 8 and general Python best practices.
  - Type hinting coverage and correctness.
  - Modularity and separation of concerns.
  - Error handling strategy (consistency, informativeness).
  - Logging implementation (structured logging preferred over `print`).
  - Identification and removal of dead/unused code.
  - **API Key Handling:** How keys are loaded from `.env` and passed within the application.
- **Recommendations:**
  - **Security Review:**
    - Verify API keys are loaded securely via `python-dotenv` and not exposed elsewhere (e.g., logs, exceptions, source code).
    - Ensure `.env` is correctly listed in `.gitignore` (it appears to be based on standard practice, but verify).
    - Document the requirement for users to create and secure their `.env` file.
  - **Consolidate Tooling with Ruff:**
    - Add `ruff` to `[dependency-groups.dev]`.
    - Remove `black`, `isort`, `flake8`.
    - Configure Ruff in `pyproject.toml` or `ruff.toml`:
      - Set a standard `line-length` (e.g., 88 or 120).
      - Select appropriate rules (start with defaults, equivalents to flake8, isort, pyupgrade, etc.).
      - Enable formatting (`ruff format`) and linting (`ruff check --fix`).
    - Update CI workflow to use Ruff commands.
  - **Code Refactoring:**
    - Perform a systematic code review focusing on readability, maintainability, and simplicity.
    - Apply Ruff auto-fixes and address remaining linting issues.
    - Refactor large functions/classes. Improve modularity.
    - Implement comprehensive type hints using modern syntax (Python 3.10+).
    - Replace `print` statements used for logging/debugging with the `logging` module. Configure basic logging.
    - Standardize exception handling.

## 7. Summary of Recommendations & Next Steps

This modernization effort involves several interconnected tasks. A suggested prioritization:

1. **Security Review:** Ensure API keys are handled safely. (High Priority)
2. **Test Suite Development:** Establish a solid baseline of tests. (High Priority)
3. **CI Setup:** Automate testing across Python versions. (High Priority)
4. **Ruff Migration:** Consolidate tooling and apply initial auto-fixes.
5. **Python Version Compatibility:** Test and adjust code/config for 3.10-3.13.
6. **PyPI Metadata & Packaging:** Complete `pyproject.toml` and entry points.
7. **Incremental Dependency Updates:** Carefully update libraries, starting with less complex ones, testing thoroughly. Tackle Langchain last.
8. **Code Refactoring:** Address quality issues identified by Ruff and manual review, improve typing, logging, error handling.
9. **CD Setup:** Automate PyPI publishing.
10. **Documentation Build-out:** Create comprehensive user and API documentation.

**Next Step:** It is recommended to switch to **Code mode** to begin implementing these changes, starting with the highest priority items like the security review, test suite, and CI setup.
