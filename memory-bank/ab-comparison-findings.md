# A/B Comparison Findings: `plutex` vs. `../ai-hedge-fund`

This document summarizes the key differences identified during the initial comparison between the `plutex` (target, high-standard) and `../ai-hedge-fund` (source, potential features) projects, based on analysis of file structures, dependencies, and key source files.

## 1. Core Functionality & Architecture

- **Similarity:** Both projects implement a multi-agent AI trading simulation using Langchain/LangGraph for workflow orchestration. They share a similar `src/` structure (`agents/`, `llm/`, `tools/`, `utils/`, etc.) and rely on external APIs for LLMs (OpenAI, Anthropic, Groq, etc.) and financial data (Financial Datasets API). Both use CLI entry points (`main.py`, `backtester.py`) and `questionary` for user interaction.

## 2. Key Differences & Potential Integrations

### 2.1. Ollama / Local LLM Support

- **`../ai-hedge-fund`:** Has comprehensive, built-in support for using local LLMs via Ollama.
    - Includes `--ollama` flag in `main.py` and `backtester.py`.
    - Provides utility scripts (`utils/ollama.py`, `utils/docker.py`) for installation checks, server management, model downloading/management, and Docker integration.
    - Defines Ollama models and integrates `ChatOllama` in `llm/models.py`.
    - Includes Docker configuration (`Dockerfile`, `docker-compose.yml`) for easy setup with Ollama.
- **`plutex`:** Currently lacks any specific code or configuration for Ollama support.
- **Integration Potential:** High. Adding Ollama support would significantly increase `plutex`'s flexibility, allowing users to run simulations without relying solely on paid cloud LLM APIs. Requires porting relevant utilities, updating model handling, adding dependencies (`langchain-ollama`), and modifying CLI scripts.

### 2.2. Michael Burry Agent

- **`../ai-hedge-fund`:** Includes a dedicated agent (`agents/michael_burry.py`) implementing a deep-value, contrarian strategy. This agent is configured in `utils/analysts.py`.
- **`plutex`:** Does not currently include this specific agent.
- **Integration Potential:** High. Adding this agent is relatively straightforward (copying the file, updating `utils/analysts.py`) and would broaden the range of simulated investment philosophies in `plutex`.

### 2.3. Backtester Portfolio Value Calculation (Short Positions)

- **Difference:** The `calculate_portfolio_value` method in `backtester.py` differs slightly in how it accounts for open short positions:
    - `plutex`: Adds the unrealized P&L (`short_shares * (short_cost_basis - current_price)`).
    - `../ai-hedge-fund`: Subtracts the current market liability (`short_shares * current_price`).
- **Integration Potential:** Low. The `plutex` method seems more aligned with tracking portfolio equity directly. This difference should be noted, but the `plutex` implementation is likely preferable and doesn't require changes based on `../ai-hedge-fund`.

### 2.4. Development Environment & Tooling

- **Difference:**
    - **Dependency Management:** `plutex` uses `uv`; `../ai-hedge-fund` uses `poetry`.
    - **Python Version:** `plutex` requires `>=3.11`; `../ai-hedge-fund` targets `>=3.9`.
- **Integration Potential:** None. These differences reflect the deliberate modernization goal for `plutex`. `plutex` should retain `uv` and its Python 3.11+ requirement.

### 2.5. Minor Model List Differences

- **Difference:** The specific list of cloud LLM models defined in `llm/models.py` varies slightly between the projects.
- **Integration Potential:** Low/Informational. The lists can be synchronized or updated in `plutex` as needed, independent of major feature integration.

## 3. Summary Table

| Feature / Aspect        | `plutex` Status                     | `../ai-hedge-fund` Status                | Integration Candidate for `plutex`? | Priority | Notes                                      |
| :---------------------- | :---------------------------------- | :------------------------------------ | :---------------------------------- | :------- | :----------------------------------------- |
| Ollama / Local LLMs   | Absent                              | Present (incl. Docker)                | Yes                                 | High     | Increases flexibility, reduces API costs |
| Michael Burry Agent   | Absent                              | Present                               | Yes                                 | Medium   | Adds strategy diversity                  |
| Backtester Value Calc | Calculates Unrealized P&L (Short) | Subtracts Market Liability (Short)  | No                                  | N/A      | `plutex` method seems preferable         |
| Dependency Tool       | `uv`                                | `poetry`                              | No                                  | N/A      | `plutex` uses modern tool              |
| Python Version        | `>=3.11`                            | `>=3.9`                               | No                                  | N/A      | `plutex` uses modern version           |
| Docker Support        | Absent                              | Present (with Ollama)                 | Maybe (Lower Priority)              | Low      | Could be added later if needed           |

This comparison forms the basis for planning the refactoring and enhancement of the `plutex` project.
