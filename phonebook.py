import re
import pandas as pd

import csv
with open("phonebook_raw.csv") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

pattern_fio_job = "\[.([а-яА-ЯёЁ]+)\W*([а-яА-ЯёЁ]+)\W*([а-яА-ЯёЁ]+)?\W*([а-яА-ЯёЁ]+)?\W*([а-яА-ЯёЁa-zA-Z –]+)?'"
pattern_phone = "((8|\+7)[\- ]?)?(\(?(\d{3})\)?[\- ]?)?(\(?(\d{3})\)?[\- ]?)?(\(?(\d{2})\)?[\- ]?)?(\(?(\d{2})\)?[\- ]?)(\()?(доб.)? ?(\d{4})?"
pattern_email = "[\w\d.]+[\w\d]+@\w+.ru|com"

people = []

for i in contacts_list[1:]:

    compiled = re.compile(pattern_fio_job)
    fio_jobs = compiled.findall(str(i))
    lastname = fio_jobs[0][0]
    firstname = fio_jobs[0][1]
    patronym = fio_jobs[0][2]
    company = fio_jobs[0][3]
    position = fio_jobs[0][4]
    # print(f'{lastname} {firstname} {patronym}\n{company}\n{position}')

    phone_compiled = re.compile(pattern_phone)
    find_phone = phone_compiled.search(str(i))
    if find_phone is not None:
        all_phones = find_phone.group(0)
        if "доб." in all_phones:
            phone = re.sub(pattern_phone, r"+7(\4)\6-\8-\10 доб.\13", all_phones)
        else:
            phone = re.sub(pattern_phone, r"+7(\4)\6-\8-\10", all_phones)

    find_email = re.search(pattern_email, str(i))
    if find_email is not None:
        email = find_email.group(0)

    person = [lastname, firstname, patronym, company, position, phone, email]
    people.append(person)

cols = ['lastname', 'firstname', 'patronym', 'company', 'position', 'phone', 'email']

frame = pd.DataFrame(people, columns=cols)
frame = frame.groupby('lastname').agg({'firstname': 'first', 'patronym': 'first', 'company': 'first',
                                       'position': 'first', 'phone': 'first', 'email': 'first'}).reset_index()
frame.to_csv('phonebook.csv', index=False)

''' не понимаю, почему в некоторых случаях дублируются телефоны и емейлы у разных людей
то есть:
- Мартиняхин без должности
- Лагунцов не с тем емейлом
- Наркаев с емейлом, которого у него не было
при этом у других всё нормально
это в groupby проблема? что-то другое нужно вписать в .agg? что? 
подскажите, пожалуйста - очень много гуглила и не нагуглила'''
