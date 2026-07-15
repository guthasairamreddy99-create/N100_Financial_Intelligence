import unittest

from src.analytics.cashflow import (
    free_cash_flow,
    cfo_quality,
    capex_intensity,
    fcf_conversion
)


class TestCashFlow(unittest.TestCase):

    def test_free_cash_flow(self):
        self.assertEqual(
            free_cash_flow(500, 100),
            400
        )

    def test_cfo_quality(self):
        self.assertEqual(
            cfo_quality(200, 100),
            2
        )

    def test_cfo_quality_zero(self):
        self.assertIsNone(
            cfo_quality(200, 0)
        )

    def test_capex_intensity(self):
        self.assertEqual(
            capex_intensity(100, 1000),
            10
        )

    def test_capex_zero(self):
        self.assertIsNone(
            capex_intensity(100, 0)
        )

    def test_fcf_conversion(self):
        self.assertEqual(
            fcf_conversion(400, 200),
            200
        )

    def test_fcf_conversion_zero(self):
        self.assertIsNone(
            fcf_conversion(400, 0)
        )


if __name__ == "__main__":
    unittest.main()