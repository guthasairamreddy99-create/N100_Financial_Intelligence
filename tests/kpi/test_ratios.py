import unittest

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    debt_to_equity,
    interest_coverage,
    asset_turnover,
    net_debt,
    working_capital,
)


class TestFinancialRatios(unittest.TestCase):

    def test_net_profit_margin(self):
        self.assertEqual(net_profit_margin(20, 100), 20)

    def test_net_profit_margin_zero_sales(self):
        self.assertIsNone(net_profit_margin(20, 0))

    def test_operating_profit_margin(self):
        self.assertEqual(operating_profit_margin(30, 150), 20)

    def test_operating_profit_margin_zero_sales(self):
        self.assertIsNone(operating_profit_margin(30, 0))

    def test_return_on_equity(self):
        self.assertEqual(return_on_equity(50, 150, 50), 25)

    def test_return_on_equity_negative_capital(self):
        self.assertIsNone(return_on_equity(50, -100, 50))

    def test_return_on_capital_employed(self):
        self.assertEqual(
            return_on_capital_employed(40, 100, 50, 50),
            20,
        )

    def test_return_on_capital_employed_zero_capital(self):
        self.assertIsNone(
            return_on_capital_employed(40, -50, 0, 50)
        )

    def test_return_on_assets(self):
        self.assertEqual(return_on_assets(20, 200), 10)

    def test_return_on_assets_zero_assets(self):
        self.assertIsNone(return_on_assets(20, 0))

    def test_debt_to_equity(self):
        self.assertEqual(
        debt_to_equity(100, 150, 50),
        0.5
    )


def test_debt_to_equity_zero_borrowings(self):
    self.assertEqual(
        debt_to_equity(0, 150, 50),
        0
    )


def test_debt_to_equity_negative_equity(self):
    self.assertIsNone(
        debt_to_equity(100, -100, 50)
    )


def test_interest_coverage(self):
    self.assertEqual(
        interest_coverage(100, 20),
        5
    )


def test_interest_zero(self):
    self.assertIsNone(
        interest_coverage(100, 0)
    )


def test_asset_turnover(self):
    self.assertEqual(
        asset_turnover(1000, 500),
        2
    )


def test_asset_turnover_zero_assets(self):
    self.assertIsNone(
        asset_turnover(100, 0)
    )


def test_net_debt(self):
    self.assertEqual(
        net_debt(200, 50),
        150
    )


def test_working_capital(self):
    self.assertEqual(
        working_capital(500, 300),
        200
    )


if __name__ == "__main__":
    unittest.main()