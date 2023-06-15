import re
from datetime import datetime, date
from prettytable import PrettyTable


class individual:
    def __init__(self, id, name="NA", gender="NA", birthday="NA", age="NA", alive="NA", death="NA", child="NA",
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


class family:
    def __init__(self, id, married="NA", divorced="NA", husband_Id="NA", husband_name="NA", wife_Id="NA",
                 wife_name="NA", children="NA"):
        self.id = id
        self.married = married
        self.divorced = divorced
        self.husband_Id = husband_Id
        self.husband_name = husband_name
        self.wife_Id = wife_Id
        self.wife_name = wife_name
        self.children = children

    def validate_dates(self):
        if self.married and self.divorced:
            married_date = datetime.strptime(self.married, "%d %b %Y")
            divorced_date = datetime.strptime(self.divorced, "%d %b %Y")
            if divorced_date < married_date:
                return False, "Divorce date {} is before marriage date {}".format(self.divorced, self.married)
        elif not self.married and self.divorced:
            return False, "Divorce date {} exists, but there is no marriage date".format(self.divorced)
        return True, None


# Code for User Stories
def US04(family, printErrors=True):
    if family.divorced == "NA":  # No divorce occurred
        return True

    marriage_date = datetime.strptime(family.married, "%d %b %Y")
    divorce_date = datetime.strptime(family.divorced, "%d %b %Y")

    if marriage_date > divorce_date:
        if printErrors:
            print(f"ERROR: US04: {family.id}: Divorced {family.divorced} before married {family.married}")
        return False

    return True


def US05(family, individuals, printErrors=True):
    if family.married == "NA":  # No marriage occurred
        return True

    marriage_date = datetime.strptime(family.married, "%d %b %Y")

    spouse_ids = {family.husband_Id, family.wife_Id}
    for indiv in individuals:
        if indiv.id in spouse_ids:
            spouse_ids.remove(indiv.id)  # Remove the spouse from the set of spouses to check
            if indiv.death is not None and indiv.death != "NA":
                death_date = datetime.strptime(indiv.death, "%d %b %Y")
                if marriage_date > death_date:
                    if printErrors:
                        print(f"ERROR: US05: {family.id}: Married {family.married} after death {indiv.death} of individual {indiv.id}")
                    return False
            if not spouse_ids:  # If we've checked both spouses, we can break early
                break

    return True

def US06(family, individuals, printErrors=True):
    if family.divorced == "NA": #No divorce
        return True
    
    divorce_date = datetime.strptime(family.divorced, "%d %b %Y")

    family_ids = {family.husband_Id, family.wife_Id}
    for i in individuals:
        if i.id in family_ids:
            family_ids.remove(i.id)
            if i.death is not None and i.death != "NA":
                death_date = datetime.strptime(i.death, "%d %b %Y")
                if divorce_date > death_date:
                    if printErrors:
                        print(f"ERROR: US06: {family.id}: Divorced {family.divorced} after death {i.death} of individual {i.id}")
                    return False
            if not family_ids:
                break

    return True

def US08(family, individuals, printErrors = True):
    if not family.children:
        return True

    if family.married == "NA" and family.divorced == "NA":
        if printErrors:
            print(f"ERROR: US08: {family.id}: Had child {family.children[0]} before marriage (unmarried)")
        return False

    marriage_date = datetime.strptime(family.married, "%d %b %Y")
    birth_date = individuals[0].birthday # Temp variable

    for i in individuals:
        if family.children[0].strip('\'') == i.id:
            birth_date = datetime.strptime(i.birthday, "%d %b %Y")

    if birth_date < marriage_date:
        if printErrors:
            print(f"ERROR: US08: {family.id}: Had child {family.children[0]} before marriage {family.married}")
        return False


    return True


def calculate_age(birth_date, death_date=None):
    if death_date is not None:
        birth_date_object = datetime.strptime(birth_date, "%d %b %Y").date()
        death_date_object = datetime.strptime(death_date, "%d %b %Y").date()
        age = death_date_object.year - birth_date_object.year
        if death_date_object.month < birth_date_object.month or (
                death_date_object.month == birth_date_object.month and death_date_object.day < birth_date_object.day):
            age -= 1
        return age
    else:
        birth_date_object = datetime.strptime(birth_date, "%d %b %Y").date()
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


file_name = input("Please enter the file name: ")
file_to_read = open(file_name, 'r')
lines = file_to_read.readlines()
valid_tags = ["INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "FAM", "MARR", "HUSB", "WIFE", "CHIL", "DIV",
              "DATE", "HEAD", "TRLR", "NOTE"]
individuals = []
families = []
tag = None
# Individual properties
individual_Id = None
name = None
gender = None
birthday = None
age = None
death = None
spouse = None
child = None
# Family properties
family_Id = None
married = None
divorced = None
husband_Id = None
husband_name = None
wife_Id = None
wife_name = None
children = []
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
        # Checks if end of file to add last individual and family
        if tag == "TRLR":
            if death is not None:
                alive = False
                age = calculate_age(birthday, death)
            else:
                alive = True
                age = calculate_age(birthday)
            # Saves an individual to the individuals list
            individuals.append(individual(individual_Id, name, gender, birthday, age, alive, death, child, spouse))
            # Check if all parameters to create a family are present
            if all(y is not None for y in (family_Id, married, husband_Id, wife_Id)):
                if divorced is None:
                    divorced = "NA"
                husband_name = find_name_for_id(husband_Id)
                wife_name = find_name_for_id(wife_Id)
                # Saves an family to the families list
                families.append(
                    family(family_Id, married, divorced, husband_Id, husband_name, wife_Id, wife_name, children))
        elif level == "0" and tag == "INDI":
            # Check if all parameters to create an individual are present
            if all(x is not None for x in (individual_Id, name, gender, birthday)):
                if death is not None:
                    alive = False
                    age = calculate_age(birthday, death)
                else:
                    alive = True
                    age = calculate_age(birthday)
                # Saves an individual to the individuals list
                individuals.append(individual(individual_Id, name, gender, birthday, age, alive, death, child, spouse))
            # Reset Data
            individual_Id = None
            name = None
            gender = None
            birthday = None
            age = None
            death = None
            spouse = None
            child = None
        elif level == "0" and tag == "FAM":
            # Check if all parameters to create a family are present
            if all(y is not None for y in (family_Id, married, husband_Id, wife_Id)):
                if divorced is None:
                    divorced = "NA"
                husband_name = find_name_for_id(husband_Id)
                wife_name = find_name_for_id(wife_Id)
                # Saves an family to the families list
                families.append(
                    family(family_Id, married, divorced, husband_Id, husband_name, wife_Id, wife_name, children))
            # Reset Data
            family_Id = None
            married = None
            divorced = None
            husband_Id = None
            husband_name = None
            wife_Id = None
            wife_name = None
            children = []
        if tag == "INDI":
            individual_Id = " ".join(components)
        elif tag == "NAME":
            name = " ".join(components)
        elif tag == "SEX":
            gender = " ".join(components)
        elif prev_tag == "BIRT" and tag == "DATE":
            birthday = " ".join(components)
        elif prev_tag == "DEAT" and tag == "DATE":
            death = " ".join(components)
        elif tag == "FAMS":
            spouse = " ".join(components)
        elif tag == "FAMC":
            child = " ".join(components)
        elif tag == "FAM":
            family_Id = " ".join(components)
        elif tag == "HUSB":
            husband_Id = " ".join(components)
        elif tag == "WIFE":
            wife_Id = " ".join(components)
        elif tag == "CHIL":
            children.append("'%s'" % (" ".join(components)))
        elif prev_tag == "MARR" and tag == "DATE":
            married = " ".join(components)
        elif prev_tag == "DIV" and tag == "DATE":
            divorced = " ".join(components)
    else:
        is_valid = 'N'
    if len(components) != 0:
        print("<-- " + level + "|" + tag + "|" + is_valid + "|" + " ".join(components))
    else:
        print("<-- " + level + "|" + tag + "|" + is_valid)

file_to_read.close()
# Individuals Table
individuals_table = PrettyTable()
individuals_table.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
for indiv in individuals:
    if indiv.child is None and indiv.spouse is None:
        individuals_table.add_row(
            [indiv.id, indiv.name, indiv.gender, indiv.birthday, indiv.age, indiv.alive, indiv.death, "NA", "NA"])
    elif indiv.child is None:
        individuals_table.add_row(
            [indiv.id, indiv.name, indiv.gender, indiv.birthday, indiv.age, indiv.alive, indiv.death, "NA",
             "{'%s'}" % indiv.spouse])
    elif indiv.spouse is None:
        individuals_table.add_row(
            [indiv.id, indiv.name, indiv.gender, indiv.birthday, indiv.age, indiv.alive, indiv.death,
             "{'%s'}" % indiv.child, "NA"])
    else:
        individuals_table.add_row(
            [indiv.id, indiv.name, indiv.gender, indiv.birthday, indiv.age, indiv.alive, indiv.death,
             "{'%s'}" % indiv.child, "{'%s'}" % indiv.spouse])
print()
print('Individuals')
print(individuals_table)

# Families Table
families_table = PrettyTable()
families_table.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name",
                              "Children"]

print()
print('Families')
for fam in families:
    US04(fam)
    US05(fam, individuals)
    US06(fam, individuals)
    US08(fam, individuals)
    families_table.add_row(
        [fam.id, fam.married, fam.divorced, fam.husband_Id, fam.husband_name, fam.wife_Id,
         fam.wife_name, "{%s}" % ",".join(fam.children)])
print(families_table)



