"""Main file that will start the image trainer

This file will be called every time a user does the bash command \"$ python
imagetrainer\".
"""

__data__ = '08/20/2018'
__authors__ = [
    'Hayden Phothong, Research Analyst Intern @ ITD'
]

import os

import trainers


def run_tests():
    current_directory = os.getcwd()
    print(current_directory)


def main():
    """Main Method."""
    trainers.ImageTrainerGUI()


if __name__ == "__main__":
    # Run test suite
    # execfile(os.path.dirname(__file__) + '\\tests\\__main__.py')

    # Run program
    main()
