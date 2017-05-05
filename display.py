# Written By Tim Bray
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
                print("Please validate and saved data before "
                      "creating a graph.")
        elif format == "database":
            if not self.__database_flag:
                self.__db.create_database()
                self.__database_flag = True
            for item in self.__db.load_database():
                print(item)
            print("Contents of database have been displayed.")
        else:
            print("Please select to display the data that is "
                  "'unchecked', 'stored', 'graph' or 'database'")

    def get_database_flag(self):
        return self.__database_flag

