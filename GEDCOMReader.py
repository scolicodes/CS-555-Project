import re
from datetime import datetime, date, timedelta

from prettytable import PrettyTable


class Individual:
    def __init__(self, id, name="NA", gender="NA", birthday="NA", age="NA", alive=True, death="NA", child="NA",
                 spouse="NA"):
        self.id = id
        self.name = name
        self.gender = gender
        self.birthday = birthday
        self.age = age
        self.alive = alive
        self.death = death
        self.child = child
        self.spouse = spouse


class Family:
    def __init__(self, id, married="NA", divorced="NA", husband_id="NA", husband_name="NA", wife_id="NA",
                 wife_name="NA", children="NA"):
        self.id = id
        self.married = married
        self.divorced = divorced
        self.husband_id = husband_id
        self.husband_name = husband_name
        self.wife_id = wife_id
        self.wife_name = wife_name
        self.children = children

    def validate_dates(self):
        if self.married and self.divorced:
            married_date = to_date(self.married)
            divorced_date = to_date(self.divorced)
            if divorced_date < married_date:
                return False, "Divorce date {} is before marriage date {}".format(self.divorced, self.married)
        elif not self.married and self.divorced:
            return False, "Divorce date {} exists, but there is no marriage date".format(self.divorced)
        return True, None


def to_date(string: str):
    try:
        return datetime.strptime(string, "%d %b %Y")
    except ValueError:
        print(f'ERROR: US42: Invalid date "{string}"')


by_id = {}


# Code for User Stories
def check_born_before_married(family, printErrors=True, by_id=by_id):
    """Satisfies US02"""
    if family.married == "NA" or family.married is None:
        return True
    marriage_date = to_date(family.married)

    def validate_bday(id):
        bday = by_id[id].birthday
        return bday is None or bday == "NA" or to_date(bday) < marriage_date

    if validate_bday(family.wife_id) and validate_bday(family.husband_id):
        return True
    else:
        if printErrors:
            print(f"ERROR: FAMILY: US02: {family.id}: Married {family.married} before birth")
        return False


def check_born_before_death(indi: Individual, printErrors=True):
    """Satisfies US03"""
    if indi.death == "NA" or indi.death is None or indi.birthday == "NA" or indi.birthday is None:
        return True

    birth = to_date(indi.birthday)
    death = to_date(indi.death)
    if birth < death:
        return True
    else:
        if printErrors:
            print(f"ERROR: INDIVIDUAL: US03: {indi.id}: Died {indi.death} before born {indi.birthday}")


def check_no_quintuplets_and_beyond(fam: Family, by_id=by_id, print_errors=True):
    """Satisfies US14 (5+ births at the same time not allowed)"""
    children = fam.children
    if isinstance(children, list):
        birthdays = [to_date(by_id[child.strip("'")].birthday) for child in children]
        # sort
        birthdays.sort()
        births = 1
        prev = None
        for birthday in birthdays:
            if prev is not None:
                # might be 1 day apart if born at/around midnight
                if (birthday - prev).days <= 1:
                    births += 1
                    if births >= 5:
                        if print_errors:
                            print(f"ERROR: FAMILY: US14: {fam.id}: >=5 births detected at the same time")
                        return False
                    continue
            births = 1
            prev = birthday

    return True


def check_under15_siblings(fam: Family, print_errors=True):
    """Satisfies US15 (15+ siblings not allowed)"""
    if isinstance(fam.children, list) and len(fam.children) >= 15:
        if print_errors:
            print(f"ERROR: FAMILY: US15: {fam.id}: >=15 siblings detected in family")
        return False
    return True

def check_male_members_last_name(fam, by_id=by_id, print_errors=True):
    if fam.children == "NA":
         return True
    last_names_match = True
    husband_obj = by_id[fam.husband_id]
    husband_name_arr= husband_obj.name.split()
    husband_last_name = husband_name_arr[-1].strip('/')
    for child in fam.children:
        child_id = child.strip('\'')
        child_obj = by_id[child_id]
        if child_obj.gender == "M":
            name_arr= child_obj.name.split()
            last_name = name_arr[-1].strip('/')
            if last_name != husband_last_name:
                if print_errors:
                    print(f"ERROR: INDIVIDUAL: US16: {child_id}: Last name ({last_name}) does not match parent's ({fam.husband_id}) last name ({husband_last_name})")
                last_names_match = False
    return last_names_match

def is_husband_male(husband_id, by_id=by_id):
    husband_obj = by_id[husband_id]
    if husband_obj.gender != "M":
        return False
    return True

