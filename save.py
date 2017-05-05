# Written By Tim Bray
class Save:

    def __init__(self, db):
        self.__db = db
        self.__washed_input = ""
        self.__database_flag = False
        self.__stored_data = "Data has not been stored yet"

    def save_data(self, line, washed_input, database_flag, stored_data):
        self.__washed_input = washed_input
        self.__database_flag = database_flag
        self.__stored_data = stored_data

        if len(line) == 0:
            if not self.__washed_input:
                print("No data has been loaded and validated."
                      "\nPlease load and validate data before saving")
            elif self.__washed_input[0]:
                print("The following data has been saved")
                if isinstance(self.__stored_data, str):
                    self.__stored_data = []
                    for row in range(1, len(self.__washed_input)):
                        self.__stored_data.append(self.__washed_input[row])
        elif line == "database":
            if not self.__washed_input:
                print("No data has been loaded and validated."
                      "\nPlease load and validate data before saving")
            elif self.__washed_input[0]:
                if not self.__database_flag:
                    self.__db.create_database()
                    self.__database_flag = True
                if isinstance(self.__stored_data, str):
                    self.__stored_data = []
                    for row in range(1, len(self.__washed_input)):
                        self.__stored_data.append(self.__washed_input[row])
                self.__db.insert_into_database(self.__stored_data)
                print("Saved to database")
        else:
            print("Please follow save with 'database' or nothing at all")

    def get_stored_data(self):
        return self.__stored_data

    def get_database_flag(self):
        return self.__database_flag
