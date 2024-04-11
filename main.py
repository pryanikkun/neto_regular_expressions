import csv
import re

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


def correct_fields_full_name():
    """ Расстановка ФИО по полям """
    full_name = contact[0].split(' ')
    if len(full_name) == 3:
        full_name = contact[0].split(' ')
        contact[0] = full_name[0]
        contact[1] = full_name[1]
        contact[2] = full_name[2]

    if len(full_name) == 2:
        full_name = contact[0].split(' ')
        contact[0] = full_name[0]
        contact[1] = full_name[1]

    full_name = contact[1].split(' ')
    if len(full_name) == 2:
        contact[1] = full_name[0]
        contact[2] = full_name[1]


def make_right_number():
    """ Приведение телефонов в нужный формат """
    pattern = r"(\+7|8)\s*[\(]*(\d{3})[\)-]* " \
              r"*(\d{3})-*(\d{2})-*(\d{2})([\( ]*[доб. ]+(\d{4})[\) ]*)"
    if re.fullmatch(pattern, contact[5]):
        pattern_to_make = r"+7(\2)\3-\4-\5 доб.\7"
        result = re.sub(pattern, pattern_to_make, contact[5])
    else:
        pattern = r"(\+7|8)\s*[\(]*(\d{3})[\)-]* *(\d{3})-*(\d{2})-*(\d{2})"
        pattern_to_make = r"+7(\2)\3-\4-\5"
        result = re.sub(pattern, pattern_to_make, contact[5])
    contact[5] = result


def add_to_contacts_dict():
    """ Добавление контакта в словарь (группировка по ФИО) """
    full_name = f"{contact[0]} {contact[1]}"
    if full_name not in contacts_dict.keys():
        contacts_dict[full_name] = {
            'lastname': contact[0],
            'firstname': contact[1],
            'surname': contact[2],
            'organization': contact[3],
            'position': contact[4],
            'phone': contact[5],
            'email': contact[6]
        }
    else:
        if contact[3]:
            contacts_dict[full_name]['organization'] = contact[3]
        if contact[4]:
            contacts_dict[full_name]['position'] = contact[4]
        if contact[5]:
            contacts_dict[full_name]['phone'] = contact[5]
        if contact[6]:
            contacts_dict[full_name]['email'] = contact[6]


def add_to_new_contact_list():
    """ Добавление контактов из словаря в новый список """
    for c in contacts_dict.values():
        new_contact_list.append([
            c['lastname'], c['firstname'],
            c['surname'], c['organization'],
            c['position'], c['phone'], c['email']
        ])


contacts_dict = {}
new_contact_list = [contacts_list[0]]
for contact in contacts_list[1:]:
    correct_fields_full_name()
    make_right_number()
    add_to_contacts_dict()

add_to_new_contact_list()

# запись обработанных данных в новый файл
with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(new_contact_list)
