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
        calculators = {"unchecked": DisplayUncheckedData(self.__loaded_input),
                       "stored": DisplayStoredData(self.__stored_data),
                       "graph": DisplayGraphData(self.__stored_data),
                       "database": DisplayDatabaseData(self.__database_flag, self.__db)}
        return calculators[display_type]

    def get_database_flag(self):
        return self.__database_flag


class DisplayData(object, metaclass=ABCMeta):
    @abstractmethod
    def display_data(self):
        pass


class DisplayUncheckedData(DisplayData):
    def __init__(self, loaded_input):
        self.load_input = loaded_input

    def display_data(self):
        for row in self.load_input:
            print(row)
        print("Unchecked data has been displayed")


class DisplayStoredData(DisplayData):
    def __init__(self, stored_data):
        self.stored_data = stored_data

    def display_data(self):
        if not isinstance(self.stored_data, str):
            for row in range(len(self.stored_data)):
                print(self.stored_data[row])
            print("Stored data has been displayed")
        else:
            print(self.stored_data)


class DisplayGraphData(DisplayData):
    def __init__(self, stored_data):
        self.stored_data = stored_data

    def display_data(self):
        if not isinstance(self.stored_data, str):
            graph_maker.create_graph(self.stored_data)
            print("Graph has been created in the browser.")
        else:
            print("Please validate and saved data before creating a graph.")


class DisplayDatabaseData(DisplayData):
    def __init__(self, database_flag, db):
        self.database_flag = database_flag
        self.db = db

    def display_data(self):
        for item in self.db.load_database():
            print(item)
        print("Contents of database have been displayed.")
