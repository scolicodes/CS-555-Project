import unittest
from GEDCOMReader import *


class TestUS01(unittest.TestCase):
    """
    Author: Ronnie Arvanites
    User Story: US01
    Sprint: Sprint 1
    """

    def setUp(self):
        self.family1 = Family(id="F1", married="20 OCT 1988", husband_id="I04", husband_name="James Kern", wife_id="I05", wife_name="Sara Keller")  # Marriage date before current date
        self.family2 = Family(id="F2", married="13 JUN 1977", husband_id="I06", husband_name="Kevin Burns", wife_id="I07", wife_name="Jackie Parker", divorced="20 APR 2001")  # Divorce date before current date
        self.individual1 = Individual(id="I01", name="Helen Klien", birthday="11 JAN 1998", age=25, alive=True)  # Birthday date before current date
        self.individual2 = Individual(id="I02", name="Mary Freeman", birthday="22 OCT 1944", age=79, alive=False, death="2 SEP 2010")  # Death date before current date
        self.individual3 = Individual(id="I03", name="Fred Green", birthday="15 NOV 2023", age=0)  # Birthday date after current date

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
        self.family1 = Family("F1", "10 FEB 1990", husband_id="H1", wife_id="W1")  # husband born before
        self.family2 = Family("F2", "20 JAN 2005", husband_id="H2", wife_id="W1")  # No birthday provided for Husband
        self.family3 = Family("F3", "30 MAR 2010", husband_id="H3", wife_id="W2")  # No birthday for wife, husband born after
        self.family4 = Family("F4", "NA", "NA", husband_id="H1", wife_id="W2")  # No marriage date
        self.family5 = Family("F5", "10 SEP 2019", "NA", husband_id="H3", wife_id="W1")  # Husband born after, wife born before.
        self.by_id = {
            "H1": Individual("H1", "Phil", birthday="30 APR 1989"),
            "H2": Individual("H2", "Bob", birthday="NA"),
            "H3": Individual("H3", "Jeff", birthday="30 MAY 2020"),
            "W1": Individual("W1", "Sharon", birthday="20 MAR 1987"),
            "W2": Individual("W2", "Karen", birthday="30 APR 1989")
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
        self.indi1 = Individual("I1", birthday="10 FEB 1990", death="15 MAR 2000")  # born before death
        self.indi2 = Individual("I1", birthday="NA", death="15 MAR 2000")  # no birthday
        self.indi3 = Individual("I1", birthday="10 FEB 2010", death="15 MAR 2000")  # born after death
        self.indi4 = Individual("I1", birthday="10 FEB 1990", death="NA")  # still alive
        self.indi5 = Individual("I1", birthday="NA", death="NA")  # no birthday no death

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
        self.family1 = Family("F1", "10 FEB 1990", "15 MAR 2000")  # Marriage date is before divorce date
        self.family2 = Family("F2", "20 JAN 2005", "NA")  # No divorce date provided
        self.family3 = Family("F3", "30 MAR 2010", "15 MAR 2005")  # Marriage date is after divorce date
        self.family4 = Family("F4", "15 APR 2000", "15 APR 2000")  # Married and divorced on the same day
        self.family5 = Family("F5", "NA", "NA")  # No marriage or divorce dates provided

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
        self.family1 = Family("F1", "10 FEB 1990", "NA", "I3", "Michael Scoli", "I4", "Emily Scoli")  # Both alive
        self.family2 = Family("F2", "20 JAN 2005", "NA", "I1", "John Smith", "I4", "Emily Scoli")  # Husband deceased but married before death
        self.family3 = Family("F3", "30 MAR 1995", "NA", "I3", "Michael Scoli", "I2", "Jane Smith")  # Wife deceased but married before death
        self.family4 = Family("F4", "20 MAR 2000", "NA", "I1", "John Smith", "I4", "Emily Scoli")  # Husband deceased and married after death
        self.family5 = Family("F5", "20 MAR 2000", "NA", "I3", "Michael Scoli", "I2", "Jane Smith")  # Wife deceased and married after death
        self.individual1 = Individual(id="I1", name="John Smith", gender="M", birthday="01 JAN 1960", death="15 MAR 1999")
        self.individual2 = Individual(id="I2", name="Jane Smith", gender="F", birthday="01 JAN 1970", death="15 MAR 1999")
        self.individual3 = Individual(id="I3", name="Michael Scoli", gender="M", birthday="01 JAN 1975", death="NA")
        self.individual4 = Individual(id="I4", name="Emily Scoli", gender="F", birthday="01 JAN 1980", death="NA")
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
        self.family1 = Family("F1", "15 JUN 1995", "12 DEC 2007", "I3", "John Smith", "I4", "Jane Smith")  # Both alive and divorced
        self.family2 = Family("F2", "1 JAN 1990", "10 OCT 1997", "I1", "Jack Smith", "I4", "Jane Smith")  # Husband deceased but divorced before death
        self.family3 = Family("F3", "3 MAR 1991", "8 AUG 1994", "I3", "John Smith", "I2", "Jill Smith")  # Wife deceased but divorced before death
        self.family4 = Family("F4", "12 MAY 1992", "24 SEP 2001", "I1", "Jack Smith", "I4", "Jane Smith")  # Husband deceased and divorced after death
        self.family5 = Family("F5", "28 MAR 1990", "10 FEB 2003", "I3", "John Smith", "I2", "Jill Smith")  # Wife deceased and divorced after death
        self.individual1 = Individual(id="I1", name="Jack Smith", gender="M", birthday="01 JAN 1960", death="5 JUL 1999")
        self.individual2 = Individual(id="I2", name="Jill Smith", gender="F", birthday="01 JAN 1970", death="1 MAR 1999")
        self.individual3 = Individual(id="I3", name="John Smith", gender="M", birthday="01 JAN 1970", death="NA")
        self.individual4 = Individual(id="I4", name="Jane Smith", gender="F", birthday="01 JAN 1975", death="NA")
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
        self.individual1 = Individual(id="I01", name="Gary Burger", birthday="11 JUL 1720", alive=True) # Living and older than 150 years
        self.individual2 = Individual(id="I02", name="Sara Gallegher", birthday="11 NOV 1740", alive=False, death="21 OCT 1895") # Not living but died over 150 years old
        self.individual3 = Individual(id="I03", name="Jalen Bass", birthday="2 NOV 1998", alive=False, death="10 DEC 2011") # Not living but died under 150 years old
        self.individual4 = Individual(id="I04", name="Isabel Mullen", birthday="2 NOV 1998", alive=True) # Living and 25 years old
        self.individual5 = Individual(id="I05", name="Ashley Lawrence", birthday="22 MAY 1913", alive=True) # Living and 110 years old

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
        self.family1 = Family("F1", "15 JUN 1995", "NA", "I1", "John Smith", "I2", "Jane Smith", ["I3"])  # Married and had a child after marriage
        self.family2 = Family("F2", "15 JUN 1995", "NA", "I1", "John Smith", "I2", "Jane Smith")  # Gets married and never had a child
        self.family3 = Family("F3", "15 JUN 1995", "NA", "I1", "John Smith", "I2", "Jane Smith", ["I4"])  # Had a child a year before marriage
        self.family4 = Family("F4", "15 JUN 1995", "15 JUNE 1998", "I1", "John Smith", "I2", "Jane Smith", ["I3"])  # Get married, have a child, then divorce
        self.family5 = Family("F5", "15 JUN 1995", "NA", "I1", "John Smith", "I2", "Jane Smith", ["I3", "I4"])  # Had a child, got married, then had another child
        self.individual1 = Individual(id="I1", name="John Smith", gender="M", birthday="01 JAN 1960", death="5 JUL 2020")
        self.individual2 = Individual(id="I2", name="Jane Smith", gender="F", birthday="01 JAN 1970", death="1 MAR 2020")
        self.individual3 = Individual(id="I3", name="Jack Smith", gender="M", birthday="01 JAN 1996", death="NA")
        self.individual4 = Individual(id="I4", name="Jill Smith", gender="F", birthday="01 JAN 1993", death="NA")
        self.individuals = [self.individual1, self.individual2, self.individual3, self.individual4]

    def test_marriage_before_birth(self):
        self.assertTrue(US08(self.family1, [self.individual1, self.individual2, self.individual3], False))
        self.assertTrue(US08(self.family2, [self.individual1, self.individual2], False))
        self.assertFalse(US08(self.family3, [self.individual1, self.individual2, self.individual4], False))
        self.assertTrue(US08(self.family4, [self.individual1, self.individual2, self.individual3], False))
        self.assertFalse(US08(self.family5, [self.individual1, self.individual2, self.individual3, self.individual4], False))

class TestUS09(unittest.TestCase):
    """
    Author: Zac Schuh
    User Story: US09
    Sprint: Sprint 2
    """

    def setUp(self):
        self.family1 = Family("F1", "15 JUN 1995", "NA", "I1", "John Smith", "I2", "Jane Smith", ["I3"])  # Had a child years before dying
        self.family2 = Family("F2", "15 JUN 1995", "NA", "I1", "John Smith", "I2", "Jane Smith")  # Never had a child
        self.family3 = Family("F3", "15 JUN 1995", "NA", "I1", "John Smith", "I2", "Jane Smith", ["I4"])  # Had a child days after mother's death
        self.family4 = Family("F4", "15 JUN 1995", "NA", "I6", "Mark Smith", "I2", "Jane Smith", ["I5"])  # Had a child 3 months after father's death and before mother's death
        self.family5 = Family("F5", "15 JUN 1995", "NA", "I1", "John Smith", "I2", "Jane Smith", ["I7"])  # Had a child after both parents' death
        self.individual1 = Individual(id="I1", name="John Smith", gender="M", birthday="01 JAN 1960", death="5 JUL 2008")
        self.individual2 = Individual(id="I2", name="Jane Smith", gender="F", birthday="01 JAN 1970", death="1 MAR 2003")
        self.individual3 = Individual(id="I3", name="Jack Smith", gender="M", birthday="01 JAN 1996", death="NA")
        self.individual4 = Individual(id="I4", name="Jill Smith", gender="F", birthday="03 MAR 2003", death="NA")
        self.individual5 = Individual(id="I5", name="James Smith", gender="M", birthday="10 JUN 2001", death="NA")
        self.individual6 = Individual(id="I6", name="Mark Smith", gender="M", birthday="01 JAN 1970", death="10 MAR 2001")
        self.individual7 = Individual(id="I7", name="Elizabeth Smith", gender="F", birthday="5 DEC 2009", death="NA")
        self.individuals = [self.individual1, self.individual2, self.individual3, self.individual4]

    def test_death_before_birth(self):
        self.assertTrue(US09(self.family1, [self.individual1, self.individual2, self.individual3], False))
        self.assertTrue(US09(self.family2, [self.individual1, self.individual2], False))
        self.assertFalse(US09(self.family3, [self.individual1, self.individual2, self.individual4], False))
        self.assertTrue(US09(self.family4, [self.individual6, self.individual2, self.individual5], False))
        self.assertFalse(US09(self.family5, [self.individual1, self.individual2, self.individual7], False))

class TestUS10(unittest.TestCase):
    """
    Author: Zac Schuh
    User Story: US10
    Sprint: Sprint 2
    """

    def setUp(self):
        self.family1 = Family("F1", "NA", "NA", "I1", "John Smith", "I2", "Jane Smith")  # Individuals never married
        self.family2 = Family("F2", "15 JUN 1990", "NA", "I1", "John Smith", "I2", "Jane Smith")  # Married thirty years after mother's birth
        self.family3 = Family("F3", "1 JAN 1973", "NA", "I1", "John Smith", "I2", "Jane Smith")  # Married thirteen years after mother's birth
        self.family4 = Family("F4", "24 OCT 1970", "NA", "I1", "John Smith", "I2", "Jane Smith")  # Married before both parents were fourteen
        self.family5 = Family("F5", "1 JUN 1974", "NA", "I1", "John Smith", "I2", "Jane Smith")  # Married exactly fourteen years after mother's birth
        self.individual1 = Individual(id="I1", name="John Smith", gender="M", birthday="01 JAN 1958", death="NA")
        self.individual2 = Individual(id="I2", name="Jane Smith", gender="F", birthday="01 JUN 1960", death="NA")
        self.individuals = [self.individual1, self.individual2]

    def test_marriage_after_fourteen(self):
        self.assertTrue(US10(self.family1, [self.individual1, self.individual2], False))
        self.assertTrue(US10(self.family2, [self.individual1, self.individual2], False))
        self.assertFalse(US10(self.family3, [self.individual1, self.individual2], False))
        self.assertFalse(US10(self.family4, [self.individual1, self.individual2], False))
        self.assertTrue(US10(self.family5, [self.individual1, self.individual2], False))

class TestUS24(unittest.TestCase):
    """
    Author: Zac Schuh
    User Story: US24
    Sprint: Sprint 3
    """

    def setUp(self):
        self.family1 = Family("F1", "15 JUN 1995", "NA", "I1", "John Smith", "I2", "Jane Smith")  
        self.family2 = Family("F2", "15 JUN 1996", "NA", "I3", "Jack Smith", "I4", "Jill Smith")  
        self.family3 = Family("F3", "15 JUN 1995", "NA", "I5", "John Smith", "I6", "Jane Smith")  # Same as F1
        self.family4 = Family("F4", "15 JUN 1995", "NA", "I7", "John Smith", "I8", "Jill Smith")  
        self.family5 = Family("F5", "10 MAY 1999", "NA", "I9", "Jack Smith", "I10", "Jill Smith")
        self.individual1 = Individual(id="I1", name="John Smith", gender="M", birthday="01 JAN 1960", death="NA")
        self.individual2 = Individual(id="I2", name="Jane Smith", gender="F", birthday="01 JAN 1970", death="NA")
        self.individual3 = Individual(id="I3", name="Jack Smith", gender="M", birthday="01 JAN 1996", death="NA")
        self.individual4 = Individual(id="I4", name="Jill Smith", gender="F", birthday="03 MAR 1993", death="NA")
        self.individual5 = Individual(id="I5", name="John Smith", gender="M", birthday="10 JUN 1991", death="NA")
        self.individual6 = Individual(id="I6", name="Jane Smith", gender="M", birthday="10 JUN 1991", death="NA")
        self.individual7 = Individual(id="I7", name="John Smith", gender="F", birthday="5 DEC 1987", death="NA")
        self.individual8 = Individual(id="I8", name="Jill Smith", gender="F", birthday="5 DEC 1989", death="NA")
        self.individual9 = Individual(id="I9", name="Jack Smith", gender="M", birthday="01 JAN 1990", death="NA")
        self.individual10 = Individual(id="I10", name="Jill Smith", gender="F", birthday="5 DEC 1989", death="NA")

    def test_unique_families(self):
        self.assertTrue(US24([self.family1, self.family2], [self.individual1, self.individual2, self.individual3, self.individual4], False))
        self.assertFalse(US24([self.family1, self.family2, self.family3], [self.individual1, self.individual2, self.individual3, self.individual4, self.individual5, self.individual6], False))
        self.assertFalse(US24([self.family1, self.family3, self.family4], [self.individual1, self.individual2, self.individual3, self.individual4], False))
        self.assertTrue(US24([self.family2, self.family4], [self.individual3, self.individual4, self.individual7, self.individual8], False))
        self.assertTrue(US24([self.family2, self.family4, self.family5], [self.individual3, self.individual4, self.individual7, self.individual8, self.individual9, self.individual10], False))

class TestUS25(unittest.TestCase):
    """
    Author: Zac Schuh
    User Story: US25
    Sprint: Sprint 3
    """

    def setUp(self):
        self.family2 = Family("F1", "15 JUN 1995", "NA", "I1", "John Smith", "I2", "Jane Smith")  # Never had a child
        self.family1 = Family("F2", "15 JUN 1995", "NA", "I1", "John Smith", "I2", "Jane Smith", ["I3"])  # One child only
        self.family3 = Family("F3", "15 JUN 1995", "NA", "I1", "John Smith", "I2", "Jane Smith", ["I3", "I4"])  # Two different children
        self.family4 = Family("F4", "15 JUN 1995", "NA", "I1", "John Smith", "I2", "Jane Smith", ["I3", "I4", "I5", "I6"])  # Two children share a name and birthday
        self.family5 = Family("F5", "15 JUN 1995", "NA", "I1", "John Smith", "I2", "Jane Smith", ["I3", "I4", "I7", "I8"])  # Two children share a name but not a birthday
        self.individual1 = Individual(id="I1", name="John Smith", gender="M", birthday="01 JAN 1960", death="NA")
        self.individual2 = Individual(id="I2", name="Jane Smith", gender="F", birthday="01 JAN 1970", death="NA")
        self.individual3 = Individual(id="I3", name="Jack Smith", gender="M", birthday="01 JAN 1996", death="NA")
        self.individual4 = Individual(id="I4", name="Jill Smith", gender="F", birthday="03 MAR 2003", death="NA")
        self.individual5 = Individual(id="I5", name="James Smith", gender="M", birthday="10 JUN 2001", death="NA")
        self.individual6 = Individual(id="I6", name="James Smith", gender="M", birthday="10 JUN 2001", death="NA")
        self.individual7 = Individual(id="I7", name="Elizabeth Smith", gender="F", birthday="5 DEC 2007", death="NA")
        self.individual8 = Individual(id="I8", name="Elizabeth Smith", gender="F", birthday="5 DEC 2009", death="NA")

    def test_unique_children(self):
        self.assertTrue(US25(self.family1, [self.individual1, self.individual2], False))
        self.assertTrue(US25(self.family2, [self.individual1, self.individual2, self.individual3], False))
        self.assertTrue(US25(self.family3, [self.individual1, self.individual2, self.individual3, self.individual4], False))
        self.assertFalse(US25(self.family4, [self.individual1, self.individual2, self.individual3, self.individual4, self.individual5, self.individual6], False))
        self.assertTrue(US25(self.family5, [self.individual1, self.individual2, self.individual3, self.individual4, self.individual7, self.individual8], False))

class TestUS33(unittest.TestCase):
    """
    Author: Zac Schuh
    User Story: US33
    Sprint: Sprint 4
    """

    def setUp(self):
        self.family1 = Family("F1", "15 JUN 1995", "NA", "I1", "John Smith", "I2", "Jane Smith")  # Never had a child
        self.family2 = Family("F2", "15 JUN 1995", "NA", "I8", "John Evans", "I9", "Jane Evans", ["I3"])  # Child under 18, but one parent alive
        self.family3 = Family("F3", "15 JUN 1995", "NA", "I10", "John Lane", "I5", "Maggie Lane", ["I11", "I4"])  # One child under 18, one child over 18, parents dead
        self.family4 = Family("F4", "15 JUN 1995", "NA", "I6", "James Waters", "I13", "Jane Waters", ["I12"])  # One child but both parents alive
        self.family5 = Family("F5", "15 JUN 1995", "NA", "I14", "John Doe", "I15", "Maggie Doe", ["I16", "I17"])  # Two children orphaned
        self.indiv1 = Individual(id="I1", name="John Smith", gender="M", birthday="01 JAN 1960", death="01 JAN 2020")
        self.indiv2 = Individual(id="I2", name="Jane Smith", gender="F", birthday="01 JAN 1970", death="NA")
        self.indiv3 = Individual(id="I3", name="Jack Smith", gender="M", birthday="01 JAN 2006", death="NA")
        self.indiv4 = Individual(id="I4", name="Jill Smith", gender="F", birthday="03 MAR 2003", death="NA")
        self.indiv5 = Individual(id="I5", name="Maggie Lane", gender="F", birthday="10 JUN 1970", death="02 JAN 2020")
        self.indiv6 = Individual(id="I6", name="James Waters", gender="M", birthday="10 JUN 1971", death="NA")
        self.indiv7 = Individual(id="I7", name="Elizabeth Smith", gender="F", birthday="5 DEC 2007", death="NA")
        self.indiv8 = Individual(id="I8", name="John Evans", gender="M", birthday="01 JAN 1960", death="01 JAN 2020")
        self.indiv9 = Individual(id="I9", name="Jane Evans", gender="F", birthday="01 JAN 1970", death="NA")
        self.indiv10 = Individual(id="I10", name="John Lane", gender="M", birthday="01 JAN 1960", death="01 JAN 2020")
        self.indiv11 = Individual(id="I11", name="Jack Lane", gender="M", birthday="01 JAN 2006", death="NA")
        self.indiv12 = Individual(id="I12", name="Elizabeth Waters", gender="F", birthday="5 DEC 2007", death="NA")
        self.indiv13 = Individual(id="I13", name="Jane Waters", gender="F", birthday="01 JAN 1970", death="NA")
        self.indiv14 = Individual(id="I14", name="John Doe", gender="M", birthday="01 JAN 1960", death="01 JAN 2020")
        self.indiv15 = Individual(id="I15", name="Maggie Doe", gender="F", birthday="10 JUN 1970", death="02 JAN 2020")
        self.indiv16 = Individual(id="I16", name="Jack Doe", gender="M", birthday="01 JAN 2006", death="NA")
        self.indiv17 = Individual(id="I17", name="Elizabeth Doe", gender="F", birthday="5 DEC 2007", death="NA")

    def test_orphans(self):
        self.orphan_table = find_orphans(
            [self.family1, self.family2, self.family3, self.family4, self.family5],
            [self.indiv1, self.indiv2, self.indiv3, self.indiv4, self.indiv5, self.indiv6, self.indiv7, self.indiv8, self.indiv9, self.indiv10, self.indiv11, self.indiv12, self.indiv13, self.indiv14, self.indiv15, self.indiv16, self.indiv17])
        self.assertEqual(len(self.orphan_table.rows), 3)

class TestUS34(unittest.TestCase):
    """
    Author: Zac Schuh
    User Story: US34
    Sprint: Sprint 4
    """

    def setUp(self):
        self.family1 = Family("F1", "15 JUN 1995", "NA", "I1", "John Smith", "I2", "Jane Smith")  # Husband was 35 when married, wife was 25
        self.family2 = Family("F2", "15 JUN 1985", "NA", "I3", "Jack Smith", "I4", "Jill Smith")  # Husband was 39 when married, wife was 19
        self.family3 = Family("F3", "15 JUN 1995", "NA", "I6", "John Lane", "I5", "Maggie Lane")  # Husband was 24 when married, wife was 25
        self.family4 = Family("F4", "15 JUN 1995", "NA", "I8", "James Evans", "I7", "Juliet Evans")  # Husband was 25 when married, wife was 57
        self.family5 = Family("F5", "15 JUN 1990", "NA", "I10", "Max Doe", "I9", "Maggie Doe")  # Husband was 40 when married, wife was 20
        self.indiv1 = Individual(id="I1", name="John Smith", gender="M", birthday="01 JAN 1960", death="NA")
        self.indiv2 = Individual(id="I2", name="Jane Smith", gender="F", birthday="01 JAN 1970", death="NA")
        self.indiv3 = Individual(id="I3", name="Jack Smith", gender="M", birthday="01 JAN 1946", death="NA")
        self.indiv4 = Individual(id="I4", name="Jill Smith", gender="F", birthday="03 MAR 1966", death="NA")
        self.indiv5 = Individual(id="I5", name="Maggie Lane", gender="F", birthday="10 JUN 1970", death="NA")
        self.indiv6 = Individual(id="I6", name="John Lane", gender="M", birthday="10 JUN 1971", death="NA")
        self.indiv7 = Individual(id="I7", name="Juliet Evans", gender="F", birthday="5 DEC 1937", death="NA")
        self.indiv8 = Individual(id="I8", name="James Evans", gender="M", birthday="01 JAN 1970", death="NA")
        self.indiv9 = Individual(id="I9", name="Maggie Doe", gender="F", birthday="01 JAN 1970", death="NA")
        self.indiv10 = Individual(id="I10", name="Max Doe", gender="M", birthday="01 JAN 1950", death="NA")

    def test_couples(self):
        self.couples_table = find_age_differences(
            [self.family1, self.family2, self.family3, self.family4, self.family5],
            [self.indiv1, self.indiv2, self.indiv3, self.indiv4, self.indiv5, self.indiv6, self.indiv7, self.indiv8, self.indiv9, self.indiv10])
        self.assertEqual(len(self.couples_table.rows), 2)

class TestUS14(unittest.TestCase):
    """
    Author: Andrew Turcan
    User Story: US14
    Sprint 2
    """
    def test_check_no_quintuplets_and_beyond(self):
        by_id = {
            "I01": Individual(id="I01", name="James Kern", birthday="20 OCT 2001"),
            "I02": Individual(id="I02", name="Kevin Burns", birthday="20 OCT 2001"),
            "I03": Individual(id="I03", name="Gary Paul", birthday="20 OCT 2001"),
            "I04": Individual(id="I04", name="Jack Simons", birthday="20 OCT 2001"),
            "I05": Individual(id="I05", name="Jaden Hall", birthday="20 OCT 2002"),
            "I06": Individual(id="I06", name="Johnathan Rubio", birthday="20 OCT 2002"),
            "I07": Individual(id="I07", name="Ryan Rubio", birthday="20 OCT 2002"),
            "I08": Individual(id="I08", name="Joel Norman", birthday="20 OCT 2002"),
            "I09": Individual(id="I09", name="Harper Norman", birthday="20 OCT 2002"),
            "I10": Individual(id="I10", name="Lily Key", birthday="20 OCT 2002"),
            "I11": Individual(id="I11", name="Brooks Pollard", birthday="20 OCT 2002"),
            "I12": Individual(id="I12", name="Dominic Thompson", birthday="20 OCT 2002"),
            "I13": Individual(id="I13", name="Annabelle Roth", birthday="20 OCT 2002"),
            "I14": Individual(id="I14", name="Justin Simons", birthday="20 OCT 2002"),
            "I15": Individual(id="I15", name="Allan Hall", birthday="20 OCT 2002"),
            "I16": Individual(id="I16", name="Brandon Newman", birthday="20 OCT 2002"),
        }

        family = Family(id="F1", children=[f"'{child_id}'" for child_id in by_id.keys()])  # 16 children
        family2 = Family(id="F2", children=["'I01'", "'I02'"])  # fewer than 5 children
        family3 = Family(id="F3")
        family4 = Family(id="F4", children=["'I01'", "'I02'", "'I03'", "'I04'", "'I05'"])
        family5 = Family(id="F5", children=["'I08'", "'I10'", "'I16'", "'I09'", "'I15'", "'I11'"])

        self.assertFalse(check_no_quintuplets_and_beyond(family, by_id, False))
        self.assertTrue(check_no_quintuplets_and_beyond(family2, by_id, False))
        self.assertTrue(check_no_quintuplets_and_beyond(family3, by_id, False))
        self.assertTrue(check_no_quintuplets_and_beyond(family4, by_id, False))
        self.assertFalse(check_no_quintuplets_and_beyond(family5, by_id, False))


class TestUS15(unittest.TestCase):
    """
    Author: Andrew Turcan
    User Story: US15
    Sprint 2
    """
    def test_check_under15_siblings(self):

        family = Family(id="F1", children=[f"'I{child_id}'" for child_id in range(16)])
        family2 = Family(id="F2", children=["'I01'", "'I02'"])
        family3 = Family(id="F3")
        family4 = Family(id="F4", children=["'I06'", "'I02'", "'I03'", "'I04'", "'I05'"])
        family5 = Family(id="F5", children=["'I07'", "'I10'", "'I16'", "'I09'", "'I15'", "'I11'"])

        self.assertFalse(check_under15_siblings(family, False))
        self.assertTrue(check_under15_siblings(family2, False))
        self.assertTrue(check_under15_siblings(family3, False))
        self.assertTrue(check_under15_siblings(family4, False))
        self.assertTrue(check_under15_siblings(family5, False))



class TestUS16(unittest.TestCase):
    """
    Author: Ronnie Arvanites
    User Story: US16
    Sprint: Sprint 2
    """

    def setUp(self):
        self.family1 = Family(id="F1", married="20 OCT 1988", husband_id="I01", husband_name="James Kern", children=["'I06'", "'I07'"])  # Family with two boys with different last names
        self.family2 = Family(id="F2", married="13 JUN 1977", husband_id="I02", husband_name="Kevin Burns", children=["'I08'", "'I09'"])  # Family with one boy and one girl with different last names
        self.family3 = Family(id="F3", married="13 JUN 1977", husband_id="I03", husband_name="Gary Paul", children=["'I10'", "'I11'"])  # Family with two girls with different last names
        self.family4 = Family(id="F4", married="13 JUN 1977", husband_id="I04", husband_name="Jack Simons", children=["'I12'", "'I13'", "'I14'"])  # Family with three children (two boys and 1 girl) with the males with the same last names
        self.family5 = Family(id="F5", married="13 JUN 1977", husband_id="I05", husband_name="Jaden Hall", children=["'I15'", "'I16'"])  # Family with two boys one with a different last name
        self.by_id = {
            "I01": Individual(id="I01", name="James Kern", gender="M"),
            "I02": Individual(id="I02", name="Kevin Burns", gender="M"),
            "I03": Individual(id="I03", name="Gary Paul", gender="M"),
            "I04": Individual(id="I04", name="Jack Simons", gender="M"),
            "I05": Individual(id="I05", name="Jaden Hall", gender="M"),
            "I06": Individual(id="I06", name="Johnathan Rubio", gender="M"),
            "I07": Individual(id="I07", name="Ryan Rubio", gender="M"),
            "I08": Individual(id="I08", name="Joel Norman", gender="M"),
            "I09": Individual(id="I09", name="Harper Norman", gender="F"),
            "I10": Individual(id="I10", name="Lily Key", gender="F"),
            "I11": Individual(id="I11", name="Brooks Pollard", gender="F"),
            "I12": Individual(id="I12", name="Dominic Simons", gender="M"),
            "I13": Individual(id="I13", name="Annabelle Roth", gender="F"),
            "I14": Individual(id="I14", name="Justin Simons", gender="M"),
            "I15": Individual(id="I15", name="Allan Hall", gender="M"),
            "I16": Individual(id="I16", name="Brandon Newman", gender="M"),
        }

    def test_two_male_children_with_different_last_names(self):
        self.assertFalse(check_male_members_last_name(self.family1, self.by_id, print_errors=False))
    
    def test_one_male_child_and_one_female_child_with_different_last_names(self):
        self.assertFalse(check_male_members_last_name(self.family2, self.by_id, print_errors=False))

    def test_two_female_children_with_different_last_names(self):
        self.assertTrue(check_male_members_last_name(self.family3, self.by_id, print_errors=False))
    
    def test_two_male_and_one_female_children_with_males_same_last_names(self):
        self.assertTrue(check_male_members_last_name(self.family4, self.by_id, print_errors=False))
    
    def test_two_male_children_one_with_different_last_name(self):
        self.assertFalse(check_male_members_last_name(self.family5, self.by_id, print_errors=False))


class TestUS12(unittest.TestCase):
    """
    Author: Michael Scoli
    User Story: US12
    Sprint: Sprint 2
    """

    def setUp(self):
        self.family1 = Family("F1", "15 JUN 1995", "NA", "I1", "John Smith", "I2", "Jane Smith", children=["I3"])  # Parents are not too old
        self.family2 = Family("F2", "1 JAN 1970", "NA", "I4", "Jack Smith", "I5", "Janet Smith", children=["I6"])  # Father is too old
        self.family3 = Family("F3", "3 MAR 1980", "NA", "I7", "Jerry Smith", "I8", "Jill Smith", children=["I9"])  # Mother is too old
        self.family4 = Family("F4", "12 MAY 1990", "NA", "I10", "Joe Smith", "I11", "Jenny Smith", children=["I12"])  # Both parents are too old

        self.individuals = [
            Individual(id="I1", name="John Smith", gender="M", birthday="01 JAN 1960"),
            Individual(id="I2", name="Jane Smith", gender="F", birthday="01 JAN 1965"),
            Individual(id="I3", name="Junior Smith", gender="M", birthday="01 JAN 1990"),
            Individual(id="I4", name="Jack Smith", gender="M", birthday="01 JAN 1830"),
            Individual(id="I5", name="Janet Smith", gender="F", birthday="01 JAN 1935"),
            Individual(id="I6", name="Jackie Smith", gender="M", birthday="01 JAN 1990"),
            Individual(id="I7", name="Jerry Smith", gender="M", birthday="01 JAN 1950"),
            Individual(id="I8", name="Jill Smith", gender="F", birthday="01 JAN 1910"),
            Individual(id="I9", name="Jenny Smith", gender="M", birthday="01 JAN 1990"),
            Individual(id="I10", name="Joe Smith", gender="M", birthday="01 JAN 1900"),
            Individual(id="I11", name="Jane Smith", gender="F", birthday="01 JAN 1905"),
            Individual(id="I12", name="Janet Smith", gender="F", birthday="01 JAN 1990"),
        ]

    def test_parents_not_too_old(self):
        self.assertTrue(US12(self.family1, self.individuals, False))

    def test_father_too_old(self):
        self.assertFalse(US12(self.family2, self.individuals, False))

    def test_mother_too_old(self):
        self.assertFalse(US12(self.family3, self.individuals, False))

    def test_both_parents_too_old(self):
        self.assertFalse(US12(self.family4, self.individuals, False))
    
class TestUS21(unittest.TestCase):
    """
    Author: Ronnie Arvanites
    User Story: US21
    Sprint: Sprint 2
    """

    def setUp(self):
        self.by_id = {
            "I01": Individual(id="I01", name="Hayden Patton", gender="M", birthday="14 JAN 1999", age=24, alive=True),  # Male husband
            "I02": Individual(id="I02", name="Teresa Patton", gender="F", birthday="20 OCT 1999", age=24, alive=True),  # Female wife
            "I03": Individual(id="I03", name="Kenzie Nelson", gender="M", birthday="11 DEC 1977", age=46, alive=True),  # Male wife
            "I04": Individual(id="I04", name="Rory Nelson", gender="F", birthday="12 NOV 1978", age=45, alive=True),  # Female husband
            "I05": Individual(id="I04", name="Dante Portillo", gender="D", birthday="12 NOV 1980", age=43, alive=True),  # Husband with D for gender
            "I06": Individual(id="I04", name="Kiera Church", gender="K", birthday="12 NOV 1988", age=35, alive=True)  # Wife with K for gender
        }

    def test_husband_is_male(self):
        self.assertTrue(is_husband_male("I01", self.by_id))

    def test_husband_is_not_male(self):
        self.assertFalse(is_husband_male("I04", self.by_id))
    
    def test_wife_is_female(self):
        self.assertTrue(is_wife_female("I02", self.by_id))
    
    def test_wife_is_not_female(self):
        self.assertFalse(is_wife_female("I03", self.by_id))
    
    def test_wife_is_not_female_K_for_gender(self):
        self.assertFalse(is_wife_female("I05", self.by_id))
    
    def test_husband_is_not_male_with_D_for_gender(self):
        self.assertFalse(is_wife_female("I06", self.by_id))

class TestUS22(unittest.TestCase):
    """
    Author: Andrew Turcan
    User Story: US22
    Sprint: Sprint 3
    """
    def test_unique_ids(self):
        i1 = Individual('I1')
        i2 = Individual('I2')
        i3 = Individual('I1')
        self.assertTrue(unique_ids([i1, i2], False))
        self.assertFalse(unique_ids([i1, i2, i3], False))


class TestUS23(unittest.TestCase):
    """
    Author: Andrew Turcan
    User Story: US23
    Sprint: Sprint 3
    """
    def test_unique_names_and_birthdays(self):
        i1 = Individual('I1', name='Dom Thompson', birthday='11 MAR 2002')
        i2 = Individual('I2', name='Dom Thompson', birthday='30 MAR 2001')
        i3 = Individual('I3', name='Dom Thompson', birthday='20 APR 2000')
        i4 = Individual('I4', name='Dom Thompson', birthday='20 APR 2000')
        i5 = Individual('I5', name='Dif Mann', birthday='11 MAR 2002')
        self.assertTrue(unique_names_and_birthdays([i1, i2, i3], False))
        self.assertFalse(unique_names_and_birthdays([i1, i2, i3, i4], False))
        self.assertTrue(unique_names_and_birthdays([i1, i2, i3, i5], False))

class TestUS29(unittest.TestCase):
    """
    Author: Ronnie Arvanites
    User Story: US29
    Sprint: Sprint 3
    """

    def setUp(self):
        indiv1 = Individual(id="I01", name="Mark Gornik", gender="M", birthday="22 MAR 1911", age=77, alive=False)
        indiv2 = Individual(id="I02", name="Sophie McCraw", gender="F", birthday="11 NOV 1999", age=24, alive=True)
        indiv3 = Individual(id="I03", name="Jack Nelson", gender="M", birthday="02 JUL 1977", age=46, alive=True)
        indiv4 = Individual(id="I04", name="Therese Felker", gender="F", birthday="19 JAN 1902", age=92, alive=False)
        indiv5 = Individual(id="I04", name="Mabel Meraz", gender="F", birthday="16 OCT 1980", age=43, alive=True)
        indiv6 = Individual(id="I04", name="Marcus Gerberding", gender="M", birthday="17 MAY 1988", age=34, alive=False)
        self.deceased_table1 = create_deceased_individuals_table([indiv1, indiv3, indiv4]) # 2 deceased individuals
        self.deceased_table2 = create_deceased_individuals_table([indiv1, indiv5]) # 1 deceased individual
        self.deceased_table3 = create_deceased_individuals_table([indiv1, indiv4, indiv6]) # 3 deceased individuals
        self.deceased_table4 = create_deceased_individuals_table([indiv1, indiv2, indiv3, indiv4, indiv5, indiv6]) # 3 deceased individuals
        self.deceased_table5 = create_deceased_individuals_table([indiv2, indiv3, indiv5]) # 0 deceased individuals

    def test_create_deceased_individuals_table1(self):
        self.assertEqual(len(self.deceased_table1.rows), 2)

    def test_create_deceased_individuals_table2(self):
        self.assertEqual(len(self.deceased_table2.rows), 1)

    def test_create_deceased_individuals_table3(self):
        self.assertEqual(len(self.deceased_table3.rows), 3)

    def test_create_deceased_individuals_table4(self):
        self.assertEqual(len(self.deceased_table4.rows), 3)

    def test_create_deceased_individuals_table5(self):
        self.assertEqual(len(self.deceased_table5.rows), 0)

class TestUS30(unittest.TestCase):
    """
    Author: Ronnie Arvanites
    User Story: US30
    Sprint: Sprint 3
    """

    def setUp(self):
        fam1 = Family(id="F1", married="12 APR 2000", divorced="NA", husband_id="I01", husband_name="Marco Cattaneo", wife_id="I02", wife_name="Ashlee Pinkham")
        fam2 = Family(id="F2", married="19 OCT 2019", divorced="NA", husband_id="I03", husband_name="Brian Heeney", wife_id="I04", wife_name="Suzzanne Biddle")
        fam3 = Family(id="F3", married="01 FEB 2015", divorced="19 MAR 2020", husband_id="I06", husband_name="Robin Schremmer", wife_id="I05", wife_name="Sandra Bozic")
        fam4 = Family(id="F4", married="27 SEP 1945", divorced="NA", husband_id="I07", husband_name="Arian Maijala", wife_id="I08", wife_name="Hannah Moffitt")
        by_id = {
            "I01": Individual(id="I01", name="Marco Cattaneo", gender="M", birthday="19 OCT 1977", alive=True),
            "I02": Individual(id="I02", name="Ashlee Pinkham", gender="F", birthday="10 NOV 1978", alive=True),
            "I03": Individual(id="I03", name="Brian Heeney", gender="M", birthday="11 DEC 1998", alive=True),
            "I04": Individual(id="I04", name="Suzzanne Biddle", gender="F", birthday="23 NOV 1998", alive=True),
            "I05": Individual(id="I05", name="Sandra Bozic", gender="F", birthday="12 MAY 1980", alive=True),
            "I06": Individual(id="I06", name="Robin Schremmer", gender="M", birthday="22 APR 1988", alive=True),
            "I07": Individual(id="I07", name="Arian Maijala", gender="M", birthday="15 DEC 1922", alive=False),
            "I08": Individual(id="I08", name="Hannah Moffitt", gender="F", birthday="10 FEB 1911", alive=False)
        }
        self.living_and_married_table1 = create_living_and_married_individuals_table([fam1, fam2], by_id) # 4 living and married individuals
        self.living_and_married_table2 = create_living_and_married_individuals_table([fam1 , fam3, fam2], by_id) # 4 living and married individuals
        self.living_and_married_table3 = create_living_and_married_individuals_table([fam1 , fam3, fam4], by_id) # 2 living and married individuals
        self.living_and_married_table4 = create_living_and_married_individuals_table([fam1 , fam2, fam3, fam4], by_id) # 4 living and married individuals
        self.living_and_married_table5 = create_living_and_married_individuals_table([fam3, fam4], by_id) # 0 living and married individuals

    def test_create_living_and_married_table1(self):
        self.assertEqual(len(self.living_and_married_table1.rows), 4)

    def test_create_living_and_married_table2(self):
        self.assertEqual(len(self.living_and_married_table2.rows), 4)

    def test_create_living_and_married_table3(self):
        self.assertEqual(len(self.living_and_married_table3.rows), 2)

    def test_create_living_and_married_table4(self):
        self.assertEqual(len(self.living_and_married_table4.rows), 4)

    def test_create_living_and_married_table5(self):
        self.assertEqual(len(self.living_and_married_table5.rows), 0)

class TestUS31(unittest.TestCase):
    """
    Author: Ronnie Arvanites
    User Story: US31
    Sprint: Sprint 4
    """

    def setUp(self):
        fams = [
            Family(id="F1", married="12 APR 2000", divorced="NA", husband_id="I01", husband_name="Kenny Kincaide", wife_id="I02", wife_name="Catrina Belmontes"),
            Family(id="F2", married="01 FEB 2015", divorced="19 MAR 2020", husband_id="I03", husband_name="Felix Trimpe", wife_id="I04", wife_name="Abby Polhamus")
        ]
        indiv1 = Individual(id="I01", name="Kenny Kincaide", gender="M", birthday="11 MAY 1975", age=48, alive=True)
        indiv2 = Individual(id="I02", name="Catrina Belmontes", gender="F", birthday="22 DEC 1975", age=47, alive=True)
        indiv3 = Individual(id="I03", name="Felix Trimpe", gender="M", birthday="02 JUN 1985", age=38, alive=True)
        indiv4 = Individual(id="I04", name="Abby Polhamus", gender="F", birthday="21 JUL 1985", age=38, alive=True)
        indiv5 = Individual(id="I05", name="Anne Gerde", gender="F", birthday="22 MAY 1980", age=43, alive=True)
        indiv6 = Individual(id="I06", name="Alex Mulcare", gender="M", birthday="11 JUN 1960", death="10 NOV 2021", age=61, alive=False)
        indiv7 = Individual(id="I07", name="Samuel Hizer", gender="M", birthday="02 APR 1922", death="10 FEB 1999", age=77, alive=False)
        indiv8 = Individual(id="I08", name="Debora Seligmann", gender="F", birthday="10 FEB 2001", age=22, alive=True)
        indiv9 = Individual(id="I09", name="Karly Stonehill", gender="F", birthday="01 AUG 1990", age=33, alive=True)
        indiv10 = Individual(id="I10", name="Dominic Coman", gender="M", birthday="11 JUL 19", age=39, alive=True)    
    
        self.living_over_30_and_never_married_table1 = create_living_over_30_and_never_married_table([indiv1, indiv2, indiv3, indiv4, indiv5, indiv6], fams) # 1 living, over 30, and never married individual
        self.living_over_30_and_never_married_table2 = create_living_over_30_and_never_married_table([indiv1, indiv2, indiv3, indiv4, indiv5, indiv6, indiv7, indiv8], fams) # 1 living, over 30, and never married individual
        self.living_over_30_and_never_married_table3 = create_living_over_30_and_never_married_table([indiv1, indiv2, indiv3, indiv4, indiv5, indiv6, indiv7, indiv8, indiv10], fams) # 2 living, over 30, and never married individuals
        self.living_over_30_and_never_married_table4 = create_living_over_30_and_never_married_table([indiv1, indiv2, indiv3, indiv4, indiv5, indiv6, indiv7, indiv8, indiv9, indiv10], fams) # 3 living, over 30, and never married individuals
        self.living_over_30_and_never_married_table5 = create_living_over_30_and_never_married_table([indiv1, indiv2, indiv3, indiv4], fams) # 0 living, over 30, and never married individuals

    def test_create_living_and_married_table1(self):
        self.assertEqual(len(self.living_over_30_and_never_married_table1.rows), 1)

    def test_create_living_and_married_table2(self):
        self.assertEqual(len(self.living_over_30_and_never_married_table2.rows), 1)

    def test_create_living_and_married_table3(self):
        self.assertEqual(len(self.living_over_30_and_never_married_table3.rows), 2)

    def test_create_living_and_married_table4(self):
        self.assertEqual(len(self.living_over_30_and_never_married_table4.rows), 3)

    def test_create_living_and_married_table5(self):
        self.assertEqual(len(self.living_over_30_and_never_married_table5.rows), 0)

class TestUS32(unittest.TestCase):
    """
    Author: Ronnie Arvanites
    User Story: US32
    Sprint: Sprint 4
    """

    def setUp(self):
        fam1 = Family(id="F1", married="12 APR 1996", divorced="NA", husband_id="I01", husband_name="Gilbert Glossner", wife_id="I02", wife_name="Emely Braunagel", children=["I03", "I04"])
        fam2 = Family(id="F2", married="10 MAR 2015", husband_id="I06", husband_name="Wilmar Staller", wife_id="I05", wife_name="Alannah Nolan", children=["I07", "I08", "I09"])
        fam3 = Family(id="F3", married="13 SEP 2010", husband_id="I10", husband_name="Felix Trimpe", wife_id="I11", wife_name="Abby Polhamus", children=["I12", "I13", "I14"])
        #Fam1
        indiv1 = Individual(id="I01", name="Gilbert Glossner", gender="M", birthday="08 JUN 1970", spouse="F1")
        indiv2 = Individual(id="I02", name="Emely Braunagel", gender="F", birthday="23 JAN 1970", spouse="F1")  
        indiv3 = Individual(id="I03", name="David Glossner", gender="M", birthday="11 APR 1998", child="F1")
        indiv4 = Individual(id="I04", name="Melonie Glossner", gender="F", birthday="05 SEP 1999", child="F1")
        #Fam2
        indiv5 = Individual(id="I05", name="Alannah Nolan", gender="F", birthday="12 FEB 1989", spouse="F2")
        indiv6 = Individual(id="I06", name="Wilmar Staller", gender="M", birthday="13 JUL 1990", spouse="F2")
        indiv7 = Individual(id="I07", name="Franco Staller", gender="M", birthday="20 MAY 2012", child="F2")
        indiv8 = Individual(id="I08", name="Eva Staller", gender="F", birthday="20 MAY 2012", child="F2")
        indiv9 = Individual(id="I09", name="Ellen Staller", gender="F", birthday="02 FEB 2014", child="F2")
        #Fam3
        indiv10 = Individual(id="I10", name="Alonzo Zeolla", gender="M", birthday="11 JUL 1982", spouse="F3")
        indiv11 = Individual(id="I11", name="Alessia Hadwin", gender="F", birthday="03 AUG 1982", spouse="F3")
        indiv12 = Individual(id="I12", name="Daylan Zeolla", gender="M", birthday="10 NOV 2012", child="F3")
        indiv13 = Individual(id="I13", name="Wanda Zeolla", gender="F", birthday="10 NOV 2012", child="F3")
        indiv14 = Individual(id="I14", name="Aurora Zeolla", gender="F", birthday="10 NOV 2012", child="F3")
        by_id = {
            "I01": indiv1,
            "I02": indiv2,
            "I03": indiv3,
            "I04": indiv4,
            "I05": indiv5,
            "I06": indiv6,
            "I07": indiv7,
            "I08": indiv8,
            "I09": indiv9,
            "I10": indiv10,
            "I11": indiv11,
            "I12": indiv12,
            "I13": indiv13,
            "I14": indiv14
        }

        self.multiple_births_table1 = create_multiple_births_table([indiv1, indiv2, indiv3, indiv4, indiv5, indiv6, indiv7, indiv8, indiv9],[fam1, fam2], by_id) # 1 multiple birth individual
        self.multiple_births_table2 = create_multiple_births_table([indiv5, indiv6, indiv7, indiv8, indiv9, indiv10, indiv11, indiv12, indiv13, indiv14],[fam2, fam3], by_id) # 2 multiple birth individuals
        self.multiple_births_table3 = create_multiple_births_table([indiv1, indiv2, indiv3, indiv4, indiv5, indiv6, indiv7, indiv8, indiv9, indiv10, indiv11, indiv12, indiv13, indiv14],[fam1, fam2, fam3], by_id) # 2 multiple birth individuals
        self.multiple_births_table4 = create_multiple_births_table([indiv10, indiv11, indiv12, indiv13, indiv14],[fam3], by_id) # 1 multiple birth individual
        self.multiple_births_table5 = create_multiple_births_table([indiv1, indiv2, indiv3, indiv4],[fam1], by_id) # 0 multiple birth individuals

    def test_create_living_and_married_table1(self):
        self.assertEqual(len(self.multiple_births_table1.rows), 1)

    def test_create_living_and_married_table2(self):
        self.assertEqual(len(self.multiple_births_table2.rows), 2)

    def test_create_living_and_married_table3(self):
        self.assertEqual(len(self.multiple_births_table3.rows), 2)

    def test_create_living_and_married_table4(self):
        self.assertEqual(len(self.multiple_births_table4.rows), 1)

    def test_create_living_and_married_table5(self):
        self.assertEqual(len(self.multiple_births_table5.rows), 0)

class TestUS13(unittest.TestCase):
    """
    Author: Michael Scoli
    User Story: US13
    Sprint: Sprint 2
    """

    def setUp(self):
        self.family1 = Family(id="F1", children=["I01", "I02"])  # siblings born more than 8 months apart
        self.family2 = Family(id="F2", children=["I03", "I04"])  # siblings born less than 2 days apart
        self.family3 = Family(id="F3", children=["I05", "I06"])  # siblings born less than 8 months but more than 2 days apart
        self.individual1 = Individual(id="I01", name="Alice", birthday="1 JAN 2000")
        self.individual2 = Individual(id="I02", name="Bob", birthday="1 SEP 2000")
        self.individual3 = Individual(id="I03", name="Charlie", birthday="1 JAN 2000")
        self.individual4 = Individual(id="I04", name="David", birthday="2 JAN 2000")
        self.individual5 = Individual(id="I05", name="Eve", birthday="1 JAN 2000")
        self.individual6 = Individual(id="I06", name="Frank", birthday="1 MAR 2000")
        self.individuals = [self.individual1, self.individual2, self.individual3, self.individual4, self.individual5, self.individual6]

    def test_sibling_spacing(self):
        self.assertTrue(US13(self.family1, self.individuals, False))  # siblings born more than 8 months apart
        self.assertTrue(US13(self.family2, self.individuals, False))  # siblings born less than 2 days apart
        self.assertFalse(US13(self.family3, self.individuals, False)) # siblings born less than 8 months but more than 2 days apart



class TestUS27(unittest.TestCase):
    """
    Author: Michael Scoli
    User Story: US27
    Sprint: Sprint 3
    """

    def setUp(self):
        self.individuals = [
            Individual(id="I01", name="James Kern", gender="M", birthday="20 OCT 2001", age=21, alive=True),
            Individual(id="I02", name="Kevin Burns", gender="M", birthday="18 FEB 2002", age=21, alive=True),
            Individual(id="I03", name="Gary Paul", gender="M", birthday="14 MAY 1999", age=24, alive=True),
            Individual(id="I04", name="Jack Simons", gender="M", birthday="12 DEC 2000", age=22, alive=True)
        ]

    def test_individual_age_inclusion(self):
        individuals_table = PrettyTable()
        individuals_table.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]

        for indiv in self.individuals:
            child_field = "None" if indiv.child == "NA" else "{'%s'}" % indiv.child
            spouse_field = "NA" if indiv.spouse == "NA" else "{'%s'}" % indiv.spouse
            individuals_table.add_row([indiv.id, indiv.name, indiv.gender, indiv.birthday, indiv.age, indiv.alive, indiv.death, child_field, spouse_field])

        for row in individuals_table.get_string().split('\n')[3:-1]:  # Skip headers and separator lines
            individual_id = row.split('|')[1].strip()  # Split by '|' and strip spaces
            expected_age = next((indiv.age for indiv in self.individuals if indiv.id == individual_id), None)
            if expected_age is not None:
                actual_age = int(row.split('|')[5].strip())  # Split by '|' and strip spaces
                self.assertEqual(actual_age, expected_age)
            else:
                self.fail(f'Individual with ID {individual_id} not found in self.individuals')


