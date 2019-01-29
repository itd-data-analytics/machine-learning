"""Unit test for the image_recognition module."""

__date__ = '09/18/2018'
__authors__ = [
    'Hayden Phothong, Research Analyst Intern @ ITD'
]

import sqlite3
import sys
import unittest

sys.path.append('../applications/')
from image_recognition import ImageRecognition


class TestImageRecognitionMethods(unittest.TestCase):

    def setUp(self):
        self.database = (
            '//itdhwy/DESFiles/DES/TransportationSystems/Common/'
            + 'ImageRecognition/Database/ImageRecognition.db'
        )
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        self.application = ImageRecognition(self.database)
        self.image_id = -1
        self.username = 'test_user'
        self.computername = 'test_computer'
        self.datetime = '2020-01-01 00:00:00.000000'

    def tearDown(self):
        self.cursor.execute(
            'DELETE FROM CompletedImages WHERE username = \'test_user\''
        )
        self.connection.commit()
        self.connection.close()

    def test_classify_image(self):
        self.application.classify_image(
            self.image_id,
            self.username,
            self.computername,
            self.datetime,
            guardrail=1
        )
        query = 'SELECT * FROM CompletedImages WHERE image_id = '
        query += '{};'.format(self.image_id)
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        self.assertEqual(row[0], self.image_id)
        self.assertEqual(row[1], self.username)
        self.assertEqual(row[2], self.computername)
        self.assertEqual(row[3], self.datetime)
        self.assertEqual(row[4], 1)

    def test_classify_image_update(self):
        self.application.classify_image(
            self.image_id,
            self.username,
            self.computername,
            self.datetime,
            guardrail=1
        )
        self.application.classify_image(
            self.image_id,
            self.username,
            self.computername,
            self.datetime,
            guardrail=0
        )
        query = 'SELECT * FROM CompletedImages WHERE image_id = '
        query += '{};'.format(self.image_id)
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        self.assertEqual(row[0], self.image_id)
        self.assertEqual(row[1], self.username)
        self.assertEqual(row[2], self.computername)
        self.assertEqual(row[3], self.datetime)
        self.assertEqual(row[4], 0)


if __name__ == '__main__':
    unittest.main()
