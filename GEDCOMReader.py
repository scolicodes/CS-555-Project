import re
from datetime import datetime, date
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
    return datetime.strptime(string, "%d %b %Y")


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


# Families Table
families_table = PrettyTable()
families_table.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name",
                              "Children"]

for fam in families:
    US04(fam)
    US05(fam, individuals)
    US06(fam, individuals)
    US08(fam, individuals)
    check_born_before_married(fam)
    check_male_members_last_name(fam)
    US12(fam, None)

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



