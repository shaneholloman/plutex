# System Patterns: plutex AI Trading System

## 1. High-Level Architecture

Both `plutex` and `../ai-hedge-fund` appear to follow a multi-agent system (MAS) architecture. The core idea is to decompose the complex task of trading analysis and decision-making into specialized, independent agents.

```mermaid
graph LR
    subgraph Input
        CLI[CLI Input (Tickers, Dates, Config)]
    end

    subgraph DataFetching
        FD[Financial Data API Client]
    end

    subgraph AgentLayer
        direction TB
        A1[Analyst Agent 1]
        A2[Analyst Agent 2]
        An[...]
        VA[Valuation Agent]
        SA[Sentiment Agent]
        FA[Fundamentals Agent]
        TA[Technicals Agent]
    end

    subgraph DecisionPipeline
        RM[Risk Manager Agent]
        PM[Portfolio Manager Agent]
    end

    subgraph LLMIntegration
        LLM[LLM API Clients (OpenAI, Anthropic, etc.)]
    end

    subgraph Output
        Console[Console Output (Analysis, Decisions)]
        Backtest[Backtesting Results (if applicable)]
    end

    CLI --> DataFetching
    DataFetching -- Fetched Data --> AgentLayer
    AgentLayer -- Analysis/Signals --> DecisionPipeline
    AgentLayer -- Uses --> LLMIntegration
    DecisionPipeline -- Risk/Portfolio Signals --> PM
    PM -- Final Decision --> Output
    DecisionPipeline -- Uses --> LLMIntegration # Portfolio/Risk managers might also use LLMs

    %% Styling
    classDef agent fill:#ffe4b5,stroke:#333,stroke-width:1px;
    class A1,A2,An,VA,SA,FA,TA,RM,PM agent;
    classDef io fill:#d3d3d3,stroke:#333,stroke-width:1px;
    class CLI,Console,Backtest io;
    classDef external fill:#add8e6,stroke:#333,stroke-width:1px;
    class FD,LLM external;
```

## 2. Key Technical Decisions & Patterns

- **Agent-Based Design:** The system is fundamentally built around specialized agents. This promotes modularity and allows for different "expert opinions" to be incorporated.
- **LLM-Powered Reasoning:** Agents leverage Large Language Models for complex analysis, interpretation, and generating human-readable reasoning. This suggests a pattern of prompt engineering and interaction with external LLM APIs.
- **Pipeline/Workflow Processing:** The flow from data fetching -> agent analysis -> risk management -> portfolio management suggests a pipeline or workflow pattern. The `plutex` README explicitly shows a Mermaid diagram illustrating this flow. `../ai-hedge-fund` likely follows a similar pattern. LangGraph is listed as a dependency, which strongly suggests a graph-based workflow for managing agent interactions.
- **Command-Line Interface (CLI):** Both projects use a CLI (`main.py`, `backtester.py`) as the primary user interface for configuration and execution. Libraries like `questionary` (in `plutex`) suggest interactive CLI elements.
- **Dependency Management:**
    - `plutex`: Uses `uv` and `pyproject.toml` (with hatchling build backend).
    - `../ai-hedge-fund`: Uses `poetry` and `pyproject.toml`.
- **Environment Configuration:** Both use `.env` files for managing sensitive API keys.
- **Modularity (Project Structure):** Both projects organize code into `src/` with subdirectories for `agents/`, `tools/`, `llm/`, `data/`, etc., indicating an attempt at modular design.
- **Backtesting Framework:** A separate `backtester.py` script suggests a dedicated component for strategy evaluation over historical data.
- **Dockerization (`../ai-hedge-fund`):** `../ai-hedge-fund` includes Docker configuration (`Dockerfile`, `docker-compose.yml`, `run.sh`, `run.bat`) for containerized deployment and execution, including integration with Ollama for local LLMs. `plutex` does not show this currently.

## 3. Component Relationships

- **`main.py` / `backtester.py`:** Entry points orchestrating the overall process.
- **Agent Modules (`src/agents/`):** Contain the core logic for each specialized agent. They likely depend on `src/tools/`, `src/llm/`, and `src/data/`.
- **Tool Modules (`src/tools/`):** Provide reusable functionalities, potentially including API clients for financial data or other utilities used by agents.
- **LLM Modules (`src/llm/`):** Encapsulate interactions with different LLM providers (OpenAI, Anthropic, Groq, etc.).
- **Data Modules (`src/data/`):** Handle fetching, processing, and potentially storing financial data.
- **Graph Modules (`src/graph/`):** Likely related to LangGraph implementation, defining the execution flow and state management between agents.
- **Utility Modules (`src/utils/`):** General helper functions.

## 4. Potential Areas for Improvement (plutex Focus)

- **Standardization:** Ensure consistent patterns across all agents in `plutex`.
- **Error Handling:** Implement robust error handling throughout the pipeline.
- **Testing:** Introduce unit and integration tests for agents and core components.
- **Configuration Management:** Potentially improve how configurations (agents, models, parameters) are managed beyond CLI arguments.
- **State Management:** Refine how state is passed between agents in the LangGraph workflow.
