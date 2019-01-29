"""Module to implement a menubar for a Tkinter window."""

__date__ = '09/13/2018'
__authors__ = [
    'Hayden Phothong, Research Analyst Intern @ ITD'
]

import sys
PY_VERSION = sys.version_info.major

if PY_VERSION == 2:

    from Tkinter import *
else:
    from tkinter import *


class Menubar(Menu):

    def __init__(self, master):
        """
        Initializes the menu with the passed in master

        Keyword arguments:
        master -- The parent Tkinter object to reference the menu to
        """
        Menu.__init__(self, master)
        self.__menu_dt = {}

    def __getitem__(self, menu_name):
        """
        Returns the menu with the specified name

        Keyword arguments:
        menu_name -- The name of the target menu
        """
        return self.__menu_dt[menu_name]

    def add_menu(self, menu_name):
        """
        Adds a dropdown menu to the menubar

        Keyword arguments:
        menu_name -- The name of the menu to add
        """
        self.__menu_dt[menu_name] = Menu(self, tearoff=0)
        self.add_cascade(label=menu_name, menu=self.__menu_dt[menu_name])

    def get_menu(self, menu_name=None):
        """
        If a menu name is not passed in, the menu dictionary will
        be returned. If the menu name was passed in, then it will
        attempt to return the menu with that name. If the menu cannot
        be found, it will raise a ValueError.

        Keyword arguments:
        menu_name -- The name of the target menu
        """
        try:
            if menu_name is None:
                return self.__menu_dt
            else:
                return self.__menu_dt[menu_name]

        except KeyError:
            raise ValueError(
                "{} is not in the menu dictionary".format(menu_name))
