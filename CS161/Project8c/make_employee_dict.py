# Author: Kevin Sekuj
# Date: 11/18/20
# Description: Program which contains an Employee class containing data
# members for several parameters including employee name and salary. The program
# initializes those data members into private data members, and has a get method
# for them to be accessed later on by the function make_employee_dict.
#
# The function iterates through the values of the four list parameters and uses them
# to create an employee object "emp." As the object is created, it's assigned
# to the dictionary emp_dict, using the ID number as key and its value as the whole object.
# Finally the function returns the resulting dictionary.

class Employee:
    """
    Employee class containing four private data members for the employee,
    including their name, id number, salary, and email address.
    """

    def __init__(self, name, ID_number, salary, email_address):
        """
        Initializes private data members for the employee
        """
        self._name = name
        self._ID_number = ID_number
        self._salary = salary
        self._email_address = email_address

    def get_name(self):
        """
        Get method to return employee name
        """
        return self._name

    def get_ID_number(self):
        """
        Get method to return employee ID number
        """
        return self._ID_number

    def get_salary(self):
        """
        Get method to return employee salary
        """
        return self._salary

    def get_email_address(self):
        """
        Get method to return employee's email address
        """
        return self._email_address


def make_employee_dict(_name, _ID_number, _salary, _email_address):
    """
    Function which goes through the first value and forward through a list
    using them to create an employee object emp, which is used to return
    a dictionary with ID number keys and the whole Employee object as values.
    """
    emp_dict = {}  # initializing dictionary
    for member in range(len(_name)):
        # using first->last member (element) of list to create employee object
        emp = Employee(_name[member], _ID_number[member], _salary[member], _email_address[member])
        emp_dict[_ID_number[member]] = emp
    return emp_dict
