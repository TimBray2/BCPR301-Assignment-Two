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
        self.__location = location
        self.__database_flag = database_flag
        try:
            destination = self.__location.split(" ")
            if destination[0] == "file":
                self.__load_location = "file"
                directory = destination[1]
                self.__file_entry.get_input(directory)
                self.__loaded_input = self.__file_entry.get_data()
                print("Loaded from file")
            elif len(destination) == 1 and destination[0] != "file":
                if destination[0] == "database":
                    self.__load_location = "database"
                    if not self.__database_flag:
                        self.__db.create_database()
                        self.__database_flag = True
                    self.__loaded_input = self.__db.load_database()
                    print("Loaded from database")
                else:
                    print("Please select to load from "
                          "'database' or 'file [location]'")
            else:
                print("Please select to load from "
                      "'database' or 'file [location]'")
        except IndexError:
            print("Please select to load from "
                  "'database' or 'file [location]'")
        except FileNotFoundError:
            print("Please select a valid file location")

    def get_loaded_input(self):
        return self.__loaded_input

    def get_database_flag(self):
        return self.__database_flag

    def get_load_location(self):
        return self.__load_location