class TestUS28(unittest.TestCase):
    """
    Author: Michael Scoli
    User Story: US28
    Sprint: Sprint 3
    """

    def setUp(self):
        indiv1 = Individual(id="I01", name="Mark Gornik", gender="M", birthday="22 MAR 1911", age=77, alive=False)
        indiv2 = Individual(id="I02", name="Sophie McCraw", gender="F", birthday="11 NOV 1999", age=24, alive=True)
        indiv3 = Individual(id="I03", name="Jack Nelson", gender="M", birthday="02 JUL 1977", age=46, alive=True)
        indiv4 = Individual(id="I04", name="Therese Felker", gender="F", birthday="19 JAN 1902", age=92, alive=False)

        fam1 = Family(id="F01", married="22 FEB 1930", divorced="NA", husband_id="I01", husband_name=indiv1.name, wife_id="I02", wife_name=indiv2.name, children=["'I03'", "'I04'"])

        self.by_id = {"I01": indiv1, "I02": indiv2, "I03": indiv3, "I04": indiv4}
        self.siblings_by_age_table1 = create_siblings_by_age_table([fam1], self.by_id)  # 2 siblings

    def test_create_siblings_by_age_table1(self):
        self.assertEqual(len(self.siblings_by_age_table1.rows), 2)

        # Ensure the siblings are sorted by age in descending order
        previous_age = float('inf')
        for row in self.siblings_by_age_table1._rows:
            age = int(row[3])  # Age column is at index 3
            self.assertGreaterEqual(previous_age, age)
            previous_age = age


