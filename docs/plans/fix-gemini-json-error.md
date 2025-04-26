# Plan: Fix Gemini JSON Parsing Error

## 1. Problem

The application incorrectly reports an error related to "Deepseek" when attempting to parse JSON responses from Gemini models (e.g., `gemini-2.0-flash`). This occurs because the code assumes Gemini models do not support native JSON mode and falls back to a manual parsing function (`extract_json_from_deepseek_response`) which has a hardcoded error message mentioning "Deepseek".

## 2. Root Cause Analysis

- **`src/llm/models.py`:** The `LLMModel.has_json_mode()` method explicitly returns `False` for models identified as Gemini (`is_gemini()` returns `True`).
- **`src/utils/llm.py`:** The `call_llm` function relies on `has_json_mode()`. When it returns `False` for Gemini, it sets `use_json_extraction = True`.
- **`src/utils/llm.py`:** When `use_json_extraction` is `True`, the code calls `extract_json_from_deepseek_response`.
- **`src/utils/llm.py`:** The `extract_json_from_deepseek_response` function contains a hardcoded error message: `"Error extracting JSON from Deepseek response: {e}"`. This message is displayed even when the error originates from processing a Gemini response.

## 3. Proposed Solution

Modify the code to correctly handle JSON responses from Gemini models, assuming they support native JSON mode (which is standard for modern Gemini models).

### Step 3.1: Update JSON Mode Check for Gemini

- **File:** `src/llm/models.py`
- **Action:** Modify the `has_json_mode` method within the `LLMModel` class.
- **Change:** Remove the `and not self.is_gemini()` condition. The method should likely only return `False` for models explicitly known *not* to support JSON mode (like older Deepseek models, if that's still the case).

    ```python
    # Before
    def has_json_mode(self) -> bool:
        """Check if the model supports JSON mode"""
        return not self.is_deepseek() and not self.is_gemini()

    # After (Assuming only Deepseek needs special handling)
    def has_json_mode(self) -> bool:
        """Check if the model supports JSON mode"""
        # Only return False for models known *not* to support JSON mode
        return not self.is_deepseek()
        # Or, if *all* models except Deepseek support it:
        # return self.provider != ModelProvider.DEEPSEEK
    ```

    *(Decision on the exact logic depends on whether other models besides Deepseek lack JSON mode)*

### Step 3.2: Refine Error Handling in `call_llm`

- **File:** `src/utils/llm.py`
- **Action:** Improve the error reporting within the `call_llm` function's retry loop and potentially within `extract_json_from_deepseek_response` if it's kept for Deepseek.
- **Change:**
    - Ensure that error messages logged or printed clearly state the *actual* model provider and name involved, not just "Deepseek".
    - Modify the `except Exception as e:` block in `call_llm` to include model details:

        ```python
        # Example modification
        except Exception as e:
            error_msg = f"Error in LLM call (provider: {model_provider}, model: {model_name}) attempt {attempt + 1}/{max_retries}: {e}"
            if agent_name:
                progress.update_status(
                    agent_name, None, f"Error - retry {attempt + 1}/{max_retries}"
                ) # Keep progress update concise

            if attempt == max_retries - 1:
                print(
                    f"Final error after {max_retries} attempts for {agent_name or 'unknown agent'} (provider: {model_provider}, model: {model_name}): {e}"
                )
                return create_default_response(pydantic_model, default_factory)
        ```

    - Modify the error message within `extract_json_from_deepseek_response` (if still needed for Deepseek) to be specific:

        ```python
        # Inside extract_json_from_deepseek_response
        except Exception as e:
            # Make error specific to this function's context
            print(f"Error during manual JSON extraction (expected Deepseek format): {e}")
        ```

## 4. Testing

- Run the original command: `python -m src.main --tickers NVDA`
- Select a Gemini model (e.g., `gemini-2.0-flash`).
- Verify that the "Error extracting JSON from Deepseek response" message no longer appears.
- Confirm that the application proceeds correctly, successfully parsing the JSON response from Gemini.
- Optionally, test with a Deepseek model to ensure the manual extraction (if kept) still works correctly for it.

## 5. Rollback Plan

- Use `git stash` to save the changes before testing.
- If testing fails, use `git stash pop` to revert the changes.
