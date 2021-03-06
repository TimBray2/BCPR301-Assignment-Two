# Written By Tim Bray
from abc import abstractmethod, ABCMeta
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
            calculators = {"database": LoadDatabase(
                self.__database_flag, self.__db, self.__file_entry),
                           "file": LoadFile(
                               self.__location, self.__file_entry)}
            try:
                return calculators[display_type]
            except KeyError:
                print("Please select to load from 'database' "
                      "or 'file [location]'")

    def get_loaded_input(self):
        return self.__loaded_input

    def get_database_flag(self):
        return self.__database_flag

    def get_load_location(self):
        return self.__load_location


class LoadData(object, metaclass=ABCMeta):

    @abstractmethod
    def load_data(self):
        pass


class LoadDatabase(LoadData):
    def __init__(self, database_flag, db, file_entry):
        self.__database_flag = database_flag
        self.__db = db
        self.__file_entry = file_entry
        self.__loaded_input = None

    def load_data(self):
        self.__load_location = "database"
        self.__loaded_input = self.__db.load_database()
        print("Loaded from database")

    def get_loaded_input(self):
        return self.__loaded_input

    def get_load_location(self):
        return self.__load_location


class LoadFile(LoadData):
    def __init__(self, location, file_entry):
        self.__location = location
        self.__file_entry = file_entry
        self.__loaded_input = None

    def load_data(self):
        try:
            self.__load_location = "file"
            self.__file_entry.get_input(self.__location[1])
            self.__loaded_input = self.__file_entry.get_data()
            print("Loaded from file")
        except IndexError:
            print("Please select to load from 'database' or 'file [location]'")
        except FileNotFoundError:
            print("Please select a valid file location")

    def get_loaded_input(self):
        return self.__loaded_input

    def get_load_location(self):
        return self.__load_location
