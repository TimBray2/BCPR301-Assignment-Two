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
        if format == "unchecked":
            for row in self.__loaded_input:
                print(row)
            print("Unchecked data has been displayed")
        elif format == "stored":
            if not isinstance(self.__stored_data, str):
                for row in range(len(self.__stored_data)):
                    print(self.__stored_data[row])
                print("Stored data has been displayed")
            else:
                print(self.__stored_data)
        elif format == "graph":
            if not isinstance(self.__stored_data, str):
                graph_maker.create_graph(self.__stored_data)
                print("Graph has been created in the browser.")
            else:
                print("Please validate and saved data before creating a graph.")
        elif format == "database":
            if not self.__database_flag:
                self.__db.create_database()
                self.__database_flag = True
            for item in self.__db.load_database():
                print(item)
            print("Contents of database have been displayed.")
        else:
            print("Please select to display the data that is 'unchecked', 'stored', 'graph' or 'database'")

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