def is_wife_female(wife_id, by_id=by_id):
    wife_obj = by_id[wife_id]
    if wife_obj.gender != "F":
        return False
    return True

def US04(family, printErrors=True):
    if family.divorced == "NA":  # No divorce occurred
        return True

    marriage_date = to_date(family.married)
    divorce_date = to_date(family.divorced)

    if marriage_date > divorce_date:
        if printErrors:
            print(f"ERROR: FAMILY: US04: {family.id}: Divorced {family.divorced} before married {family.married}")
        return False
    return True

def US05(family, individuals, printErrors=True):
    if family.married == "NA":  # No marriage occurred
        return True

    marriage_date = to_date(family.married)

    spouse_ids = {family.husband_id, family.wife_id}
    for indiv in individuals:
        if indiv.id in spouse_ids:
            spouse_ids.remove(indiv.id)  # Remove the spouse from the set of spouses to check
            if indiv.death is not None and indiv.death != "NA":
                death_date = to_date(indiv.death)
                if marriage_date > death_date:
                    if printErrors:
                        print(f"ERROR: FAMILY: US05: {family.id}: Married {family.married} after death {indiv.death} of individual {indiv.id}")
                    return False
            if not spouse_ids:  # If we've checked both spouses, we can break early
                break

    return True

def US06(family, individuals, printErrors=True):
    if family.divorced == "NA": #No divorce
        return True
    
    divorce_date = to_date(family.divorced)

    family_ids = {family.husband_id, family.wife_id}
    for i in individuals:
        if i.id in family_ids:
            family_ids.remove(i.id)
            if i.death is not None and i.death != "NA":
                death_date = to_date(i.death)
                if divorce_date > death_date:
                    type = "husband" if i.id == family.husband_id else "wife"
                    if printErrors:
                        return (f"ERROR: FAMILY: US06: {family.id}: Divorced {family.divorced} after {type}'s ({i.id}) death on {i.death}")
                    return False
            if not family_ids:
                break

    return True

def US08(family, individuals, printErrors = True):
    if not family.children or family.children == "NA":
        return True

    if family.married == "NA" and family.divorced == "NA":
        child = family.children[0].strip('\'')
        if printErrors:
            print(f"ANOMALY: FAMILY: US08: {family.id}: Child {child} before marriage (unmarried)")
        return False

    marriage_date = to_date(family.married)
    
    for c in family.children:
        for i in individuals:
            c = c.strip('\'')
            if c == i.id and to_date(i.birthday) < marriage_date:
                if printErrors:
                    print(f"ANOMALY: FAMILY: US08: {family.id}: Child {c} before marriage on {family.married}")
                return False
        
    return True

def US09(family, individuals, printErrors=True):
    """Child should be born before death of mother and before 9 months after death of father"""
    if family.children == "NA":
        return True
    
    death_date = ""
    for i in individuals:
        if i.id == family.wife_id:
            if i.death is not None and i.death != "NA":
                death_date = to_date(i.death)
    
    husband_threshold = death_date + timedelta(days=270)

    for i in individuals:
        if i.id == family.husband_id:
            if i.death is not None and i.death != "NA" and to_date(i.death) < husband_threshold:
                death_date = to_date(i.death) + timedelta(days=270)
    
    for c in family.children:
        for i in individuals:
            c = c.strip('\'')
            if c == i.id and to_date(i.birthday) > death_date:
                if printErrors:
                    print(f"ERROR: FAMILY: US09: {family.id}: Child {c} after parent death on {death_date}")
                return False
        
    return True

def US10(family, individuals, printErrors=True):
    """Marriage should be at least 14 years after birth of both spouses (parents must be at least 14 years old)"""
    
    if family.married == "NA":
        return True
    
    marriage_date = to_date(family.married)

    for i in individuals:
        if i.id == family.wife_id:
            birth_date = to_date(i.birthday)

    for i in individuals:
        if i.id == family.husband_id and to_date(i.birthday) > birth_date:
            birth_date = to_date(i.birthday)

    threshold = birth_date.replace(year=birth_date.year + 14)
    
    if threshold > marriage_date:
        if printErrors:
            print(f"ERROR: FAMILY: US10: {family.id}: Marriage less than 14 years after parent birth on {birth_date}")
        return False
        
    return True

