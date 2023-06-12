import unittest
from GEDCOMReader import family, US04


class TestUS04(unittest.TestCase):
    """
    Author: Michael Scoli
    User Story: US04
    Sprint: Sprint 1
    """

    def setUp(self):
        self.family1 = family("F1", "10 FEB 1990", "15 MAR 2000")  # Marriage date is before divorce date
        self.family2 = family("F2", "20 JAN 2005", "NA")  # No divorce date provided
        self.family3 = family("F3", "30 MAR 2010", "15 MAR 2005")  # Marriage date is after divorce date
        self.family4 = family("F4", "15 APR 2000", "15 APR 2000")  # Married and divorced on the same day
        self.family5 = family("F5", "NA", "NA")  # No marriage or divorce dates provided

    def test_marriage_before_divorce(self):
        self.assertTrue(US04(self.family1))  # Marriage date is before divorce date
        self.assertTrue(US04(self.family2))  # No divorce date provided
        self.assertFalse(US04(self.family3))  # Marriage date is after divorce date
        self.assertTrue(US04(self.family4))  # Marriage and divorce dates are the same
        self.assertTrue(US04(self.family5))  # No marriage or divorce dates, should return True by default


if __name__ == '__main__':
    unittest.main()
