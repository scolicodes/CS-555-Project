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
    Author: Your Name
    User Story: US12
    Sprint: Sprint 1
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


if __name__ == '__main__':
    unittest.main()
