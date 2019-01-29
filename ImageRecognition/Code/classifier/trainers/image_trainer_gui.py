"""Graphical User Interface for the image recognition trainer."""

__date__ = '09/20/2018'
__authors__ = [
    'Hayden Phothong, Research Analyst Intern @ ITD'
]

from gui import GUI
from applications import *

import datetime
import os
import sys
import time

PY_VERSION = sys.version_info.major

if PY_VERSION == 2:
    from Tkinter import *
    import tkMessageBox
    import tkFileDialog
else:
    from tkinter import *
    import messagebox
    import filedialog

from PIL import Image
from PIL import ImageTk

DEFAULT_DATABASE_FILEPATH = (
    '../../ImageRecognition.db'
)

# 0 days, 0 seconds, 500000 microseconds
BUTTON_DELAY = datetime.timedelta(0, 0, 500000)


class ImageTrainerGUI(GUI):

    def __init__(self):
        """Creates a GUI for the image trainer."""
        GUI.__init__(self)

        self.__previous_time = datetime.datetime.now()
        self.__user = os.environ.get("USERNAME")
        self.__computer = os.environ.get("COMPUTERNAME")
        self.__database_filepath = DEFAULT_DATABASE_FILEPATH

        self.__application = ImageRecognition(self.__database_filepath)
        self.__init_assets()
        self.__init_config()
        self.__init_menu()
        self.__init_widgets()
        self.__init_shortcuts()

        self.load_image(self.__application.get_next_image())

        # Assign Row Weights
        for i in range(5):
            if i == 2:
                continue
            else:
                self.grid_rowconfigure(i, weight=1)

        # Assign Column Weights
        for i in range(10):
            self.grid_columnconfigure(i, weight=1)

        self.show()

    def __init_assets(self):
        """Initializes the assets from the database."""
        self.__asset_dt = {}

        self.__assets = self.__application.get_assets()
        for asset in self.__assets:
            self.__asset_dt[asset] = None

        if len(self.__asset_dt.keys()) < 1:
            raise ValueError("There are no assets to check from the database")

    def __init_config(self):
        """Initializes the main window"""
        self.title("Image Recognition Trainer")
        self.geometry("1280x720+300+150")
        self.minsize(1280, 800)
        self.width = 1280
        self.height = 800
        self.grid()
        self.protocol("WM_DELETE_WINDOW", self.__close)
        self.bind("<Configure>", self.__resize)
        self.__previous_stack = []

    def __init_menu(self):
        """Creates the menu bar for the application."""
        self.set_menubar()

        # Create the file menu
        self.menubar.add_menu("File")

        self.menubar["File"].add_command(
            label="New Directory",
            command=self.__new_directory
        )

        # Create the help menu
        self.menubar.add_menu("Help")

        self.menubar["Help"].add_command(
            label="Full Database Path",
            command=lambda: self.__help("Full Database Path")
        )
        self.menubar["Help"].add_command(
            label="Statistics",
            command=lambda: self.__help("Statistics")
        )
        self.menubar["Help"].add_command(
            label="About",
            command=lambda: self.__help("About")
        )

    def __init_shortcuts(self):
        """Initializes all of the shortcut keys."""
        self.bind('y', self.__yes_function)
        self.bind('n', self.__no_function)

    def __init_widgets(self):
        """Intialize all of the widgets on the page."""

        # Initialize the back button
        self.__back_button = Button(
            self.frame,
            text="Back",
            font=("arial", 18),
            command=self.__back_function
        )
        self.__back_button.grid(column=0, row=0, sticky=W)

        # Initialize the Database label
        self.__database_text = StringVar()
        self.__database_text.set(
            "Database: " +
            os.path.basename(
                self.__database_filepath))
        self.__database_label = Label(
            self.frame,
            textvariable=self.__database_text,
            font=("arial", 18),
            wraplength=int(self.width * 0.40)
        )
        self.__database_label.grid(column=1, columnspan=6, row=0, sticky=W)

        # Initialize the image name
        self.__image_name = StringVar()
        self.__image_name_label = Label(
            self.frame,
            textvariable=self.__image_name,
            font=("arial", 18)
        )
        self.__image_name_label.grid(column=7, columnspan=3, row=0, sticky=W)

        # Initialize the No button
        self.__no_button = Button(
            self.frame,
            text="No",
            bg="red",
            width=20,
            height=2,
            pady=12,
            font=("arial", 24),
            command=self.__no_function
        )
        self.__no_button.grid(
            column=0,
            columnspan=3,
            row=2,
            rowspan=3,
            sticky=S + W)

        # Initialize the prompt
        self.__label_text = StringVar()
        self.__current_asset_index = 0
        self.__current_asset = self.__assets[self.__current_asset_index]
        self.__label_text.set(
            "Is a {} present?".format(
                self.__current_asset.replace(
                    "_", " ")))
        self.__prompt_label = Label(
            self.frame,
            textvariable=self.__label_text,
            font=("arial", 24),
            wraplength=int(self.width * 0.35)
        )
        self.__prompt_label.grid(column=3, columnspan=4, row=2, sticky=S)

        # Initialize the yes button
        self.__yes_button = Button(
            self.frame,
            text="Yes",
            bg="green",
            width=20,
            height=2,
            pady=12,
            font=("arial", 24),
            command=self.__yes_function
        )
        self.__yes_button.grid(
            column=7,
            columnspan=3,
            row=2,
            rowspan=3,
            sticky=S + E)

    def __back_function(self):
        """Function when the back button is pressed."""
        current_time = datetime.datetime.now()

        if current_time - self.__previous_time < BUTTON_DELAY:
            return
        else:
            self.__previous_time = current_time

        if self.__current_asset_index == 0:
            self.__previous_stack.append(self.__image_id)
            self.load_image(
                self.__application.get_previous_image(
                    self.__user,
                    *self.__previous_stack
                )
            )

        else:
            self.__current_asset_index -= 1

        self.__current_asset = self.__assets[self.__current_asset_index]
        self.__label_text.set(
            "Is a {} present?".format(
                self.__current_asset.replace(
                    "_", " ")))

    def __close(self):
        """Function called when the windows is closed."""
        if PY_VERSION == 2:
            if tkMessageBox.askyesno(
                    "Exit", "Do you want to exit the application?"):
                self.__application.clear_unfinished_images(self.__user)
                self.destroy()
        else:
            if messagebox.askyesno(
                    "Exit", "Do you want to exit the application?"):
                self.__application.clear_unfinished_images(self.__user)
                self.destroy()

    def __help(self, help_type):
        """Shows the about message for the application."""
        if help_type == "About":
            help_message = (
                """
                Image classifier application that will connect to the SQLite3
                database on the common shared drive to store information
                about images that are being displayed.
                """.replace("\t\t\t", " ").replace("\n", "")
            )

            help_message += (
                """\n
                Authors:
                Hayden Phothong, Research Analyst Intern @ ITD......09/11/2018
                """.replace("\t\t\t", "")
            )

        elif help_type == "Full Database Path":
            help_message = (
                "Database can be found at: " + self.__database_filepath
            )

        elif help_type == "Statistics":
            help_message = self.__application.get_statistics(*self.__assets)

        if PY_VERSION == 2:
            tkMessageBox.showinfo(help_type, help_message)
        else:
            messagebox.showinfo(help_type, help_message)

    def __new_directory(self):
        """Allows the user to change the target image directory from
        the database.
        """
        if PY_VERSION == 2:
            self.__database_filepath = tkFileDialog.askdirectory()
        else:
            self.__database_filepath = filedialog.askdirectory()

    def __no_function(self, event=None):
        """Function when the no button is pressed."""
        current_time = datetime.datetime.now()
        if current_time - self.__previous_time < BUTTON_DELAY:
            print(current_time - self.__previous_time)
            return
        else:
            self.__current_asset_index += 1
            self.__previous_time = current_time

        self.__asset_dt[self.__current_asset] = 0

        if self.__current_asset_index == len(self.__assets):
            self.__current_asset_index = 0
            self.__application.classify_image(
                self.__image_id,
                self.__user,
                self.__computer,
                self.__previous_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
                **self.__asset_dt
            )
            if self.__previous_stack:
                self.load_image(
                    self.__application.get_image_at(
                        self.__previous_stack.pop()
                    )
                )
            else:
                self.load_image(self.__application.get_next_image())

        self.__current_asset = self.__assets[self.__current_asset_index]
        self.__label_text.set(
            "Is a {} present?".format(
                self.__current_asset.replace(
                    "_", " ")))

    def __resize(self, event):
        """Function to call when the frame is resized."""
        self.width = self.winfo_width()
        self.height = self.winfo_height()

        # Update Prompt
        self.__prompt_label.configure(wraplength=int(self.width * 0.33))

        # Update Image
        self.__resized_photo = self.__photo.resize(
            (
                int(self.width * 0.993),
                int(self.height * 0.85)
            ),
            Image.ANTIALIAS
        )
        self.__resized_photo = ImageTk.PhotoImage(self.__resized_photo)
        self.__image.config(
            image=self.__resized_photo,
            width=self.width,
            height=int(self.height * 0.82)
        )

    def __yes_function(self, event=None):
        """Function when the yes button is pressed."""
        current_time = datetime.datetime.now()
        if current_time - self.__previous_time < BUTTON_DELAY:
            print(current_time - self.__previous_time)
            return
        else:
            self.__current_asset_index += 1
            self.__previous_time = current_time

        self.__asset_dt[self.__current_asset] = 1

        if self.__current_asset_index == len(self.__assets):
            self.__current_asset_index = 0
            self.__application.classify_image(
                self.__image_id,
                self.__user,
                self.__computer,
                self.__previous_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
                **self.__asset_dt
            )

        self.load_image(self.__application.get_next_image(self.__image_id))

        self.__current_asset = self.__assets[self.__current_asset_index]
        self.__label_text.set(
            "Is a {} present?".format(
                self.__current_asset.replace(
                    "_", " ")))

    def load_image(self, image_info):
        """
        Loads the image to the tkinter window

        Keyword arguments:
        image_info -- The image_id and the image_filepath
        """
        self.__image_id = str(image_info[0])
        initialize_dt = {}
        for asset in self.__assets:
            initialize_dt[asset] = -1

        self.__application.classify_image(
            self.__image_id,
            self.__user,
            self.__computer,
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            **initialize_dt
        )
        self.__image_name.set("Image Filename: " + str(image_info[1]))
        self.__image_filepath = str(image_info[2])
        self.__photo = Image.open(self.__image_filepath)
        self.__resized_photo = ImageTk.PhotoImage(self.__photo)
        self.__image = Label(
            self.frame,
            image=self.__resized_photo,
            width=self.width,
            height=int(self.height * 0.82)
        )
        self.__image.grid(columnspan=10, row=1)
