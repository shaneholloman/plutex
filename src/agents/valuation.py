from langchain_core.messages import HumanMessage
from graph.state import AgentState, show_agent_reasoning
from utils.progress import progress
import json

from tools.api import get_financial_metrics, get_market_cap, search_line_items


##### Valuation Agent #####
def valuation_agent(state: AgentState):
    """Performs detailed valuation analysis using multiple methodologies for multiple tickers."""
    data = state["data"]
    end_date = data["end_date"]
    tickers = data["tickers"]

    # Initialize valuation analysis for each ticker
    valuation_analysis = {}

    for ticker in tickers:
        progress.update_status("valuation_agent", ticker, "Fetching financial data")

        # Fetch the financial metrics
        financial_metrics = get_financial_metrics(
            ticker=ticker,
            end_date=end_date,
            period="ttm",
        )

        # Add safety check for financial metrics
        if not financial_metrics:
            progress.update_status(
                "valuation_agent", ticker, "Failed: No financial metrics found"
            )
            continue

        metrics = financial_metrics[0]

        progress.update_status("valuation_agent", ticker, "Gathering line items")
        # Fetch the specific line_items that we need for valuation purposes
        financial_line_items = search_line_items(
            ticker=ticker,
            line_items=[
                "free_cash_flow",
                "net_income",
                "depreciation_and_amortization",
                "capital_expenditure",
                "working_capital",
            ],
            end_date=end_date,
            period="ttm",
            limit=2,
        )

        # Add safety check for financial line items
        if len(financial_line_items) < 2:
            progress.update_status(
                "valuation_agent", ticker, "Failed: Insufficient financial line items"
            )
            continue

        # Pull the current and previous financial line items
        current_financial_line_item = financial_line_items[0]
        previous_financial_line_item = financial_line_items[1]

        progress.update_status("valuation_agent", ticker, "Calculating owner earnings")
        # Safely access dynamic attributes using getattr with default 0.0
        current_wc = getattr(current_financial_line_item, "working_capital", 0.0)
        previous_wc = getattr(previous_financial_line_item, "working_capital", 0.0)
        current_ni = getattr(current_financial_line_item, "net_income", 0.0)
        current_da = getattr(
            current_financial_line_item, "depreciation_and_amortization", 0.0
        )
        current_ce = getattr(current_financial_line_item, "capital_expenditure", 0.0)
        current_fcf = getattr(current_financial_line_item, "free_cash_flow", 0.0)

        # Calculate working capital change, handle potential None from getattr
        working_capital_change = (current_wc or 0.0) - (previous_wc or 0.0)

        # Provide default growth rate if None
        growth_rate = (
            metrics.earnings_growth if metrics.earnings_growth is not None else 0.0
        )

        # Owner Earnings Valuation (Buffett Method)
        owner_earnings_value = calculate_owner_earnings_value(
            net_income=(current_ni or 0.0),
            depreciation=(current_da or 0.0),
            capex=(current_ce or 0.0),
            working_capital_change=working_capital_change,
            growth_rate=growth_rate,
            required_return=0.15,
            margin_of_safety=0.25,
        )

        progress.update_status("valuation_agent", ticker, "Calculating DCF value")
        # DCF Valuation
        dcf_value = calculate_intrinsic_value(
            free_cash_flow=(current_fcf or 0.0),
            growth_rate=growth_rate,
            discount_rate=0.10,
            terminal_growth_rate=0.03,
            num_years=5,
        )

        progress.update_status("valuation_agent", ticker, "Comparing to market value")
        # Get the market cap
        market_cap = get_market_cap(ticker=ticker, end_date=end_date)

        # Check if market_cap is valid before calculating gaps
        if market_cap is None or market_cap <= 0:
            progress.update_status(
                "valuation_agent", ticker, "Failed: Invalid market cap for valuation"
            )
            valuation_gap = 0.0
            dcf_gap = 0.0
            owner_earnings_gap = 0.0
            dcf_details = (
                f"Intrinsic Value: ${dcf_value:,.2f}, Market Cap: N/A, Gap: N/A"
            )
            owner_earnings_details = f"Owner Earnings Value: ${owner_earnings_value:,.2f}, Market Cap: N/A, Gap: N/A"
        else:
            # Calculate combined valuation gap (average of both methods)
            dcf_gap = (dcf_value - market_cap) / market_cap
            owner_earnings_gap = (owner_earnings_value - market_cap) / market_cap
            valuation_gap = (dcf_gap + owner_earnings_gap) / 2
            dcf_details = f"Intrinsic Value: ${dcf_value:,.2f}, Market Cap: ${market_cap:,.2f}, Gap: {dcf_gap:.1%}"
            owner_earnings_details = f"Owner Earnings Value: ${owner_earnings_value:,.2f}, Market Cap: ${market_cap:,.2f}, Gap: {owner_earnings_gap:.1%}"

        if valuation_gap > 0.15:  # More than 15% undervalued
            signal = "bullish"
        elif valuation_gap < -0.15:  # More than 15% overvalued
            signal = "bearish"
        else:
            signal = "neutral"

        # Create the reasoning
        reasoning = {}
        reasoning["dcf_analysis"] = {
            "signal": (
                "bullish"
                if dcf_gap > 0.15
                else "bearish"
                if dcf_gap < -0.15
                else "neutral"
            ),
            "details": dcf_details,
        }

        reasoning["owner_earnings_analysis"] = {
            "signal": (
                "bullish"
                if owner_earnings_gap > 0.15
                else "bearish"
                if owner_earnings_gap < -0.15
                else "neutral"
            ),
            "details": owner_earnings_details,
        }

        confidence = (
            round(abs(valuation_gap), 2) * 100
            if market_cap is not None and market_cap > 0
            else 0.0
        )
        valuation_analysis[ticker] = {
            "signal": signal,
            "confidence": confidence,
            "reasoning": reasoning,
        }

        progress.update_status("valuation_agent", ticker, "Done")

    message = HumanMessage(
        content=json.dumps(valuation_analysis),
        name="valuation_agent",
    )

    # Print the reasoning if the flag is set
    if state["metadata"]["show_reasoning"]:
        show_agent_reasoning(valuation_analysis, "Valuation Analysis Agent")

    # Add the signal to the analyst_signals list
    state["data"]["analyst_signals"]["valuation_agent"] = valuation_analysis

    return {
        "messages": [message],
        "data": data,
    }


