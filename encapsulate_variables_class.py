# Author: Barrett Duna

from testfixtures import ShouldRaise


class EncapsulateVariables:

    """
    Class that provides an encapsulation of variables.
    It keeps the outer name scope clean of the variables
    passed to the EncapsulateVariables class.
    """

    def __init__(self, **kwargs):
        """
        Creates class instance and loads encapsulated
        variables as keyword arguments.
        """
        for var_name, val in kwargs.items():
            self.__dict__[var_name] = val

    def add_var(self, var_name, val):
        """
        Adds a single variable to the class instance
        with variable name var_name and value val.
        """
        self.__dict__[var_name] = val

    def add_vars(self, **kwargs):
        """
        Adds multiple variables to class instance as
        keyword arguments.
        """
        for var_name, val in kwargs.items():
            if var_name not in self.__dict__:
                self.__dict__[var_name] = val


if __name__ == '__main__':

    # create an EncapsulateVariables instance with variables
    # x, y and z
    var_encaps = EncapsulateVariables(x="variable x", y="variable y",
                                      z="variable z")

    # print newly created instance variables
    print("__init__ Variables...")
    print(var_encaps.x)
    print(var_encaps.y)
    print(var_encaps.z)

    # access to variables as local variables raises a NameError
    with ShouldRaise(NameError):
        print(x)

    with ShouldRaise(NameError):
        print(y)

    with ShouldRaise(NameError):
        print(z)

    # uses add_var method to add instance variables a, b and c
    var_encaps.add_var("a", "variable a")
    var_encaps.add_var("b", "variable b")
    var_encaps.add_var("c", "variable c")

    # print newly created instance variables
    print("add_var Variables...")
    print(var_encaps.a)
    print(var_encaps.b)
    print(var_encaps.c)

    # access to variables as local variables raises a NameError
    with ShouldRaise(NameError):
        print(a)

    with ShouldRaise(NameError):
        print(b)

    with ShouldRaise(NameError):
        print(c)

    # uses add_vars method to add instance variables m, n and o
    var_encaps.add_vars(m="variable m", n="variable n", o="variable o")

    # print newly created instance variables
    print("add_vars variables")
    print(var_encaps.m)
    print(var_encaps.n)
    print(var_encaps.o)

    # access to variables as local variables raises a NameError
    with ShouldRaise(NameError):
        print(m)

    with ShouldRaise(NameError):
        print(n)

    with ShouldRaise(NameError):
        print(o)
