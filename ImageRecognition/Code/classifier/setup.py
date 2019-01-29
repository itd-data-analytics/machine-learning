"""The setup package for pip install and py2exe."""

__date__ = '09/06/2018'
__authors__ = [
    'Hayden Phothong, Research Analyst Intern @ ITD'
]

from distutils.core import setup

import py2exe

setup(console=['__main__.py'], options={"py2exe": {"dll_excludes": [
    "libopenblas.UWVN3XTD2LSS7SFIFK6TIQ5GONFDBJKU.gfortran-win32.dll"]}})
