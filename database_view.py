# Written By Tim Bray
import sqlite3
import validate
import re


class Database:
    def __init__(self):
        self.__rows = []
        self.__con = ""
        self.__conn = ""
        self.__validate = validate.CheckInput()

    def _connect(self):
        self.__conn = sqlite3.connect('employeeDb')
        print("Opened database successfully")
        return self.__conn

    def create_database(self):
        self.__con = self._connect()
        c = self.__con.cursor()
        c.execute('''DROP TABLE IF EXISTS employeeDb.Employee''')
        c.execute('''CREATE TABLE IF NOT EXISTS Employee(
            EMPID    	VarChar(4) primary key,
            Gender	 	VarChar(1),
            Age      	int(2),
            Sales 		int(3),
            BMI         VarChar(11),
            Salary      int(3),
            Birthday    date);''')
        c.execute('''INSERT INTO Employee VALUES ('T123', 'M',
        20, 654, 'Normal', 56, '1996-10-18');''')
        c.execute('''INSERT INTO Employee VALUES ('G834', 'M',
        54, 213, 'Overweight', 566, '1990/12/4');''')
        c.execute('''INSERT INTO Employee VALUES ('S931', 'F',
        16, 986, 'Obesity', 852, '2001-5-1');''')
        c.execute('''INSERT INTO Employee VALUES ('P912', 'M',
        18, 483, 'Underweight', 135, '1998-7-26');''')
        c.execute('''INSERT INTO Employee VALUES ('B720', 'F',
        24, 867, 'Normal', 741, '1993-1-6');''')

    def load_database(self):
        c = self.__con.cursor()
        c.execute("SELECT * FROM Employee")
        self.__rows = c.fetchall()
        return self.__rows

    def insert_into_database(self, input_list):
        c = self.__con.cursor()
        for row in input_list:
            try:
                split_data = re.split("-", str(row[6]))
                if len(split_data) < 2:
                    split_data = re.split("/", str(row[6]))
                split_data = "-".join(self.__validate.rearrange(split_data))
                c.execute("INSERT INTO Employee VALUES ('" + str(row[0]) +
                          "', '" + str(row[1]) + "', " + str(
                    row[2]) + ", " + str(row[3]) + ", '" + str(row[4]) +
                          "', " + str(row[5]) + ", '" + split_data + "');")
            except sqlite3.IntegrityError:
                print("Entry is already inside database, "
                      "this row will not be inserted into the database.")
