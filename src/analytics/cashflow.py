"""
Sprint 2
Cash Flow KPI Engine
"""

from typing import Optional


def free_cash_flow(cfo: float,
                   capex: float) -> float:
    """
    Free Cash Flow
    """
    return cfo - capex


def cfo_quality(cfo: float,
                net_profit: float) -> Optional[float]:
    """
    CFO Quality Ratio
    """
    if net_profit == 0:
        return None

    return cfo / net_profit


def capex_intensity(capex: float,
                    revenue: float) -> Optional[float]:
    """
    Capex Intensity
    """
    if revenue == 0:
        return None

    return (capex / revenue) * 100


def fcf_conversion(fcf: float,
                   net_profit: float) -> Optional[float]:
    """
    Free Cash Flow Conversion
    """
    if net_profit == 0:
        return None

    return (fcf / net_profit) * 100