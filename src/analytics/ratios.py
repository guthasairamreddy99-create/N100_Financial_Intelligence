"""
Financial Ratio Engine
Sprint 2 - Day 8
"""

from typing import Optional


def net_profit_margin(net_profit: float, sales: float) -> Optional[float]:
    """Net Profit Margin (%)"""
    if sales == 0:
        return None
    return (net_profit / sales) * 100


def operating_profit_margin(operating_profit: float, sales: float) -> Optional[float]:
    """Operating Profit Margin (%)"""
    if sales == 0:
        return None
    return (operating_profit / sales) * 100


def return_on_equity(net_profit: float,
                     equity: float,
                     reserves: float) -> Optional[float]:
    """ROE (%)"""

    capital = equity + reserves

    if capital <= 0:
        return None

    return (net_profit / capital) * 100


def return_on_capital_employed(ebit: float,
                               equity: float,
                               reserves: float,
                               borrowings: float) -> Optional[float]:
    """ROCE (%)"""

    capital = equity + reserves + borrowings

    if capital <= 0:
        return None

    return (ebit / capital) * 100


def return_on_assets(net_profit: float,
                     total_assets: float) -> Optional[float]:
    """ROA (%)"""

    if total_assets == 0:
        return None

    return (net_profit / total_assets) * 100

def debt_to_equity(borrowings: float,
                   equity: float,
                   reserves: float):
    """
    Debt to Equity Ratio
    """
    capital = equity + reserves

    if borrowings == 0:
        return 0

    if capital <= 0:
        return None

    return borrowings / capital


def interest_coverage(operating_profit: float,
                      interest: float):
    """
    Interest Coverage Ratio
    """
    if interest == 0:
        return None

    return operating_profit / interest


def asset_turnover(sales: float,
                   total_assets: float):
    """
    Asset Turnover Ratio
    """
    if total_assets == 0:
        return None

    return sales / total_assets


def net_debt(borrowings: float,
             investments: float):
    """
    Net Debt
    """
    return borrowings - investments


def working_capital(current_assets: float,
                    current_liabilities: float):
    """
    Working Capital
    """
    return current_assets - current_liabilities