def calculate_owner_earnings_value(
    net_income: float,
    depreciation: float,
    capex: float,
    working_capital_change: float,
    growth_rate: float = 0.05,
    required_return: float = 0.15,
    margin_of_safety: float = 0.25,
    num_years: int = 5,
) -> float:
    """
    Calculates the intrinsic value using Buffett's Owner Earnings method.

    Owner Earnings = Net Income
                    + Depreciation/Amortization
                    - Capital Expenditures
                    - Working Capital Changes

    Args:
        net_income: Annual net income
        depreciation: Annual depreciation and amortization
        capex: Annual capital expenditures
        working_capital_change: Annual change in working capital
        growth_rate: Expected growth rate
        required_return: Required rate of return (Buffett typically uses 15%)
        margin_of_safety: Margin of safety to apply to final value
        num_years: Number of years to project

    Returns:
        float: Intrinsic value with margin of safety
    """
    if not all(
        [
            isinstance(x, (int, float))
            for x in [net_income, depreciation, capex, working_capital_change]
        ]
    ):
        return 0

    # Calculate initial owner earnings
    owner_earnings = net_income + depreciation - capex - working_capital_change

    if owner_earnings <= 0:
        return 0

    # Project future owner earnings
    future_values = []
    for year in range(1, num_years + 1):
        future_value = owner_earnings * (1 + growth_rate) ** year
        discounted_value = future_value / (1 + required_return) ** year
        future_values.append(discounted_value)

    # Calculate terminal value (using perpetuity growth formula)
    terminal_growth = min(growth_rate, 0.03)  # Cap terminal growth at 3%
    terminal_value = (future_values[-1] * (1 + terminal_growth)) / (
        required_return - terminal_growth
    )
    terminal_value_discounted = terminal_value / (1 + required_return) ** num_years

    # Sum all values and apply margin of safety
    intrinsic_value = sum(future_values) + terminal_value_discounted
    value_with_safety_margin = intrinsic_value * (1 - margin_of_safety)

    return value_with_safety_margin


def calculate_intrinsic_value(
    free_cash_flow: float,
    growth_rate: float = 0.05,
    discount_rate: float = 0.10,
    terminal_growth_rate: float = 0.02,
    num_years: int = 5,
) -> float:
    """
    Computes the discounted cash flow (DCF) for a given company based on the current free cash flow.
    Use this function to calculate the intrinsic value of a stock.
    """
    # Estimate the future cash flows based on the growth rate
    cash_flows = [free_cash_flow * (1 + growth_rate) ** i for i in range(num_years)]

    # Calculate the present value of projected cash flows
    present_values = []
    for i in range(num_years):
        present_value = cash_flows[i] / (1 + discount_rate) ** (i + 1)
        present_values.append(present_value)

    # Calculate the terminal value
    terminal_value = (
        cash_flows[-1]
        * (1 + terminal_growth_rate)
        / (discount_rate - terminal_growth_rate)
    )
    terminal_present_value = terminal_value / (1 + discount_rate) ** num_years

    # Sum up the present values and terminal value
    dcf_value = sum(present_values) + terminal_present_value

    return dcf_value


def calculate_working_capital_change(
    current_working_capital: float,
    previous_working_capital: float,
) -> float:
    """
    Calculate the absolute change in working capital between two periods.
    A positive change means more capital is tied up in working capital (cash outflow).
    A negative change means less capital is tied up (cash inflow).

    Args:
        current_working_capital: Current period's working capital
        previous_working_capital: Previous period's working capital

    Returns:
        float: Change in working capital (current - previous)
    """
    return current_working_capital - previous_working_capital
