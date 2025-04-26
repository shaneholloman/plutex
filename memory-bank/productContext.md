# Product Context: plutex AI Trading System

## 1. Problem Space

The original `../ai-hedge-fund` project demonstrated the potential of using multiple AI agents, each embodying different investment philosophies, to simulate trading decisions. However, it suffered from potential issues related to code quality, maintainability, and adherence to modern development standards, hindering further development and reliability. The `plutex` project aims to address these shortcomings.

## 2. Product Vision

`plutex` aims to be a robust, maintainable, and high-quality implementation of the multi-agent AI trading simulation concept. It serves as an educational and research platform for exploring AI-driven financial analysis and decision-making, built with best practices in software engineering. The goal is not live trading, but a sophisticated simulation environment.

## 3. Core Functionality (Derived from `../ai-hedge-fund` and `plutex` READMEs)

- **Multi-Agent Analysis:** Employs various AI agents (e.g., mimicking Warren Buffett, Cathie Wood, technical analysts, sentiment analysts) to analyze financial instruments (stocks). `../ai-hedge-fund` lists more specific investor agents than `plutex` initially.
- **Signal Generation:** Each agent generates trading signals (BUY, SELL, HOLD, SHORT) based on its specific analysis and investment style, along with a confidence score and reasoning.
- **Risk Management:** A dedicated agent assesses risk based on the signals and potentially other factors, providing risk-related guidance.
- **Portfolio Management:** A final agent synthesizes the inputs from analysts and the risk manager to make a final trading decision (simulated action) for each ticker, considering factors like portfolio cash and position limits.
- **LLM Integration:** Leverages Large Language Models (LLMs) via various APIs (OpenAI, Anthropic, Groq, Google, DeepSeek) to power the reasoning and analysis capabilities of the agents. `../ai-hedge-fund` also mentions Ollama support for local LLMs.
- **Financial Data Integration:** Uses external APIs (like Financial Datasets API) to fetch necessary financial data for analysis. Specific tickers (AAPL, GOOGL, MSFT, NVDA, TSLA) might have free data access.
- **Configuration:** Allows users to select which analysts to use, the LLM model, and target tickers via command-line arguments or interactive prompts.
- **Backtesting:** Includes a separate script (`backtester.py`) to simulate the strategy over historical data.
- **Reasoning Visibility:** Option to display the reasoning behind each agent's decision (`--show-reasoning`).
- **Date Range Specification:** Ability to run the simulation or backtest for specific start and end dates.

## 4. User Experience Goals

- **Clarity:** Provide clear output summarizing agent analysis and final trading decisions.
- **Flexibility:** Allow users to easily configure the simulation parameters (tickers, agents, LLMs, dates).
- **Insight:** Offer visibility into the agents' reasoning process when requested.
- **Reproducibility:** Ensure consistent results for given inputs and configurations (important for backtesting).
- **Developer Experience:** Maintain high code quality and clear documentation (`plutex` specific goal).

## 5. Target Audience

- Researchers exploring AI in finance.
- Students learning about quantitative trading strategies and AI agents.
- Developers interested in building agent-based systems.
- Individuals seeking an educational tool for understanding different investment philosophies through AI simulation.
