# Written by Tim Bray
import datetime
import unittest
import cmd_view
import sys
from unittest.mock import patch
from contextlib import contextmanager
from io import StringIO
from controller import Controller
from validate import CheckInput
from display import DisplayData


class MainTests(unittest.TestCase):
    def setUp(self):
        self.__con = Controller(cmd_view.CmdView())
        self.__today = datetime.date.today()
        self.__validate = CheckInput()
        self.__view = cmd_view.CmdView()
        self.__view.set_controller(self.__con)

    @contextmanager
    def captured_output(self):
        new_out, new_err = StringIO(), StringIO()
        old_out, old_err = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = new_out, new_err
            yield sys.stdout, sys.stderr
        finally:
            sys.stdout, sys.stderr = old_out, old_err

    def test_invalid_data_file(self):
        with self.captured_output() as (out, err):
            self.__view.do_load("file TestFile1.txt")
            self.__view.do_validate("")
        output = out.getvalue().strip()
        expected = "Loaded from file" \
                   "\nThe date of birth and age do not match up" \
                   "\nRow: ['Z131', 'M', '27', '234', 'Normal', '39', " \
                   "'31-01.1992'] has invalid data." \
                   "\nThis row will not be stored due to business policies" \
                   "\n" \
                   "\n25_12_1990 is invalid" \
                   "\nRow: ['Z130', 'M', '27', '234', 'Normal', '39', " \
                   "'25_12_1990'] has invalid data." \
                   "\nThis row will not be stored due to business policies" \
                   "\n" \
                   "\nThe date of birth and age do not match up" \
                   "\nRow: ['Z125', 'F', '27', '234', 'Normal', '39', " \
                   "'25-12'] has invalid data." \
                   "\nThis row will not be stored due to business policies" \
                   "\n" \
                   "\nThe date of birth and age do not match up" \
                   "\nRow: ['Z127', 'F', '27', '234', 'Normal', '39', " \
                   "'25-12-1880'] has invalid data." \
                   "\nThis row will not be stored due to business policies" \
                   "\n" \
                   "\nThe date of birth and age do not match up" \
                   "\nRow: ['Z128', 'F', '27', '234', 'Normal', '39', " \
                   "'25-15-1880'] has invalid data." \
                   "\nThis row will not be stored due to business policies" \
                   "\n" \
                   "\nThe date of birth and age do not match up" \
                   "\nRow: ['Z124', 'F', '27', '234', 'Normal', '39', " \
                   "'25-12-2020'] has invalid data." \
                   "\nThis row will not be stored due to business policies" \
                   "\n" \
                   "\n2 is invalid" \
                   "\nRow: ['I123', 'M', '2', '13', 'OverWeight', '123', " \
                   "'31-12-1989'] has invalid data." \
                   "\nThis row will not be stored due to business policies" \
                   "\n" \
                   "\n123I is invalid" \
                   "\nRow: ['123I', 'm', '90', '40.5', 'Underweight', " \
                   "'000', '15-3-1927'] has invalid data." \
                   "\nThis row will not be stored due to business policies" \
                   "\n" \
                   "\nXXD4 is invalid" \
                   "\nRow: ['XXD4', ' F', '50', '001', '', '002', " \
                   "'29-02-1967'] has invalid data." \
                   "\nThis row will not be stored due to business policies" \
                   "\n" \
                   "\nu258 is invalid" \
                   "\nRow: ['u258', 'F', '50', '999', 'Obesity', '999', " \
                   "'31-02-1967'] has invalid data." \
                   "\nThis row will not be stored due to business policies" \
                   "\n" \
                   "\nX is invalid" \
                   "\nRow: ['Q258', 'X', '50', '999', 'Normal', '.99', " \
                   "'1967-02-01'] has invalid data." \
                   "\nThis row will not be stored due to business policies" \
                   "\n" \
                   "\nRow: ['Q258/F/50/123/Normal/123/01-01-1967'] does " \
                   "not have the correct number of " \
                   "fields filled out." \
                   "\nThis row will not be stored due to business policies" \
                   "\n" \
                   "\nRow: ['Q234  F  50  123  Normal  123  01-01-1967'] " \
                   "does not have the correct number of " \
                   "fields filled out." \
                   "\nThis row will not be stored due to business policies" \
                   "\n" \
                   "\n  is invalid" \
                   "\nRow: [' ', ' ', ' ', ' ', ' ', ' ', ''] " \
                   "has invalid data." \
                   "\nThis row will not be stored due to business policies" \
                   "\n" \
                   "\nEntry data is checked"
        self.assertEqual(expected, output)

    def test_valid_data_file(self):
        with self.captured_output() as (out, err):
            self.__view.do_load("file validInputData.txt")
            self.__view.do_validate("")
        output = out.getvalue().strip()
        expected = "Loaded from file" \
                   "\nEntry data is checked"
        self.assertEqual(expected, output)

    def test_validate_function_input_1(self):
        with self.captured_output() as (out, err):
            self.__view.do_load("file validInputData.txt")
            self.__view.do_validate("file")
        output = out.getvalue().strip()
        expected = "Loaded from file" \
                   "\nPlease do not enter any extra input after 'validate'"
        self.assertEqual(expected, output)

    def test_validate_function_input_2(self):
        with self.captured_output() as (out, err):
            self.__view.do_validate("")
        output = out.getvalue().strip()
        expected = "Please load data before validating"
        self.assertEqual(expected, output)

    def test_validate_checkRearrange_true(self):
        date = [1989, 12, 25]
        actual = self.__validate.rearrange(date)
        expected = [25, 12, 1989]
        self.assertEqual(expected, actual)

    def test_validate_loadDatabase_true(self):
        self.__view.do_load("database")
        with self.captured_output() as (out, err):
            self.__view.do_validate("")
        output = out.getvalue().strip()
        expected = "Entry data is checked"
        self.assertEqual(expected, output)

    def test_save_validInput_1(self):
        with self.captured_output() as (out, err):
            self.__view.do_load("file validInputData.txt")
            self.__view.do_validate("")
            self.__view.do_save("")
        output = out.getvalue().strip()
        expected = "Loaded from file" \
                   "\nEntry data is checked" \
                   "\nThe following data has been saved"
        self.assertEqual(expected, output)

    def test_save_invalidInput_1(self):
        with self.captured_output() as (out, err):
            self.__view.do_load("file validInputData.txt")
            self.__view.do_validate("")
            self.__view.do_save("file")
        output = out.getvalue().strip()
        expected = "Loaded from file" \
                   "\nEntry data is checked" \
                   "\nPlease follow save with 'database' or nothing at all"
        self.assertEqual(expected, output)

    def test_save_invalidInput_5(self):
        with self.captured_output() as (out, err):
            self.__view.do_load("file validInputData.txt")
            self.__view.do_validate("")
            self.__view.do_save("file 123")
        output = out.getvalue().strip()
        expected = "Loaded from file" \
                   "\nEntry data is checked" \
                   "\nPlease follow save with 'database' or nothing at all"
        self.assertEqual(expected, output)

    def test_save_invalidInput_2(self):
        self.__view.do_load("file validInputData.txt")
        with self.captured_output() as (out, err):
            self.__view.do_save("")
        output = out.getvalue().strip()
        expected = "No data has been loaded and validated." \
                   "\nPlease load and validate data before saving"
        self.assertEqual(expected, output)

    def test_save_invalidInput_3(self):
        with self.captured_output() as (out, err):
            self.__view.do_save("database")
        output = out.getvalue().strip()
        expected = "No data has been loaded and validated." \
                   "\nPlease load and validate data before saving"
        self.assertEqual(expected, output)

    def test_save_function_input_4(self):
        self.__view.do_load("file testinput.txt")
        with self.captured_output() as (out, err):
            self.__view.do_save("")
        output = out.getvalue().strip()
        expected = "No data has been loaded and validated." \
                   "\nPlease load and validate data before saving"
        self.assertEqual(expected, output)

    def test_display_function_input_1(self):
        self.__view.do_load("file inputData.txt")
        self.__view.do_validate("")
        self.__view.do_save("")
        with self.captured_output() as (out, err):
            self.__view.do_display("unchecked")
        output = out.getvalue().strip()
        expected = "['T123', 'M', '20', '654', 'Normal', '56', " \
                   "'18-10-1996']" \
                   "\n['G834', 'M', '26', '213', 'Overweight', '566', " \
                   "'4-12-1990']" \
                   "\n['S931', 'F', '16', '986', 'Obesity', '852', " \
                   "'1-5-2001']" \
                   "\n['P12', 'M', '18', '682', 'Underweight', '135', " \
                   "'26-7-1998']" \
                   "\n['P912', 'D', '18', '682', 'Underweight', '135', " \
                   "'26-7-1998']" \
                   "\n['P912', 'M', '78', '682', 'Underweight', '135', " \
                   "'26-7-1998']" \
                   "\n['P912', 'M', '18', '43', 'Underweight', '135', " \
                   "'26-7-1998']" \
                   "\n['P912', 'M', '18', '682', 'Fit', '135', " \
                   "'26-7-1998']" \
                   "\n['B720', 'F', '24', '867', 'Normal', '845864', " \
                   "'6-1-1993']" \
                   "\n['S987', 'F', '30', '867', 'Normal', '741', " \
                   "'6/1/1987']" \
                   "\n['S987', 'F', '30', '867', 'Normal', '741', " \
                   "'6-15-1987']" \
                   "\n['S987', 'F', '30', '867', 'Normal', '741', " \
                   "'90-1-1987']" \
                   "\n['S987', 'F', '30', '867', 'Normal', '741', " \
                   "'6-1-3000']" \
                   "\n['S987', 'F', '30', '867', 'Normal', '741', " \
                   "'6-1-3000', 'sad', '213', '23', 'asd']" \
                   "\nUnchecked data has been displayed"
        self.assertEqual(expected, output)

    def test_saveToDatabase_function(self):
        self.__view.do_load("file testfile1.txt")
        self.__view.do_validate("")
        self.__view.do_save("database")
        with self.captured_output() as (out, err):
            self.__view.do_display("database")
        output = out.getvalue().strip()
        expected = "('T123', 'M', 20, 654, 'Normal', 56, '1996-10-18')" \
                   "\n('G834', 'M', 54, 213, 'Overweight', 566, " \
                   "'1990/12/4')" \
                   "\n('S931', 'F', 16, 986, 'Obesity', 852, '2001-5-1')" \
                   "\n('P912', 'M', 18, 483, 'Underweight', 135, " \
                   "'1998-7-26')" \
                   "\n('B720', 'F', 24, 867, 'Normal', 741, '1993-1-6')" \
                   "\n('Z123', 'M', 25, 123, 'Normal', 39, '1992-01-31')" \
                   "\n('Z132', 'M', 25, 123, 'Normal', 39, '1992-01-31')" \
                   "\n('Z126', 'F', 27, 234, 'Normal', 39, '1989-12-25')" \
                   "\nContents of database have been displayed."
        self.assertEqual(expected, output)

    def test_display_function_input_2(self):
        self.__view.do_load("file inputData.txt")
        self.__view.do_validate("")
        self.__view.do_save("")
        with self.captured_output() as (out, err):
            self.__view.do_display("stored")
        output = out.getvalue().strip()
        expected = "['T123', 'M', '20', '654', 'Normal', '56', " \
                   "'18-10-1996']" \
                   "\n['G834', 'M', '26', '213', 'Overweight', '566', " \
                   "'4-12-1990']" \
                   "\n['S931', 'F', '16', '986', 'Obesity', '852', " \
                   "'1-5-2001']" \
                   "\n['B720', 'F', '24', '867', 'Normal', '845864', " \
                   "'6-1-1993']" \
                   "\n['S987', 'F', '30', '867', 'Normal', '741', " \
                   "'6/1/1987']" \
                   "\nStored data has been displayed"
        self.assertEqual(expected, output)

    def test_display_function_input_3(self):
        self.__view.do_load("file inputData.txt")
        self.__view.do_validate("")
        self.__view.do_save("")
        with self.captured_output() as (out, err):
            self.__view.do_display("imported")
        output = out.getvalue().strip()
        expected = "Please select to display the data that is 'unchecked'," \
                   " 'stored', 'graph' or 'database'"
        self.assertEqual(expected, output)

    def test_display_function_input_4(self):
        self.__view.do_load("file validInputData.txt")
        self.__view.do_validate("")
        self.__view.do_save("")
        with self.captured_output() as (out, err):
            self.__view.do_display("graph")
        output = out.getvalue().strip()
        expected = "Graph has been created in the browser."
        self.assertEqual(expected, output)

    def test_display_function_input_5(self):
        self.__view.do_load("file inputData.txt")
        self.__view.do_validate("")
        self.__view.do_save("")
        with self.captured_output() as (out, err):
            self.__view.do_display("graph pie")
        output = out.getvalue().strip()
        expected = "Please select to display the data that is 'unchecked'," \
                   " 'stored', 'graph' or 'database'"
        self.assertEqual(expected, output)

    def test_display_function_input_6(self):
        self.__view.do_load("file inputData.txt")
        self.__view.do_validate("")
        with self.captured_output() as (out, err):
            self.__view.do_display("stored")
        output = out.getvalue().strip()
        expected = "Data has not been stored yet"
        self.assertEqual(expected, output)

    def test_display_function_input_7(self):
        self.__view.do_load("file inputData.txt")
        self.__view.do_validate("")
        with self.captured_output() as (out, err):
            self.__view.do_display("graph")
        output = out.getvalue().strip()
        expected = "Please validate and saved data before creating a graph."
        self.assertEqual(expected, output)

    def test_display_function_input_8(self):
        with self.captured_output() as (out, err):
            self.__view.do_display("database")
        output = out.getvalue().strip()
        expected = "Opened database successfully" \
                   "\n('T123', 'M', 20, 654, 'Normal', 56, '1996-10-18')" \
                   "\n('G834', 'M', 54, 213, 'Overweight', 566, " \
                   "'1990/12/4')" \
                   "\n('S931', 'F', 16, 986, 'Obesity', 852, '2001-5-1')" \
                   "\n('P912', 'M', 18, 483, 'Underweight', 135, " \
                   "'1998-7-26')" \
                   "\n('B720', 'F', 24, 867, 'Normal', 741, '1993-1-6')" \
                   "\nContents of database have been displayed."
        self.assertEqual(expected, output)

    def test_welcome_function_input_1(self):
        with self.captured_output() as (out, err):
            self.__view.do_welcome("")
        output = out.getvalue().strip()
        expected = "Welcome to the program.\nThe date is " + str(self.__today)
        self.assertEqual(expected, output)

    def test_welcome_function_input_2(self):
        with self.captured_output() as (out, err):
            self.__view.do_welcome("message")
        output = out.getvalue().strip()
        expected = "Please do not enter any extra input after 'welcome'"
        self.assertEqual(expected, output)

    def test_pickle_function_input_1(self):
        self.__view.do_load("file validInputData.txt")
        self.__view.do_validate("")
        self.__view.do_save("")
        with self.captured_output() as (out, err):
            self.__view.do_pickle("export validInputData")
        output = out.getvalue().strip()
        expected = "The stored data has been pickled"
        self.assertEqual(expected, output)

    def test_pickle_function_input_2(self):
        with self.captured_output() as (out, err):
            self.__view.do_pickle("load validInputData")
        output = out.getvalue().strip()
        expected = "['A123', 'M', '25', '123', 'Normal', '39', " \
                   "'31-01-1992']" \
                   "\n['B123', 'M', '27', '234', 'Normal', '39', " \
                   "'25-12-1989']" \
                   "\n['T123', 'M', '20', '654', 'Normal', '56', " \
                   "'18-10-1996']" \
                   "\n['G834', 'M', '26', '213', 'Overweight', '566'," \
                   " '4-12-1990']" \
                   "\n['S931', 'F', '16', '986', 'Obesity', '852'," \
                   " '1-5-2001']" \
                   "\n['P912', 'M', '18', '463', 'Underweight', '135', " \
                   "'26-7-1998']" \
                   "\n['B720', 'F', '24', '867', 'Normal', '741', " \
                   "'6-1-1993']" \
                   "\n['S987', 'F', '30', '867', 'Overweight', '741', " \
                   "'6-1-1987']" \
                   "\nLoaded from pickle file"
        self.assertEqual(expected, output)

    def test_pickle_function_input_3(self):
        self.__view.do_load("file validInputData.txt")
        self.__view.do_validate("")
        with self.captured_output() as (out, err):
            self.__view.do_pickle("export validInputData")
        output = out.getvalue().strip()
        expected = "Please load, validate and save data before exporting it."
        self.assertEqual(expected, output)

    def test_pickle_function_input_4(self):
        self.__view.do_load("file validInputData.txt")
        self.__view.do_validate("")
        with self.captured_output() as (out, err):
            self.__view.do_pickle("pickle")
        output = out.getvalue().strip()
        expected = "Please follow pickle with 'export (file_name)' " \
                   "or 'load (file_name)'"
        self.assertEqual(expected, output)

    def test_pickle_function_input_5(self):
        self.__view.do_load("file validInputData.txt")
        self.__view.do_validate("")
        with self.captured_output() as (out, err):
            self.__view.do_pickle("pickle")
        output = out.getvalue().strip()
        expected = "Please follow pickle with 'export (file_name)' " \
                   "or 'load (file_name)'"
        self.assertEqual(expected, output)

    def test_pickle_function_input_6(self):
        self.__view.do_load("file validInputData.txt")
        self.__view.do_validate("")
        with self.captured_output() as (out, err):
            self.__view.do_pickle("load randomPickleFile")
        output = out.getvalue().strip()
        expected = "Please follow pickle with 'export (file_name)' " \
                   "or 'load (file_name)'"
        self.assertEqual(expected, output)

    def test_pickle_function_input_7(self):
        self.__view.do_load("file validInputData.txt")
        self.__view.do_validate("")
        self.__view.do_save("")
        with self.captured_output() as (out, err):
            self.__view.do_pickle("export")
        output = out.getvalue().strip()
        expected = "Please follow pickle with 'export (file_name)' " \
                   "or 'load (file_name)'"
        self.assertEqual(expected, output)

    def test_load_invalidInput_1(self):
        with self.captured_output() as (out, err):
            self.__view.do_load("excel")
        output = out.getvalue().strip()
        expected = "Please select to load from 'database' or " \
                   "'file [location]'"
        self.assertEqual(expected, output)

    def test_load_invalidInput_2(self):
        with self.captured_output() as (out, err):
            self.__view.do_load("load excel spreadsheet")
        output = out.getvalue().strip()
        expected = "Please select to load from 'database' or " \
                   "'file [location]'"
        self.assertEqual(expected, output)

    def test_load_invalidInput_3(self):
        with self.captured_output() as (out, err):
            self.__view.do_load("file unknownFile")
        output = out.getvalue().strip()
        expected = "Please select a valid file location"
        self.assertEqual(expected, output)

    def test_load_invalidInput_4(self):
        with self.captured_output() as (out, err):
            self.__view.do_load("file")
        output = out.getvalue().strip()
        expected = "Please select to load from 'database' or " \
                   "'file [location]'"
        self.assertEqual(expected, output)

    def runTest(self, given_answer, expected_out):
        with patch('builtins.input', return_value=given_answer), patch(
                'sys.stdout', new=StringIO()) as output:
            sys.argv.append("welcome")
            self.__con.go(self.__con)
            self.assertEqual(expected_out, output.getvalue().strip())

    def test_set_controller(self):
        self.runTest("exit", "Welcome to the program."
                             '\nThe date is ' + str(self.__today) +
                     "\nExiting.....")

    @patch.multiple(DisplayData, __abstractmethods__=set())
    def test_DisplayData_abstractMethod(self):
        self.display_data = DisplayData()
        with self.captured_output() as (out, err):
            self.display_data.display_data()
        output = out.getvalue().strip()
        expected = ""
        self.assertEqual(expected, output)

    def test_viewHelp_save(self):
        with self.captured_output() as (out, err):
            self.__view.help_save()
        output = out.getvalue().strip()
        expected = "save [database]" \
                   '\nSave the imported data. Can be used as "save" ' \
                   'or "save database"'
        self.assertEqual(expected, output)

    def test_viewHelp_pickle(self):
        with self.captured_output() as (out, err):
            self.__view.help_pickle()
        output = out.getvalue().strip()
        expected = "pickle [type] (export, load)" \
                   '\nExport the stored data to a pickle file or load data ' \
                   'from the pickle file.'
        self.assertEqual(expected, output)

    def test_viewHelp_load(self):
        with self.captured_output() as (out, err):
            self.__view.help_load()
        output = out.getvalue().strip()
        expected = "load [location] (file, database)" \
                   '\nLoad from the database or file'
        self.assertEqual(expected, output)

    def test_viewHelp_validate(self):
        with self.captured_output() as (out, err):
            self.__view.help_validate()
        output = out.getvalue().strip()
        expected = "validate" \
                   '\nValidates all loaded data'
        self.assertEqual(expected, output)

    def test_viewHelp_display(self):
        with self.captured_output() as (out, err):
            self.__view.help_display()
        output = out.getvalue().strip()
        expected = "display [type] (unchecked, stored, graph, database)" \
                   '\nDisplay all the stored data'
        self.assertEqual(expected, output)

    def test_viewHelp_exit(self):
        with self.captured_output() as (out, err):
            self.__view.help_exit()
        output = out.getvalue().strip()
        expected = "exit" \
                   '\nExits the command line'
        self.assertEqual(expected, output)

    def test_do_exit(self):
        with self.captured_output() as (out, err):
            self.__view.do_exit("")
        output = out.getvalue().strip()
        expected = "Exiting....."
        self.assertEqual(expected, output)

    def test_viewHelp_welcome(self):
        with self.captured_output() as (out, err):
            self.__view.help_welcome()
        output = out.getvalue().strip()
        expected = "welcome" \
                   '\nWelcomes the user to the program'
        self.assertEqual(expected, output)

    def test_do_welcome(self):
        with self.captured_output() as (out, err):
            self.__view.do_welcome("")
        output = out.getvalue().strip()
        expected = "Welcome to the program." \
                   '\nThe date is ' + str(self.__today)
        self.assertEqual(expected, output)


if __name__ == '__main__':
    unittest.main(verbosity=2)
