"""Module to make the Tk window and the main frame that will have
content added to it.
"""

__date__ = '09/13/2018'
__authors__ = [
    'Hayden Phothong, Research Anslyst Intern @ ITD'
]

from menubar import Menubar

import sys
PY_VERSION = sys.version_info.major

if PY_VERSION == 2:
    from Tkinter import Tk
    from Tkinter import Frame
else:
    from tkinter import Tk
    from tkinter import Frame


class GUI(Tk):

    def __init__(self):
        """Initialize a Tk window."""
        Tk.__init__(self)
        self.geometry("1280x720+300+150")
        self.frame = Frame(self)
        self.frame.pack(fill="both", expand=True)

    def set_menubar(self):
        """Adds a menubar to the gui."""
        self.menubar = Menubar(self)
        self.config(menu=self.menubar)

    def show(self):
        self.mainloop()
