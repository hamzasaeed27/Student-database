# Student Query Project by Hamza Saeed
from datetime import datetime

# This is assigning all .csv files into variables
student_major_file = 'StudentsMajorsList.csv'
gpa_file = 'GPAList.csv'
graduation_file = 'GraduationDatesList.csv'
main_dict = {}
today = datetime.today()
date_format = "%m/%d/%Y"

# Making a Dictionary to place all files in. This makes sure that if the line has a disciplined student, they
# get a 'Y' as an extra dictionary. This is also assigning all major into a list to check if user input has
# more than one major.
majorlist = []
with open(student_major_file) as majorfile:
    list1 = majorfile.read().splitlines()
    for x in list1:
        y = x.split(',')
        if y[-1] == 'Y':
            main_dict[y[0]] = {'ID': y[0], 'Last Name': y[1], 'First Name': y[2], 'Major': y[3], 'Disp': y[4]}
        else:
            main_dict[y[0]] = {'ID': y[0], 'Last Name': y[1], 'First Name': y[2], 'Major': y[3]}
        if y[3] in majorlist:
            pass
        else:
            majorlist.append(y[3])

# Adding graduation date to main dictionary
with open(graduation_file) as gradfile:
    list2 = gradfile.read().splitlines()
    for x in list2:
        y = x.split(',')
        for key in main_dict:
            if y[0] == key:
                main_dict[key]['Graduation Date'] = y[1]

# Adding GPA to main dictionary. This is also assigning all GPA into a list to check if user input has more than
# one GPA.
gpalist = []
with open(gpa_file) as gpafile:
    list3 = gpafile.read().splitlines()
    for x in list3:
        y = x.split(',')
        for key in main_dict:
            if y[0] == key:
                main_dict[key]['GPA'] = y[1]
                gpalist.append(y[1])
gpa_list = [float(x) for x in gpalist]


# This is a function that check the closest number in a list to the user's GPA, in case none of the results show up
# within 0.1 or 0.25 of the user's value. I use a list in case there are 2 GPAs that fall within the closest range
# For example, if the user's input is 3.5, and the 2 closest GPAs are 3 and 4.
def nearest_value(values, number):
    distance_list = {}
    for v in values:
        dist = abs(v - number)
        if dist not in distance_list:
            distance_list[dist] = [v]
        elif v not in distance_list[dist]:
            distance_list[dist].append(v)
    if distance_list:

        return distance_list[min(distance_list)]
    else:
        return []


# This is asking for the user's input.
user_input = input("Enter major and GPA:\n")

# This is setting the user's major and GPA as empty, and setting the errors as false, so in the case the user's entry
# has more than one major or GPA, it can turn the error as true.
while user_input != 'q':
    user_gpa = ""
    student_major = ""
    error = False
# Here, I used try and except in the case where a word is a string instead of a float. The code accepts the first GPA
# as the user's GPA, and calls the error as true if there's a second GPA in the user's input.
    for token in user_input.split():
        try:
            student_gpa = float(token)
            if user_gpa == "":
                user_gpa = student_gpa
            else:
                error = True
                break
        except ValueError:
            pass

# The code accepts the first major as the user's major, and calls the error as true
# if there's a second major in the user's input.
    for major in majorlist:
        if major in user_input:
            if student_major == "":
                student_major = major
            else:
                error = True
                break

# If the error is true or either the major or GPA is not found, the main error becomes true.
    if error or not student_major or not user_gpa:
        print("No such student")
        user_input = input("Enter major and GPA:\n")
        continue

# Instead of printing, I am using a list so I can make sure that whoever is mentioned in 0.1 range of GPA won't be
# mentioned again within 0.25 range of GPA.
    print_list1 = []
    for d in main_dict.values():
        # Checking if the student has been disciplined
        if d.get('Disp', 'N/A') == 'N/A':
            if d['Major'] in user_input and ((user_gpa - 0.1) <= float(d['GPA']) <= (user_gpa + 0.1)) and \
                    datetime.strptime(d['Graduation Date'], date_format) > today:
                print_list1.append('%s, %s, %s, %s' % (d['ID'], d['First Name'], d['Last Name'], d['GPA']))

# Here, I am printing the heading for the students that fall within 0.1 of user's GPA. The PDF file didn't mention to
# not write this statement if there are no students that fall under here.
    print()
    print("Your student(s):")
    for x in print_list1:
        print(x)

    print_list2 = []
    for d in main_dict.values():
        # Checking if the student has been disciplined
        if d.get('Disp', 'N/A') == 'N/A':
            if d['Major'] in user_input and ((user_gpa - 0.25) <= float(d['GPA']) <= (user_gpa + 0.25)) and \
                        datetime.strptime(d['Graduation Date'], date_format) > today:
                print_list2.append('%s, %s, %s, %s' % (d['ID'], d['First Name'], d['Last Name'], d['GPA']))
    # Here, I am making a different list so those who were mentioned before won't be mentioned again
    print_list3 = [student for student in print_list2 if student not in print_list1]

# Here, I am printing the heading for the students that fall within 0.25 of user's GPA. The PDF file didn't mention to
# not write this statement if there are no students that fall under here.
    print()
    print("You may also consider:")
    for x in print_list3:
        print(x)

# If no students are listed from both sides, the program will search for the closest GPA to the user's GPA (provided
# that student has not been graduated, and that student was not disciplined.
    if not print_list2:
        print()

# This code is to make sure only students with the user requested GPA are checked with the closest GPA function.
        major_gpa_list = []
        for d in main_dict.values():
            if d.get('Disp', 'N/A') == 'N/A':
                if d['Major'] in user_input and datetime.strptime(d['Graduation Date'], date_format) > today:
                    major_gpa_list.append(float(d['GPA']))

        closest_gpas = nearest_value(major_gpa_list, float(user_gpa))

        for closest_gpa in closest_gpas:
            for d in main_dict.values():
                if d['Major'] in user_input and \
                        d.get('Disp', 'N/A') == 'N/A' and datetime.strptime(d['Graduation Date'], date_format) > today:

                    if float(d['GPA']) == closest_gpa:
                        print('%s, %s, %s, %s' % (d['ID'], d['First Name'], d['Last Name'], d['GPA']))

    user_input = input("Enter major and GPA:\n")