def US24(families, individuals, printErrors=True):
    """No more than one family with the same spouses by name and the same marriage date should appear in a GEDCOM file"""
    
    unique_families = []

    for f in families:
        for i in individuals:
            if f.wife_id == i.id:
                wife_name = i.name
            if f.husband_id == i.id:
                husband_name = i.name
        if (husband_name, wife_name, to_date(f.married)) in unique_families:
            if printErrors:
                        print(f"ERROR: FAMILY: US24: {f.id}: Family with the same spouse names and marriage date")
            return False
        unique_families.append((husband_name, wife_name, to_date(f.married)))
        
    return True

def US25(family, individuals, printErrors=True):
    """No more than one child with the same name and birth date should appear in a family"""
    
    unique_children = [("", "")]

    for c in family.children:
        for i in individuals:
            c = c.strip('\'')
            if c == i.id:
                if (i.name, i.birthday) in unique_children:
                    if printErrors:
                        print(f"ERROR: FAMILY: US25: {family.id}: 2 children with same name {i.name} and birthday {i.birthday} in family")
                    return False
                unique_children.append((i.name, i.birthday))
        
    return True

def US12(family, individuals, printErrors=True):
    """Mother should be less than 60 years older than her children and
    father should be less than 80 years older than his children"""
    flag = True

    if family.children == "NA":
        return flag

    if printErrors:
        husband_bday = to_date(by_id[family.husband_id].birthday)
        wife_bday = to_date(by_id[family.wife_id].birthday)
    else:
        husband_bday = to_date(next((obj for obj in individuals if obj.id == family.husband_id), None).birthday)
        wife_bday = to_date(next((obj for obj in individuals if obj.id == family.wife_id), None).birthday)

    for child_id in family.children:
        if printErrors:
            child_bday = to_date(by_id[child_id.strip('\'')].birthday)
        else:
            child_bday = to_date(next((obj for obj in individuals if obj.id == child_id), None).birthday)
        if (child_bday.year - husband_bday.year) > 80:
            if printErrors:
                print(f"ERROR: FAMILY: US12: {family.id}: Father {family.husband_id} is more than 80 years older than child {child_id}")
            flag = False
        if (child_bday.year + -wife_bday.year) > 60:
            if printErrors:
                print(
                    f"ERROR: FAMILY: US12: {family.id}: Mother {family.wife_id} is more than 60 years older than child {child_id}")
            flag = False
    return flag


def US13(family, individuals, printErrors=True):
    """Birth dates of siblings should be more than 8 months apart or less than 2 days apart
    (twins may be born one day apart, e.g. 11:59 PM and 12:02 AM the following calendar day)"""

    # If there's only once child or no children, there's no need to check anything.
    if family.children == "NA" or len(family.children) < 2:
        return True

    # Convert string dates to datetime objects and sort them.
    if printErrors:
        sorted_bdays = sorted(to_date(by_id[child_id.strip('\'')].birthday) for child_id in family.children)
    else:
        children = list(filter(lambda x: x.id in family.children, individuals))
        sorted_bdays = sorted(to_date(child.birthday) for child in children)

    for i in range(len(sorted_bdays) - 1):
        difference = sorted_bdays[i + 1] - sorted_bdays[i]
        # If the difference is more than 2 days but less than 8 months, there's a problem.
        if 2 < difference.days < 240:
            if printErrors:
                print(
                    f"ERROR: FAMILY: US13: {family.id}: There is less than 8 months and more than 2 days between "
                    f"siblings' birthdays")
            return False

    return True


def calculate_age(birth_date, death_date="NA"):
    if death_date != "NA":
        birth_date_object = to_date(birth_date).date()
        death_date_object = to_date(death_date).date()
        age = death_date_object.year - birth_date_object.year
        if death_date_object.month < birth_date_object.month or (
                death_date_object.month == birth_date_object.month and death_date_object.day < birth_date_object.day):
            age -= 1
        return age
    else:
        birth_date_object = to_date(birth_date).date()
        current_date = date.today()
        age = current_date.year - birth_date_object.year
        if current_date.month < birth_date_object.month or (
                current_date.month == birth_date_object.month and current_date.day < birth_date_object.day):
            age -= 1
        return age

def find_name_for_id(id):
    for individual in individuals:
        if individual.id == id:
            return individual.name


def date_after_current_date(date):
    current_date = datetime.now().date()
    date = to_date(date).date()
    return date > current_date


def age_over_150(indiv):
    return indiv.age > 150


def unique_ids(indivs: list[Individual], printErrors=True):
    """Satisfies US22 (All individuals have unique ids)"""
    if len(indivs) == len({i.id for i in indivs}):
        return True
    if printErrors:
        print("US22: Error: Duplicate ID's found in individuals")
    return False


