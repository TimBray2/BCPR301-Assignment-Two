# Written by Tim Bray
import csv


class FileEntry:
    def __init__(self):
        self.__results = []

    def get_input(self, directory):
        with open(directory, newline='') as input_file:
            for row in csv.reader(input_file):
                self.__results.append(row)

    def get_data(self):
        return self.__results

entry = FileEntry()
