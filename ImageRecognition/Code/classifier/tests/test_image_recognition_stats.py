"""Unit tests for the \"image_recognition_statistics module."""

__date__ = '09/20/2018'
__authors__ = [
    'Hayden Phothong, Research Analyst Intern @ ITD'
]

import sqlite3
import sys
import unittest

sys.path.append('../applications/')
from image_recognition_stats import ImageRecognitionStats


class TestImageRecognitionStats(unittest.TestCase):

    def setUp(self):
        self.database = (
            '//itdhwy/DESFiles/DES/TransportationSystems/Common/'
            + 'ImageRecognition/Database/ImageRecognition.db'
        )
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        query = 'SELECT asset_name FROM Assets;'
        self.cursor.execute(query)
        self.assets = []
        for row in self.cursor:
           self.assets.append(row[0].lower())

    def tearDown(self):
        self.connection.close()

    def test_completed_images_count(self):
        
        self.assertEqual(1, 1)

    def test_percent_images_complete(self):
        # TODO: Finish the percent test
        self.assertEqual(1, 1)
