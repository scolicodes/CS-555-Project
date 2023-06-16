import unittest
from GEDCOMReader import family, individual, US04, US05, US06, date_after_current_date, age_over_150, calculate_age, US08, \
    check_born_before_death, check_born_before_married


class TestUS01(unittest.TestCase):
    """
    Author: Ronnie Arvanites
    User Story: US01
    Sprint: Sprint 1
    """

    def setUp(self):
        self.family1 = family(id="F1", married="20 OCT 1988", husband_Id="I04", husband_name="James Kern", wife_Id="I05", wife_name="Sara Keller")  # Marriage date before current date
        self.family2 = family(id="F2", married="13 JUN 1977", husband_Id="I06", husband_name="Kevin Burns", wife_Id="I07", wife_name="Jackie Parker", divorced="20 APR 2001")  # Divorce date before current date
        self.individual1 = individual(id="I01", name="Helen Klien", birthday="11 JAN 1998", age=25, alive=True)  # Birthday date before current date
        self.individual2 = individual(id="I02", name="Mary Freeman", birthday="22 OCT 1944", age=79, alive=False, death="2 SEP 2010")  # Death date before current date
        self.individual3 = individual(id="I03", name="Fred Green", birthday="15 NOV 2023", age=0)  # Birthday date after current date

    def test_marriage_date_before_current_date(self):
        self.assertFalse(date_after_current_date(self.family1.married))

    def test_divorce_date_before_current_date(self):
        self.assertFalse(date_after_current_date(self.family2.divorced))
    
    def test_birthday_before_current_date(self):
        self.assertFalse(date_after_current_date(self.individual1.birthday))
    
    def test_death_before_current_date(self):
        self.assertFalse(date_after_current_date(self.individual2.death))
    
    def test_birthday_after_current_date(self):
        self.assertTrue(date_after_current_date(self.individual3.birthday))


class TestUS02(unittest.TestCase):
    """
    Author: Andrew Turcan
    User Story: US02
    Sprint: Sprint 1
    """

    def setUp(self):
        self.family1 = family("F1", "10 FEB 1990", husband_Id="H1", wife_Id="W1")  # husband born before
        self.family2 = family("F2", "20 JAN 2005", husband_Id="H2", wife_Id="W1")  # No birthday provided for Husband
        self.family3 = family("F3", "30 MAR 2010", husband_Id="H3", wife_Id="W2")  # No birthday for wife, husband born after
        self.family4 = family("F4", "NA", "NA", husband_Id="H1", wife_Id="W2")  # No marriage date
        self.family5 = family("F5", "10 SEP 2019", "NA", husband_Id="H3", wife_Id="W1")  # Husband born after, wife born before.
        self.by_id = {
            "H1": individual("H1", "Phil", birthday="30 APR 1989"),
            "H2": individual("H2", "Bob", birthday="NA"),
            "H3": individual("H3", "Jeff", birthday="30 MAY 2020"),
            "W1": individual("W1", "Sharon", birthday="20 MAR 1987"),
            "W2": individual("W2", "Karen", birthday="30 APR 1989")
        }

    def test_birth_before_marriage(self):
        self.assertTrue(check_born_before_married(self.family1, False, self.by_id))  # Marriage date is before divorce date
        self.assertTrue(check_born_before_married(self.family2, False, self.by_id))  # No divorce date provided
        self.assertFalse(check_born_before_married(self.family3, False, self.by_id))  # Marriage date is after divorce date
        self.assertTrue(check_born_before_married(self.family4, False, self.by_id))  # Marriage and divorce dates are the same
        self.assertFalse(check_born_before_married(self.family5, False, self.by_id))  # Marriage and divorce dates are the same


class TestUS03(unittest.TestCase):
    """
    Author: Andrew Turcan
    User Story: US03
    Sprint: Sprint 1
    """

    def setUp(self):
        self.indi1 = individual("I1", birthday="10 FEB 1990", death="15 MAR 2000")  # born before death
        self.indi2 = individual("I1", birthday="NA", death="15 MAR 2000")  # no birthday
        self.indi3 = individual("I1", birthday="10 FEB 2010", death="15 MAR 2000")  # born after death
        self.indi4 = individual("I1", birthday="10 FEB 1990", death="NA")  # still alive
        self.indi5 = individual("I1", birthday="NA", death="NA")  # no birthday no death

    def test_birth_before_marriage(self):
        self.assertTrue(check_born_before_death(self.indi1, False))  # born before death
        self.assertTrue(check_born_before_death(self.indi2, False))  # no birthday
        self.assertFalse(check_born_before_death(self.indi3, False))  # born after death
        self.assertTrue(check_born_before_death(self.indi4, False))  # still alive
        self.assertTrue(check_born_before_death(self.indi5, False))  # still alive



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

