from pprint import pprint
import csv
import re
from itertools import groupby

def parse_phonebook():
    result = []
    with open("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)  
    temp_list = [contacts_list[0]]
    for item in contacts_list[1:]:
        temp = ' '.join(item[:3]).replace('  ', ' ').strip()
        temp_item = list(temp.split(' '))
        temp_item.append('')
        temp_item = temp_item[:3]
        temp_item.extend(item[3:5])

        phone = item[5]
        pattern = '^\+?[7-8]\s*\(*(\d{3})\)*-*\s*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})'
        res = re.sub(pattern, '+7(' + r'\1' + ')' + r'\2' + '-' + r'\3' + '-' + r'\4', phone)
        pattern2 = '(\()?(доб\.\s)(\d{4})(\)*)'
        res2 = re.sub(pattern2, 'доб.' + r'\3', res)

        temp_item.append(res2)
        temp_item.append(item[-1])
        temp_list.append(temp_item)
    
    sort_temp = sorted(temp_list, reverse=False, key=lambda x: x[0])
    for i, j in groupby(sort_temp, key=lambda x:(x[0], x[1])):
        res_group = list(j)
        if len(res_group) > 1:
            merger = []
            for (idx, elem) in enumerate(res_group[0]):
                merger.append(elem) if elem else merger.append(res_group[1][idx])
            result.append(merger)
        else:
            result.append(res_group[0])

    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(result)


if __name__ == '__main__':
    print('start main')
    parse_phonebook()