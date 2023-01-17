# Student Input Project by Hamza Saeed
from datetime import datetime

# Opening Files
student_major_file = 'StudentsMajorsList.csv'
gpa_file = 'GPAList.csv'
graduation_file = 'GraduationDatesList.csv'
main_dict = {}
today = datetime.today()
date_format = "%m/%d/%Y"

# Making a Dictionary to place al files in
with open(student_major_file) as majorfile:
    list1 = majorfile.read().splitlines()
    for x in list1:
        y = x.split(',')
        if y[-1] == 'Y':
            main_dict[y[0]] = {'ID': y[0], 'Last Name': y[1], 'First Name': y[2], 'Major': y[3], 'Disp': y[4]}
        else:
            main_dict[y[0]] = {'ID': y[0], 'Last Name': y[1], 'First Name': y[2], 'Major': y[3]}


# Adding graduation date to main dictionary
with open(graduation_file) as gradfile:
    list2 = gradfile.read().splitlines()
    for x in list2:
        y = x.split(',')
        for key in main_dict:
            if y[0] == key:
                main_dict[key]['Graduation Date'] = y[1]

# Adding GPA to main dictionary
with open(gpa_file) as gpafile:
    list3 = gpafile.read().splitlines()
    for x in list3:
        y = x.split(',')
        for key in main_dict:
            if y[0] == key:
                main_dict[key]['GPA'] = y[1]


# Making new dictionaries for sorting as needed
def func1(item):
    return item[1]['Last Name']


def func2(item):
    return item[1]['ID']


def func3(item):
    return item[1]['GPA']


def func4(item):
    return item[1]['Graduation Date']


full_roster = sorted(main_dict.items(), key=func1)
major_sort = sorted(main_dict.items(), key=func2)
scholarship_sort = sorted(main_dict.items(), reverse=True, key=func3)
disciplined_sort = sorted(main_dict.items(), key=func4)

# Outputting into a FullRoster file
rosterlist = open('FullRoster.csv', 'w')
for id, info in full_roster:
    try:
        rosterlist.write('%s,%s,%s,%s,%s,%s,%s\n' % (info['ID'], info['Major'], info['First Name'], info['Last Name'],
                                                     info['GPA'], info['Graduation Date'], info['Disp']))
    except KeyError:
        rosterlist.write('%s,%s,%s,%s,%s,%s\n' % (info['ID'], info['Major'], info['First Name'], info['Last Name'],
                                                  info['GPA'], info['Graduation Date']))
rosterlist.close()

# Outputting into a scholarship file
scholar_list = open('ScholarshipCandidates.csv', 'w')
for id, info in scholarship_sort:
    if info.get('Disp', 'N/A') == 'N/A':
        if float(info['GPA']) > 3.8 and datetime.strptime(info['Graduation Date'], date_format) > today:
            scholar_list.write('%s,%s,%s,%s,%s\n' % (info['ID'], info['Last Name'], info['First Name'],
                                                     info['Major'], info['GPA']))
    else:
        pass
scholar_list.close()

# Outputting into a disciplined file
disc_list = open('DisciplinedStudents.csv', 'w')
for id, info in disciplined_sort:
    try:
        x = info['Disp']
        disc_list.write('%s,%s,%s,%s\n' % (info['ID'], info['Last Name'], info['First Name'], info['Graduation Date']))
    except KeyError:
        pass
disc_list.close()

# List per Major
for id, info in major_sort:
    majorsplit = info["Major"].replace(" ", "")
    majorlist = open(majorsplit + 'Students.csv', 'a+')
    try:
        majorlist.writelines('%s,%s,%s,%s,%s\n' % (info['ID'], info['Last Name'], info['First Name'],
                                                   info['Graduation Date'], info['Disp']))
        majorlist.close()
    except KeyError:
        majorlist.writelines('%s,%s,%s,%s\n' % (info['ID'], info['Last Name'], info['First Name'],
                                                info['Graduation Date']))
        majorlist.close()