class TestUS35(unittest.TestCase):
    """
    Author: Michael Scoli
    User Story: US35
    Sprint: Sprint 4
    """

    def setUp(self):
        today = datetime.today()
        ten_days_ago = (today - timedelta(days=10)).strftime('%d %b %Y')
        forty_days_ago = (today - timedelta(days=40)).strftime('%d %b %Y')
        ten_days_later = (today + timedelta(days=10)).strftime('%d %b %Y')

        self.by_id = {
            "I01": Individual(id="I01", name="Alice Thompson", gender="F", birthday=ten_days_ago, death="NA", age=10),
            "I02": Individual(id="I02", name="Bob Johnson", gender="M", birthday=forty_days_ago, death="NA", age=40),
            "I03": Individual(id="I03", name="Charlie Brown", gender="M", birthday=ten_days_later, death="NA", age=-10),
        }

        self.born_in_last_30_days_table = create_born_in_last_30_days_table(self.by_id)

    def test_create_born_in_last_30_days_table1(self):
        # Retrieve the names from the rows. Assuming the 'Name' column is the second column in the table.
        names_in_table = [list(row)[1] for row in self.born_in_last_30_days_table._rows]  # use _rows to access the rows
        self.assertEqual(len(names_in_table), 1)
        self.assertIn("Alice Thompson", names_in_table)


