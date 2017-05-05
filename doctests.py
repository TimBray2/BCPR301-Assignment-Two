"""
# Doctests for the load function
>>> control = Controller(cmd_view.CmdView())
>>> control.load("database")
Opened database successfully
Finishing connection to database
Loaded from database

>>> control.load("database employee")
Please select to load from 'database' or 'file [location]'

>>> control.load("12312")
Please select to load from 'database' or 'file [location]'

>>> control.load("file")
Please select to load from 'database' or 'file [location]'

>>> control.load("file validInputData.txt")
Loaded from file

>>> control.load("file doesNotExist.txt")
Please select a valid file location

"""
from controller import Controller
import cmd_view

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
