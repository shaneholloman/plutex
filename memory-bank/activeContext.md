# Active Context: plutex Refactor & Enhancement - A/B Comparison Complete

## 1. Current Focus

The current focus is completing the initial A/B comparison between `plutex` and `../ai-hedge-fund` based on file structure and key source code analysis. The goal is to identify key differences and potential features from `../ai-hedge-fund` to integrate into `plutex`.

## 2. Recent Changes

- **Memory Bank Review:** Read all core Memory Bank files (`projectBrief.md`, `productContext.md`, `systemPatterns.md`, `techContext.md`, `activeContext.md`, `progress.md`).
- **Source Code Structure Analysis:** Listed files in `src/` for both projects.
- **Key File Comparison:** Read and compared the following files between `plutex` and `../ai-hedge-fund`:
    - `agents/michael_burry.py` (only in `../ai-hedge-fund`)
    - `utils/ollama.py` (only in `../ai-hedge-fund`)
    - `utils/docker.py` (only in `../ai-hedge-fund`)
    - `main.py`
    - `backtester.py`
    - `utils/analysts.py`
    - `llm/models.py`

## 3. Next Steps

1.  **Present Findings:** Report the results of the A/B comparison and the identified integration candidates (`Ollama support`, `Michael Burry agent`) to the user.
2.  **Plan Integration (User Approval):** Based on user feedback, plan the specific steps for integrating the selected features into `plutex`, ensuring adherence to its higher coding standards.
3.  **Git History Analysis (Targeted):** If needed for integration planning, perform targeted `git log` analysis on the specific files related to Ollama support or the Michael Burry agent in `../ai-hedge-fund`.
4.  **Implementation:** Begin the refactoring and integration work within `plutex`.

## 4. Active Decisions & Considerations

- **Key Differences Identified:**
    - **Ollama/Docker:** `../ai-hedge-fund` has comprehensive Ollama/Docker support; `plutex` does not.
    - **Michael Burry Agent:** Present in `../ai-hedge-fund`, absent in `plutex`.
    - **Backtester Value Calc:** Minor difference in short position accounting (`plutex` method seems preferable).
    - **Tooling/Python Version:** `plutex` uses `uv`/Python 3.11+; `../ai-hedge-fund` uses `poetry`/Python 3.9+.
- **Integration Candidates:** Ollama support and the Michael Burry agent are the primary candidates for porting to `plutex`.
- **Prioritize Source Analysis:** Focused on source code comparison before Git history, as requested.
