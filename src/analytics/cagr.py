"""
Sprint 2 - CAGR Engine
"""

from typing import Optional


def calculate_cagr(start_value: float,
                   end_value: float,
                   years: int) -> Optional[float]:
    """
    Generic CAGR Formula
    """

    if years <= 0:
        return None

    if start_value <= 0:
        return None

    if end_value <= 0:
        return None

    return ((end_value / start_value) ** (1 / years) - 1) * 100


def revenue_cagr(start_revenue: float,
                 end_revenue: float,
                 years: int):
    return calculate_cagr(start_revenue,
                          end_revenue,
                          years)


def pat_cagr(start_pat: float,
             end_pat: float,
             years: int):
    return calculate_cagr(start_pat,
                          end_pat,
                          years)


def eps_cagr(start_eps: float,
             end_eps: float,
             years: int):
    return calculate_cagr(start_eps,
                          end_eps,
                          years)