class TestUS06(unittest.TestCase):
    """
    Author: Zac Schuh
    User Story: US06
    Sprint: Sprint 1
    """

    def setUp(self):
        self.family1 = family("F1", "15 JUN 1995", "12 DEC 2007", "I3", "John Smith", "I4", "Jane Smith")  # Both alive and divorced
        self.family2 = family("F2", "1 JAN 1990", "10 OCT 1997", "I1", "Jack Smith", "I4", "Jane Smith")  # Husband deceased but divorced before death
        self.family3 = family("F3", "3 MAR 1991", "8 AUG 1994", "I3", "John Smith", "I2", "Jill Smith")  # Wife deceased but divorced before death
        self.family4 = family("F4", "12 MAY 1992", "24 SEP 2001", "I1", "Jack Smith", "I4", "Jane Smith")  # Husband deceased and divorced after death
        self.family5 = family("F5", "28 MAR 1990", "10 FEB 2003", "I3", "John Smith", "I2", "Jill Smith")  # Wife deceased and divorced after death
        self.individual1 = individual(id="I1", name="Jack Smith", gender="M", birthday="01 JAN 1960", death="5 JUL 1999")
        self.individual2 = individual(id="I2", name="Jill Smith", gender="F", birthday="01 JAN 1970", death="1 MAR 1999")
        self.individual3 = individual(id="I3", name="John Smith", gender="M", birthday="01 JAN 1970", death="NA")
        self.individual4 = individual(id="I4", name="Jane Smith", gender="F", birthday="01 JAN 1975", death="NA")
        self.individuals = [self.individual1, self.individual2, self.individual3, self.individual4]

    def test_divorce_before_death(self):
        self.assertTrue(US06(self.family1, [self.individual3, self.individual4], False))  # Both alive
        self.assertTrue(US06(self.family2, [self.individual1, self.individual4], False))  # Husband deceased but married before death
        self.assertTrue(US06(self.family3, [self.individual3, self.individual2], False))  # Wife deceased but married before death
        self.assertFalse(US06(self.family4, [self.individual1, self.individual4], False))  # Husband deceased and married after death
        self.assertFalse(US06(self.family5, [self.individual3, self.individual2], False))  # Wife deceased and married after death

class TestUS07(unittest.TestCase):
    """
    Author: Ronnie Arvanites
    User Story: US07
    Sprint: Sprint 1
    """

    def setUp(self):
        self.individual1 = individual(id="I01", name="Gary Burger", birthday="11 JUL 1720", alive=True) # Living and older than 150 years
        self.individual2 = individual(id="I02", name="Sara Gallegher", birthday="11 NOV 1740", alive=False, death="21 OCT 1895") # Not living but died over 150 years old
        self.individual3 = individual(id="I03", name="Jalen Bass", birthday="2 NOV 1998", alive=False, death="10 DEC 2011") # Not living but died under 150 years old
        self.individual4 = individual(id="I04", name="Isabel Mullen", birthday="2 NOV 1998", alive=True) # Living and 25 years old
        self.individual5 = individual(id="I05", name="Ashley Lawrence", birthday="22 MAY 1913", alive=True) # Living and 110 years old

    def test_living_and_older_than_150(self):
        self.individual1.age = calculate_age(self.individual1.birthday)
        self.assertTrue(age_over_150(self.individual1))

    def test_not_living_and_older_than_150(self):
        self.individual2.age = calculate_age(self.individual2.birthday, self.individual2.death)
        self.assertTrue(age_over_150(self.individual2))
    
    def test_not_living_and_under_150(self):
        self.individual3.age = calculate_age(self.individual3.birthday, self.individual3.death)
        self.assertFalse(age_over_150(self.individual3))
    
    def test_living_and_under_150(self):
        self.individual4.age = calculate_age(self.individual4.birthday)
        self.assertFalse(age_over_150(self.individual4))
    
    def test_living_and_under_150_but_older_than_100(self):
        self.individual5.age = calculate_age(self.individual5.birthday)
        self.assertFalse(age_over_150(self.individual5))

class TestUS08(unittest.TestCase):
    """
    Author: Zac Schuh
    User Story: US08
    Sprint: Sprint 1
    """

    def setUp(self):
        self.family1 = family("F1", "15 JUN 1995", "NA", "I1", "John Smith", "I2", "Jane Smith", ["I3"])  # Married and had a child after marriage
        self.family2 = family("F1", "15 JUN 1995", "NA", "I1", "John Smith", "I2", "Jane Smith")  # Gets married and never had a child
        self.family3 = family("F1", "15 JUN 1995", "NA", "I1", "John Smith", "I2", "Jane Smith", ["I4"])  # Had a child a year before marriage
        self.family4 = family("F1", "15 JUN 1995", "15 JUNE 1998", "I1", "John Smith", "I2", "Jane Smith", ["I3"])  # Get married, have a child, then divorce
        self.family5 = family("F1", "15 JUN 1995", "NA", "I1", "John Smith", "I2", "Jane Smith", ["I3", "I4"])  # Had a child, got married, then had another child
        self.individual1 = individual(id="I1", name="John Smith", gender="M", birthday="01 JAN 1960", death="5 JUL 2020")
        self.individual2 = individual(id="I2", name="Jane Smith", gender="F", birthday="01 JAN 1970", death="1 MAR 2020")
        self.individual3 = individual(id="I3", name="Jack Smith", gender="M", birthday="01 JAN 1996", death="NA")
        self.individual4 = individual(id="I4", name="Jill Smith", gender="F", birthday="01 JAN 1993", death="NA")
        self.individuals = [self.individual1, self.individual2, self.individual3, self.individual4]

    def test_marriage_before_birth(self):
        self.assertTrue(US08(self.family1, [self.individual1, self.individual2, self.individual3], False))
        self.assertTrue(US08(self.family2, [self.individual1, self.individual2], False))
        self.assertFalse(US08(self.family3, [self.individual1, self.individual2, self.individual4], False))
        self.assertTrue(US08(self.family4, [self.individual1, self.individual2, self.individual3], False))
        self.assertFalse(US08(self.family5, [self.individual1, self.individual2, self.individual3, self.individual4], False))

if __name__ == '__main__':
    unittest.main()