def unique_names_and_birthdays(indivs: list[Individual], printErrors=True):
    """Satisfies US23 (All individuals do not share both a name and birthday)"""
    if len(indivs) == len({(i.name, i.birthday) for i in indivs}):
        return True
    if printErrors:
        print("US23: Error: Duplicate name and birthday for 2+ individuals")
    return False


def create_deceased_individuals_table(indivs):
    deceased_table = PrettyTable()
    deceased_table.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
    for indiv in indivs:
        if indiv.alive == False:
            child_field = "None" if indiv.child == "NA" else "{'%s'}" % indiv.child
            spouse_field = "NA" if indiv.spouse == "NA" else "{'%s'}" % indiv.spouse
            deceased_table.add_row(
                [indiv.id, indiv.name, indiv.gender, indiv.birthday, indiv.age, indiv.alive, indiv.death, child_field, spouse_field])
    return deceased_table

def create_living_and_married_individuals_table(families, by_id=by_id):
    living_and_married_table = PrettyTable()
    living_and_married_table.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
    married_ids = set()
    for fam in families:
        if fam.divorced == "NA":
            married_ids.add(fam.husband_id)
            married_ids.add(fam.wife_id)
    for id in married_ids:
        indiv = by_id[id]
        if indiv.alive:
            child_field = "None" if indiv.child == "NA" else "{'%s'}" % indiv.child
            spouse_field = "NA" if indiv.spouse == "NA" else "{'%s'}" % indiv.spouse
            living_and_married_table.add_row(
                [indiv.id, indiv.name, indiv.gender, indiv.birthday, indiv.age, indiv.alive, indiv.death, child_field, spouse_field])
    return living_and_married_table

def create_living_over_30_and_never_married_table(indivs, families):
    living_over_30_and_never_married_table = PrettyTable()
    living_over_30_and_never_married_table.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
    married_ids = set()
    for fam in families:
        married_ids.add(fam.husband_id)
        married_ids.add(fam.wife_id)
    for indiv in indivs:
        if indiv.alive == True and indiv.age > 30 and indiv.id not in married_ids:
            child_field = "None" if indiv.child == "NA" else "{'%s'}" % indiv.child
            spouse_field = "NA" if indiv.spouse == "NA" else "{'%s'}" % indiv.spouse
            living_over_30_and_never_married_table.add_row(
                [indiv.id, indiv.name, indiv.gender, indiv.birthday, indiv.age, indiv.alive, indiv.death, child_field, spouse_field])
    return living_over_30_and_never_married_table

def create_multiple_births_table(indivs, families, by_id=by_id):
    multiple_births_table = PrettyTable()
    multiple_births_table.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
    fam_ids_with_multiple_births = set()
    for indiv in indivs:
        filtered_indivs = list(filter(lambda person: person.birthday == indiv.birthday and person.child == indiv.child, indivs))
        if len(filtered_indivs) > 1:
            fam_ids_with_multiple_births.add(indiv.child)
    for fam_id in fam_ids_with_multiple_births:
        family = [fam for fam in families if fam.id == fam_id]
        wife_obj = by_id[family[0].wife_id]
        child_field = "None" if wife_obj.child == "NA" else "{'%s'}" % wife_obj.child
        spouse_field = "NA" if wife_obj.spouse == "NA" else "{'%s'}" % wife_obj.spouse
        multiple_births_table.add_row([wife_obj.id, wife_obj.name, wife_obj.gender, wife_obj.birthday, wife_obj.age, wife_obj.alive, wife_obj.death, child_field, spouse_field])
    return multiple_births_table

def create_siblings_by_age_table(families, by_id=by_id):
    """Satisfies US28"""
    siblings_by_age_table = PrettyTable()
    siblings_by_age_table.field_names = ["Family ID", "Sibling ID", "Name", "Age"]
    for family in families:
        if family.children != "NA":
            # Get a list of siblings (children of the family) with their age
            siblings = [(child_id.strip("'"), by_id[child_id.strip("'")].name, by_id[child_id.strip("'")].age) for child_id in family.children]

            # Sort the list by age, in decreasing order
            siblings.sort(key=lambda x: x[2], reverse=True)
            # Add rows to the table
            for sibling in siblings:
                siblings_by_age_table.add_row([family.id] + list(sibling))
    return siblings_by_age_table


