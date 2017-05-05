import datetime

age = 20
dob = "1996"

today = datetime.date.today()
birthday = today.year - int(dob[2]) - ((today.month, today.day) < (int(dob[1]), int(dob[0])))
if int(birthday) == int(age):
    print()
else:
    print()

