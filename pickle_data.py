# Written By Tim Bray
import pickle


class PickleData:

    def __init__(self):
        self.__stored_data = ""
        self.__loaded_input = ""

    def pickle(self, line, loaded_input, stored_data):
        self.__loaded_input = loaded_input
        self.__stored_data = stored_data
        try:
            choice = line.split(" ")
            if choice[0] == "export":
                if self.__stored_data != "Data has not been stored yet":
                    self.pickle_export(self.__stored_data, choice[1])
                    print("The stored data has been pickled")
                else:
                    print("Please load, validate and save data "
                          "before exporting it.")
            elif choice[0] != "export":
                if choice[0] == "load":
                    self.__loaded_input = self.pickle_load(choice[1])
                    for item in self.__loaded_input:
                        print(item)
                    print("Loaded from pickle file")
                else:
                    print("Please follow pickle with "
                          "'export (file_name)' or 'load (file_name)'")
        except IndexError:
            print("Please follow pickle with "
                  "'export (file_name)' or 'load (file_name)'")
        except FileNotFoundError:
            print("Please follow pickle with "
                  "'export (file_name)' or 'load (file_name)'")

    @staticmethod
    def pickle_export(stored_data, file_name):
        with open(file_name + '.pickle', 'wb') as file:
            pickle.dump(stored_data, file)

    @staticmethod
    def pickle_load(location):
        with open(location + '.pickle', 'rb') as file:
            output = pickle.load(file)
        return output

    def get_loaded_input(self):
        return self.__loaded_input
