# Written By Tim Bray
import datetime
import cmd_view
import graph_maker
from pickle_data import PickleData
from database_view import Database
from file_entry_view import FileEntry
from validate import CheckInput
from save import Save
from sys import argv
from load import Load
from display import Display


class Controller:
    def __init__(self, view):
        self.__database_flag = False
        self.__temp_input = [False, "No data has been loaded"]
        self.__check_input = CheckInput()
        self.__stored_data = "Data has not been stored yet"
        self.__washed_input = []
        self.__load_location = ""
        self.__file_entry = FileEntry()
        self.__db = Database()
        self.__cmd_view = view
        self.__loaded_input = None
        self.__pickle_data = PickleData()
        self.__save = Save(self.__db)
        self.__load_data = Load()
        self.__display = Display(self.__db)

    def go(self, controller):
        self.__cmd_view.set_controller(controller)
        if len(argv) > 1:
            self.__cmd_view.onecmd(' '.join(argv[1:]))
        self.__cmd_view.cmdloop()

    def pickle(self, line):
        self.__pickle_data.pickle(line, self.__loaded_input,
                                  self.__stored_data)
        self.__loaded_input = self.__pickle_data.get_loaded_input()

    def save(self, line):
        self.__save.save_data(line, self.__washed_input,
                              self.__database_flag, self.__stored_data)
        self.__database_flag = self.__save.get_database_flag()
        self.__stored_data = self.__save.get_stored_data()

    def load(self, location):
        self.__load_data.load_data(location, self.__database_flag)
        self.__database_flag = self.__load_data.get_database_flag()
        self.__loaded_input = self.__load_data.get_loaded_input()
        self.__load_location = self.__load_data.get_load_location()

    def display(self, format):
        self.__display.display_data(format, self.__loaded_input,
                                    self.__stored_data, self.__database_flag)
        self.__database_flag = self.__display.get_database_flag()

    def validate(self, line):
        try:
            if len(line) == 0:
                self.__washed_input = self.__check_input.check_data(self.__loaded_input, self.__load_location)
                print("Entry data is checked")
            else:
                print("Please do not enter any extra input after 'validate'")
        except TypeError:
            print("Please load data before validating")

    @staticmethod
    def welcome(line):
        if len(line) == 0:
            today = datetime.date.today()
            print("Welcome to the program.\nThe date is " + str(today))
        else:
            print("Please do not enter any extra input after 'welcome'")


if __name__ == "__main__":
    control = Controller(cmd_view.CmdView())
    control.go(control)
