import unittest

from src.analytics.cagr import (
    calculate_cagr,
    revenue_cagr,
    pat_cagr,
    eps_cagr
)


class TestCAGR(unittest.TestCase):

    def test_calculate_cagr(self):
        result = calculate_cagr(100, 200, 5)
        self.assertAlmostEqual(result, 14.87, places=2)

    def test_zero_years(self):
        self.assertIsNone(calculate_cagr(100, 200, 0))

    def test_zero_start(self):
        self.assertIsNone(calculate_cagr(0, 200, 5))

    def test_negative_start(self):
        self.assertIsNone(calculate_cagr(-100, 200, 5))

    def test_negative_end(self):
        self.assertIsNone(calculate_cagr(100, -200, 5))

    def test_revenue_cagr(self):
        self.assertAlmostEqual(
            revenue_cagr(100, 200, 5),
            14.87,
            places=2
        )

    def test_pat_cagr(self):
        self.assertAlmostEqual(
            pat_cagr(50, 100, 5),
            14.87,
            places=2
        )

    def test_eps_cagr(self):
        self.assertAlmostEqual(
            eps_cagr(10, 20, 5),
            14.87,
            places=2
        )


if __name__ == "__main__":
    unittest.main()