class TestUS36(unittest.TestCase):
    """
    Author: Michael Scoli
    User Story: US36
    Sprint: Sprint 4
    """

    def setUp(self):
        today = datetime.today()
        five_days_ago = (today - timedelta(days=5)).strftime('%d %b %Y')
        twenty_nine__days_ago = (today - timedelta(days=29)).strftime('%d %b %Y')

        # Example individuals. Adjust these according to your data structure.
        indiv1 = Individual(id="I01", name="Bob Smith", birthday="10 JAN 2000", death=twenty_nine__days_ago)  # Died 29 days ago
        indiv2 = Individual(id="I02", name="Jane Doe", birthday="5 JAN 1980",
                            death="5 JUN 2022")  # Died over a year ago
        indiv3 = Individual(id="I03", name="John Snow", birthday="10 JAN 1990", death=five_days_ago) # Died 5 days ago

        # Convert to a dictionary format for the by_id structure.
        self.by_id = {
            "I01": indiv1,
            "I02": indiv2,
            "I03": indiv3
        }

        # Create the table using the function
        self.died_in_last_30_days_table = create_died_in_last_30_days_table(self.by_id)

    def test_create_died_in_last_30_days_table(self):
        # Retrieve the names from the rows. Assuming the 'Name' column is the second column in the table.
        names_in_table = [list(row)[1] for row in self.died_in_last_30_days_table._rows]

        # Check that there are 2 individuals in the table.
        self.assertEqual(len(names_in_table), 2)

        # Check that both Bob Smith and John Snow are in the table, but Jane Doe isn't.
        self.assertIn("Bob Smith", names_in_table)
        self.assertIn("John Snow", names_in_table)
        self.assertNotIn("Jane Doe", names_in_table)


if __name__ == '__main__':
    unittest.main()