def create_born_in_last_30_days_table(by_id=by_id):
    """Satisfies US35"""
    table = PrettyTable()
    table.field_names = ["ID", "Name", "Birthday"]

    today = datetime.today()
    thirty_days_ago = today - timedelta(days=30)

    for individual_id, individual in by_id.items():
        birth_date = to_date(individual.birthday)

        if thirty_days_ago <= birth_date <= today:
            table.add_row([individual.id, individual.name, individual.birthday])

    return table


def create_died_in_last_30_days_table(by_id=by_id):
    """Satisfies US36"""
    table = PrettyTable()
    table.field_names = ["ID", "Name", "Death Date"]

    today = datetime.today()
    thirty_days_ago = today - timedelta(days=30)

    for individual_id, individual in by_id.items():
        if individual.death != "NA":
            death_date = to_date(individual.death)
            if thirty_days_ago <= death_date <= today:
                table.add_row([individual.id, individual.name, individual.death])

    return table


def create_survivors_in_last30days_tables(families, by_id=by_id):
    """Satisfies US37"""
    today = datetime.today()
    thirty_days_ago = today - timedelta(days=30)
    res = []
    for family in families:
        if family.divorced != "NA":
            continue
        for id in (family.wife_id, family.husband_id):
            indi = by_id[id]
            if indi.death != "NA" and thirty_days_ago <= to_date(indi.death) <= today:
                survivors = [family.wife_id, family.husband_id]
                if isinstance(family.children, list):
                    survivors += family.children
                survivors = [indi for indi in (by_id[id.strip("'")] for id in survivors) if indi.death == "NA"]
                table = PrettyTable()
                table.field_names = ["ID", "Name"]
                table.title = f'Living spouses and children of {indi.name}'
                for survivor in survivors:
                    table.add_row([survivor.id, survivor.name])
                res.append(table)
    return res


if __name__ == '__main__':
    file_name = input("Please enter the file name: ") or 'TestFamilyTree.ged'
else:
    file_name = 'TestFamilyTree.ged'
file_to_read = open(file_name, 'r')
lines = file_to_read.readlines()
valid_tags = ["INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "FAM", "MARR", "HUSB", "WIFE", "CHIL", "DIV",
              "DATE", "HEAD", "TRLR", "NOTE"]
individuals = []
families = []
tag = None
# Loop through each line
for line in lines:
    line = line.strip()
    print("--> " + line)
    components = line.split()
    level = components.pop(0)
    if bool(re.search(r'\d', components[0])):
        prev_tag = tag
        tag = components.pop(1)
    else:
        prev_tag = tag
        tag = components.pop(0)
    if tag in valid_tags:
        is_valid = 'Y'
        # Checks if tag is individual
        if level == "0" and tag == "INDI":
            individual_Id = " ".join(components)
            individuals.append(Individual(individual_Id))
        elif level == "0" and tag == "FAM":
            family_Id = " ".join(components)
            families.append(Family(family_Id))
        elif level == "1" and tag == "NAME":
            name = " ".join(components)
            individuals[-1].name = name
        elif tag == "SEX":
            gender = " ".join(components)
            individuals[-1].gender = gender
        elif prev_tag == "BIRT" and tag == "DATE":
            birthday = " ".join(components)
            individuals[-1].birthday = birthday
            individuals[-1].age = calculate_age(birthday)
        elif prev_tag == "DEAT" and tag == "DATE":
            death = " ".join(components)
            individuals[-1].death = death
            individuals[-1].age = calculate_age(birthday, death)
            individuals[-1].alive = False
        elif tag == "FAMS":
            spouse = " ".join(components)
            individuals[-1].spouse = spouse
        elif tag == "FAMC":
            child = " ".join(components)
            individuals[-1].child = child
        elif tag == "HUSB":
            husband_id = " ".join(components)
            husband_name = find_name_for_id(husband_id)
            families[-1].husband_id = husband_id
            families[-1].husband_name = husband_name
        elif tag == "WIFE":
            wife_id = " ".join(components)
            wife_name = find_name_for_id(wife_id)
            families[-1].wife_id = wife_id
            families[-1].wife_name = wife_name
        elif tag == "CHIL":
            current_children = families[-1].children
            if current_children == "NA":
                current_children = ["'%s'" % (" ".join(components))]
            else:
                current_children.append("'%s'" % (" ".join(components)))
            families[-1].children = current_children
        elif prev_tag == "MARR" and tag == "DATE":
            married = " ".join(components)
            families[-1].married = married
        elif prev_tag == "DIV" and tag == "DATE":
            divorced = " ".join(components)
            families[-1].divorced = divorced
    else:
        is_valid = 'N'
    if len(components) != 0:
        print("<-- " + level + "|" + tag + "|" + is_valid + "|" + " ".join(components))
    else:
        print("<-- " + level + "|" + tag + "|" + is_valid)

