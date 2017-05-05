# Written By Tim Bray
import datetime
import re


class CheckInput:
    def __init__(self):
        self.__age_check = True
        self.__regex_checklist = [
            "[A-Z][0-9]{3}", "(M|F)", "[0-9]{2}", "[0-9]{3}", "(Normal|Overweight|Obesity|Underweight)",
            "[0-9]{2,3}"]
        self.__check = bool
        self.__washed_data = []
        self.__row_check = True
        self.__user_ids = []

    @staticmethod
    def __check_date_validity(split_data):
        try:
            datetime.datetime(split_data[2], split_data[1], split_data[0])
            today = datetime.date.today()
            if split_data[2] > int(today.year):
                is_valid = False
            else:
                is_valid = True
        except ValueError:
            is_valid = False
        except IndexError:
            is_valid = False
        return is_valid

    @staticmethod
    def __split_item(split_value, item):
        new_item = re.split(split_value, item)
        return new_item

    @staticmethod
    def __compare_age_to_year(age, dob):
        today = datetime.date.today()
        birthday = today.year - int(dob[2]) - ((today.month, today.day) < (int(dob[1]), int(dob[0])))
        if int(birthday) == int(age):
            return True
        else:
            return False

    @staticmethod
    def __check_regex(regex, value):
        if re.search(regex, value):
            return True
        else:
            return False

    @staticmethod
    def rearrange(split_data):
        return [split_data[2], split_data[1], split_data[0]]

    def check_data(self, data, location):
        self.__washed_data = [True]
        for row in data:
            if len(row) == 7:
                self.__age_check = True
                count = 0
                self.__row_check = True
                if row[0] not in self.__user_ids:
                    self.__user_ids.append(row[0])
                else:
                    self.__row_check = False
                    print(str(row[0]) + " is already entered in the database")
                    print("Row: " + str(row) + " has invalid data."
                                               "\nThis row will not be stored due to business policies\n")
                for item in row:
                    if self.__row_check:
                        if count == 6:
                            split_data = self.__split_item("-", item)
                            if len(split_data) < 2:
                                split_data = self.__split_item("/", item)
                                if len(split_data) < 2:
                                    self.__check = False
                            else:
                                try:
                                    split_data = list(map(int, split_data))
                                except ValueError:
                                    self.__check = False
                                if location == "database":
                                    split_data = self.rearrange(split_data)
                                if self.__check_date_validity(split_data):
                                    self.__age_check = self.__compare_age_to_year(row[2], split_data)
                                else:
                                    self.__age_check = False
                        else:
                            self.__check = self.__check_regex(self.__regex_checklist[count], str(item))
                        if not self.__age_check:
                            print("The date of birth and age do not match up")
                            print("Row: " + str(row) + " has invalid data."
                                                       "\nThis row will not be stored due to business policies\n")
                            self.__row_check = False
                        elif not self.__check :
                            print(str(item) + " is invalid")
                            print("Row: " + str(row) + " has invalid data."
                                                       "\nThis row will not be stored due to business policies\n")
                            self.__row_check = False
                    count += 1
                if self.__row_check:
                    self.__washed_data.append(row)
            else:
                print("Row: " + str(row) + " does not have the correct number of fields filled out."
                                           "\nThis row will not be stored due to business policies\n")
        return self.__washed_data
