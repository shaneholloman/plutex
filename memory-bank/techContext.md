# Technical Context: plutex AI Trading System

## 1. Core Technologies

- **Programming Language:** Python
    - `plutex`: Requires Python >= 3.11 (`~=3.11` specified in `pyproject.toml`).
    - `../ai-hedge-fund`: Requires Python >= 3.9 (`^3.9` specified in `pyproject.toml`, Dockerfile uses `python:3.13-slim`).
- **AI/LLM Framework:** Langchain & LangGraph
    - Both projects utilize Langchain for interacting with LLMs and LangGraph for orchestrating agent workflows. Specific versions might differ slightly but are close (e.g., Langchain 0.3.0, LangGraph 0.2.56 in both).
- **LLM Providers:**
    - Both support: Anthropic, DeepSeek, Groq, Google (Gemini), OpenAI. API keys are managed via `.env`.
    - `../ai-hedge-fund`: Explicitly supports Ollama for local LLMs, integrated via Docker Compose. `plutex` does not explicitly mention Ollama support in the provided files.
- **Financial Data Provider:** Financial Datasets API (`financialdatasets.ai`). Requires an API key via `.env` for tickers beyond a free set (AAPL, GOOGL, MSFT, NVDA, TSLA).
- **Data Handling:** Pandas, NumPy. Used for processing and manipulating financial data.
- **CLI Interaction:**
    - `plutex`: Uses `questionary` for interactive prompts, `rich` and `tabulate` for formatted console output, `colorama` likely for colored output.
    - `../ai-hedge-fund`: Also uses `questionary`, `rich`, `tabulate`, `colorama`.
- **Visualization:** Matplotlib (likely used for backtester results).

## 2. Development Environment & Tooling

- **Dependency Management:**
    - `plutex`: `uv` (syncing based on `uv.lock` and `pyproject.toml`). Build backend: `hatchling`.
    - `../ai-hedge-fund`: `poetry` (installing based on `poetry.lock` and `pyproject.toml`). Build backend: `poetry.core.masonry.api`.
- **Environment Variables:** `.env` file (using `python-dotenv` library). `.env.example` provided as a template.
- **Containerization (`../ai-hedge-fund` only):** Docker (`Dockerfile`, `docker-compose.yml`) for creating reproducible environments and integrating services like Ollama. Includes helper scripts (`run.sh`, `run.bat`).
- **Version Control:** Git. Both projects are Git repositories.
- **Linting/Formatting (Assumed for `plutex` based on goals):** Likely intended to use tools like Ruff, Black, MyPy (dev dependencies listed in `plutex` `pyproject.toml`). `../ai-hedge-fund` lists Black, isort, flake8 as dev dependencies.

## 3. Key Dependencies & Versions (Comparison based on provided files)

| Library             | `plutex` Version Specifier | `../ai-hedge-fund` Version Specifier | Notes                                      |
| :------------------ | :------------------------- | :-------------------------------- | :----------------------------------------- |
| python              | `~=3.11`                   | `^3.9`                            | plutex requires a newer Python version.    |
| langchain           | `==0.3.0`                  | `0.3.0`                           | Same version.                              |
| langgraph           | `==0.2.56`                 | `0.2.56`                          | Same version.                              |
| langchain-anthropic | `==0.3.5`                  | `0.3.5`                           | Same version.                              |
| langchain-groq      | `==0.2.3`                  | `0.2.3`                           | Same version.                              |
| langchain-openai    | `>=0.3.5,<0.4`             | `^0.3.5`                          | Effectively similar ranges.                |
| langchain-deepseek  | `>=0.1.2,<0.2`             | `^0.1.2`                          | Effectively similar ranges.                |
| langchain-google    | `>=2.0.11,<3`              | `^2.0.11`                         | Effectively similar ranges.                |
| langchain-ollama    | -                          | `^0.2.0`                          | Only in `../ai-hedge-fund`.                   |
| pandas              | `>=2.1.0,<3`               | `^2.1.0`                          | Effectively similar ranges.                |
| numpy               | `>=1.24.0,<2`              | `^1.24.0`                         | Effectively similar ranges.                |
| python-dotenv       | Implicit (present)         | `1.0.0`                           | plutex likely uses `python-dotenv`.        |
| matplotlib          | `>=3.9.2,<4`               | `^3.9.2`                          | Effectively similar ranges.                |
| tabulate            | `>=0.9.0,<0.10`            | `^0.9.0`                          | Effectively similar ranges.                |
| colorama            | `>=0.4.6,<0.5`             | `^0.4.6`                          | Effectively similar ranges.                |
| questionary         | `>=2.1.0,<3`               | `^2.1.0`                          | Effectively similar ranges.                |
| rich                | `>=13.9.4,<14`             | `^13.9.4`                         | Effectively similar ranges.                |

*Note: Version specifiers like `^` (caret) and `>=,<` define compatible ranges. While slightly different, many core dependencies are pinned to similar functional versions.*

## 4. Technical Constraints & Considerations

- **API Keys:** Requires users to obtain and configure multiple API keys for LLMs and financial data.
- **LLM Costs:** Usage of cloud-based LLMs incurs costs. Ollama support in `../ai-hedge-fund` offers a free alternative if run locally.
- **Data Availability:** Financial data access might be limited by the API provider's free tier or subscription level.
- **Python Version:** The differing Python requirements might affect compatibility if code is directly copied without adjustments.
- **Dependency Management Tools:** Developers need to use the correct tool (`uv` for `plutex`, `poetry` for `../ai-hedge-fund`).
