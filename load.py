# Written By Tim Bray
from database_view import Database
from file_entry_view import FileEntry


class Load:

    def __init__(self):
        self.__location = ""
        self.__database_flag = False
        self.__db = Database()
        self.__file_entry = FileEntry()
        self.__loaded_input = None
        self.__load_location = ""

    def load_data(self, location, database_flag):
        self.__location = location.split(" ")
        self.__database_flag = database_flag
        if self.__location[0] == "database":
            if not self.__database_flag:
                self.__db.create_database()
                self.__database_flag = True
        calculator = self.create_load_builder(self.__location[0])
        try:
            calculator.load_data()
            self.__loaded_input = calculator.get_loaded_input()
            self.__load_location = calculator.get_load_location()
        except AttributeError:
            pass

    def create_load_builder(self, display_type):
            pass

    def get_loaded_input(self):
        return self.__loaded_input

    def get_database_flag(self):
        return self.__database_flag

    def get_load_location(self):
        return self.__load_location
