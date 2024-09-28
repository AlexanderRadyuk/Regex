import csv
import re

with open('phonebook_raw.csv', encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=',')
    contact_list = list(rows)

email_pattern = r'[A-Za-z\._\d]+@[A-Za-z\._\d]+\.[a-z]+'
phone_pattern = r'[\+]*([78])*[\s-]*[\(]*(\d{3})[\)]*[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})[\s-]*[\(]*([доб\.]*\s*\d*)[\)]*'
org_pattern = r'(\b[А-ЯЁа-яё]+\b)'
phone_subst = r'+7 (\2) \3-\4-\5 \6'

pers_dict = {}
pers_data = {}
headers = contact_list.pop(0)
# print(headers)
for entry in contact_list:

    clear_entry_string = ' '.join([word for word in entry if word != ''])

    email = re.findall(email_pattern, clear_entry_string)[0] if\
        len(re.findall(email_pattern, clear_entry_string)) > 0 else 'No email'

    phone_coord = re.search(phone_pattern, clear_entry_string).span()\
        if re.search(phone_pattern, clear_entry_string) is not None else 'No phone'

    if phone_coord != 'No phone':
        phone = re.sub(phone_pattern, phone_subst, clear_entry_string[phone_coord[0]:phone_coord[1]])
    else:
        phone = 'No phone'

    clear_entry_list = ' '.join([word for word in entry if word != '']).split(' ')

    lastname = clear_entry_list[0].strip()
    firstname = clear_entry_list[1].strip()
    patronymic = clear_entry_list[2].strip() if clear_entry_list[2] not in email else 'N/A'
    organization = re.findall(org_pattern, clear_entry_string)[3]\
        if len(re.findall(org_pattern, clear_entry_string)) >= 4 else 'No org'

    if f'{lastname} {firstname}' not in pers_dict.keys():
        pers_dict[f'{lastname} {firstname}'] = [patronymic, organization, phone.strip(), email]
    else:
        if patronymic != 'N/A':
            pers_dict[f'{lastname} {firstname}'].pop(0)
            pers_dict[f'{lastname} {firstname}'].insert(0, patronymic)
        if organization != 'No org':
            pers_dict[f'{lastname} {firstname}'].pop(1)
            pers_dict[f'{lastname} {firstname}'].insert(1, organization)
        if phone != 'No phone':
            pers_dict[f'{lastname} {firstname}'].pop(2)
            pers_dict[f'{lastname} {firstname}'].insert(2, phone)
        if email != 'No email':
            pers_dict[f'{lastname} {firstname}'].pop(3)
            pers_dict[f'{lastname} {firstname}'].insert(3, email)




arranged_contacts = []
counter = 0
for item in pers_dict.keys():
    arranged_contacts.append(item.split(' ')[:])
    # print(arranged_contacts)
    for record in pers_dict[item]:
        arranged_contacts[counter].append(record)
    counter += 1

with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(arranged_contacts)