file_to_read.close()

by_id.update({indi.id: indi for indi in individuals})

# Individuals Table
individuals_table = PrettyTable()
individuals_table.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
for indiv in individuals:
    if indiv.birthday != "NA" and date_after_current_date(indiv.birthday):
        print(f"ERROR: INDIVIDUAL US01: {indiv.id}: Birthday {indiv.birthday} occurs in future")
    if indiv.death != "NA" and date_after_current_date(indiv.death):
        print(f"ERROR: INDIVIDUAL US01: {indiv.id}: Death {indiv.death} occurs in future")
    check_born_before_death(indiv)
    if age_over_150(indiv):
        if indiv.death == "NA":
            print(f"ERROR: INDIVIDUAL US07: {indiv.id}: More than 150 years old - Birth date {indiv.birthday}")
        else:
            print(f"ERROR: INDIVIDUAL US07: {indiv.id}: More than 150 years old at death - Birth date {indiv.birthday}: Death {indiv.death}")

    child_field = "None" if indiv.child == "NA" else "{'%s'}" % indiv.child
    spouse_field = "NA" if indiv.spouse == "NA" else "{'%s'}" % indiv.spouse
    individuals_table.add_row(
        [indiv.id, indiv.name, indiv.gender, indiv.birthday, indiv.age, indiv.alive, indiv.death, child_field, spouse_field])
# individuals check
unique_ids(individuals)
unique_names_and_birthdays(individuals)

# Families Table
families_table = PrettyTable()
families_table.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name",
                              "Children"]

# Families check
US24(families, individuals)

for fam in families:
    US04(fam)
    US05(fam, individuals)
    US06(fam, individuals)
    US08(fam, individuals)
    US25(fam, individuals)
    check_born_before_married(fam)
    check_male_members_last_name(fam)
    US12(fam, None)
    US13(fam, None)
    check_no_quintuplets_and_beyond(fam)
    check_under15_siblings(fam)

    if fam.married != "NA" and date_after_current_date(fam.married):
        print(f"ERROR: FAMILY: US01: {fam.id}: Marriage date {fam.married} occurs in future")
    if fam.divorced != "NA" and date_after_current_date(fam.divorced):
        print(f"ERROR: FAMILY: US01: {fam.id}: Divorce date {fam.divorced} occurs in future")
    if fam.children != "NA":
        row = [fam.id, fam.married, fam.divorced, fam.husband_id, fam.husband_name, fam.wife_id,
               fam.wife_name, "{%s}" % ",".join(fam.children)]
    else:
        row = [fam.id, fam.married, fam.divorced, fam.husband_id, fam.husband_name, fam.wife_id,
               fam.wife_name, "NA"]
    if not is_husband_male(fam.husband_id):
        print(f"ERROR: FAMILY: US21: {fam.husband_id}: Husband is not male.")
    if not is_wife_female(fam.wife_id):
        print(f"ERROR: FAMILY: US21: {fam.wife_id}: Wife is not female.")
    families_table.add_row(row)

# Print Individuals Table
print()
print('Individuals')
print(individuals_table)

# Print Family Table
print()
print('Families')
print(families_table)

#Print Deceased Individuals Table
print()
print('Deceased Individuals')
print(create_deceased_individuals_table(individuals))

#Print Living and Married Individuals Table
print()
print('Living and Married Individuals')
print(create_living_and_married_individuals_table(families))

# Print Siblings-By-Age Table
print()
print('List Siblings in Families by Decreasing Age')
print(create_siblings_by_age_table(families))

# Print Individuals Born in Last 30 Days Table
print()
print('Individuals who were born in the last 30 days')
print(create_born_in_last_30_days_table())

# Print Individuals Who Died in Last 30 Days Table
print()
print('Individuals who died in the last 30 days')
print(create_died_in_last_30_days_table())

# Print Living, Over 30, and Never Married Table
print()
print('Living, Over 30, and Never Married')
print(create_living_over_30_and_never_married_table(individuals, families))

# Print Multiple Births Table
print()
print('Multiple Births Table')
print(create_multiple_births_table(individuals, families))

for table in create_survivors_in_last30days_tables(families):
    print()
    print(table)
