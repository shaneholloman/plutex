# Project Brief: Plutus Refactor & Enhancement

## 1. Project Goal

Refactor the existing `../ai-hedge-fund` Python project into a new project named `plutus`. The primary goal is to significantly improve coding standards, maintainability, and potentially modernize the architecture while selectively incorporating valuable functionality updates from the original `../ai-hedge-fund` project.

## 2. Core Objectives

- **Establish High Coding Standards:** Implement and enforce strict coding standards (linting, formatting, type checking, testing) in the `plutus` project.
- **Refactor Core Logic:** Review and refactor the core agent logic, data handling, and decision-making processes from `../ai-hedge-fund` for clarity, efficiency, and robustness in `plutus`.
- **A/B Comparison:** Conduct a thorough comparison between `plutus` and `../ai-hedge-fund` to identify differences in features, dependencies, and implementation details.
- **Selective Feature Integration:** Identify and evaluate recent features or improvements in `../ai-hedge-fund` for potential integration into `plutus`, ensuring they align with the new standards.
- **Modernize Dependencies & Setup:** Utilize modern Python practices, potentially updating dependencies (e.g., using `uv` in `plutus` vs. `poetry` in `../ai-hedge-fund`) and improving the development environment setup.
- **Maintain Documentation:** Create and maintain comprehensive documentation for `plutus` within the `memory-bank/` directory structure.

## 3. Scope

- **In Scope:**
    - Analysis and refactoring of Python code within `src/`.
    - Comparison of project structure, dependencies, and configuration.
    - Git history analysis of both repositories.
    - Documentation of findings and progress in the Memory Bank.
    - Implementation of coding standards and tooling (e.g., linters, formatters).
- **Out of Scope (Initially):**
    - Actual financial trading or deployment to live markets.
    - Major architectural changes beyond refactoring unless explicitly planned.
    - UI/Frontend development (unless present in the original and deemed essential).

## 4. Key Repositories

- `plutus/`: The target repository for the refactored, high-standard project.
- `../ai-hedge-fund/`: The source repository, used for comparison and potential feature extraction.
- `ai-financial-agent/`: Another repository in the project root, currently out of scope for this specific task.

## 5. Success Criteria

- `plutus` project adheres to defined coding standards (documented in `.clinerules`).
- Core functionality from `../ai-hedge-fund` (as deemed valuable) is present and refactored in `plutus`.
- Clear documentation exists in the Memory Bank detailing the project state, decisions, and progress.
- The `plutus` project is runnable and demonstrates the intended agent-based trading simulation logic.
