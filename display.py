# Written By Tim Bray
from abc import abstractmethod, ABCMeta
import graph_maker


class Display:
    def __init__(self, db):
        self.__db = db
        self.__loaded_input = ""
        self.__stored_data = ""
        self.__database_flag = ""

    def display_data(self, format, loaded_input, stored_data, database_flag):
        self.__loaded_input = loaded_input
        self.__stored_data = stored_data
        self.__database_flag = database_flag
        if format == "database":
            if not self.__database_flag:
                self.__db.create_database()
                self.__database_flag = True
        try:
            calculator = self.create_display_builder(format)
            return calculator.display_data()
        except KeyError:
            print("Please select to display the data that is 'unchecked', 'stored', 'graph' or 'database'")

    def create_display_builder(self, display_type):
        calculators = {"unchecked": DisplayUncheckedData(),
                       "stored": DisplayStoredData(),
                       "graph": DisplayGraphData(),
                       "database": DisplayDatabaseData()}
        return calculators[display_type]

    def get_database_flag(self):
        return self.__database_flag


class DisplayData(object, metaclass=ABCMeta):
    @abstractmethod
    def display_data(self):
        pass


class DisplayUncheckedData(DisplayData):

    def display_data(self):
        pass


class DisplayStoredData(DisplayData):

    def display_data(self):
        pass


class DisplayGraphData(DisplayData):

    def display_data(self):
        pass


class DisplayDatabaseData(DisplayData):

    def display_data(self):
        pass
