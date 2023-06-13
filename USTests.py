import unittest
from GEDCOMReader import family, individual, US04, US05


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
        self.assertTrue(US04(self.family1, False))  # Marriage date is before divorce date
        self.assertTrue(US04(self.family2, False))  # No divorce date provided
        self.assertFalse(US04(self.family3, False))  # Marriage date is after divorce date
        self.assertTrue(US04(self.family4, False))  # Marriage and divorce dates are the same
        self.assertTrue(US04(self.family5, False))  # No marriage or divorce dates, should return True by default


class TestUS05(unittest.TestCase):
    """
    Author: Michael Scoli
    User Story: US05
    Sprint: Sprint 1
    """

    def setUp(self):
        self.family1 = family("F1", "10 FEB 1990", "NA", "I3", "Michael Scoli", "I4", "Emily Scoli")  # Both alive
        self.family2 = family("F2", "20 JAN 2005", "NA", "I1", "John Smith", "I4", "Emily Scoli")  # Husband deceased but married before death
        self.family3 = family("F3", "30 MAR 1995", "NA", "I3", "Michael Scoli", "I2", "Jane Smith")  # Wife deceased but married before death
        self.family4 = family("F4", "20 MAR 2000", "NA", "I1", "John Smith", "I4", "Emily Scoli")  # Husband deceased and married after death
        self.family5 = family("F5", "20 MAR 2000", "NA", "I3", "Michael Scoli", "I2", "Jane Smith")  # Wife deceased and married after death
        self.individual1 = individual(id="I1", name="John Smith", gender="M", birthday="01 JAN 1960", death="15 MAR 1999")
        self.individual2 = individual(id="I2", name="Jane Smith", gender="F", birthday="01 JAN 1970", death="15 MAR 1999")
        self.individual3 = individual(id="I3", name="Michael Scoli", gender="M", birthday="01 JAN 1975", death="NA")
        self.individual4 = individual(id="I4", name="Emily Scoli", gender="F", birthday="01 JAN 1980", death="NA")
        self.individuals = [self.individual1, self.individual2, self.individual3, self.individual4]

    def test_marriage_before_death(self):
        self.assertTrue(US05(self.family1, [self.individual3, self.individual4], False))  # Both alive
        self.assertFalse(US05(self.family2, [self.individual1, self.individual4], False))  # Husband deceased but married before death
        self.assertTrue(US05(self.family3, [self.individual3, self.individual2], False))  # Wife deceased but married before death
        self.assertFalse(US05(self.family4, [self.individual1, self.individual4], False))  # Husband deceased and married after death
        self.assertFalse(US05(self.family5, [self.individual3, self.individual2], False))  # Wife deceased and married after death



if __name__ == '__main__':
    unittest.main()
