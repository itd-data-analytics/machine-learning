"""Functions to query for statistics in the database."""

import sqlite3

__authors__ = [
    'Hayden Phothong, Research Anslyst Intern @ ITD'
]


class ImageRecognitionStats:
    """Represent the statistics of the image recognition database."""

    @classmethod
    def __get_cursor(cls):
        """Return the cursor to the ImageRecognition database."""
        cls.connection = sqlite3.connect('../../ImageRecognition.db')
        return cls.connection.cursor()

    @classmethod
    def completed_images_count(cls, field):
        """Return the number of completed images."""
        cursor = cls.__get_cursor()
        try:
            # Load assets
            cursor.execute('SELECT asset_name FROM Assets;')
            asset_names = []
            for row in cursor:
                asset_names.append(row[0].lower())

            # Query number of completed images
            for asset_name in asset_names:
                if field.lower() in asset_name:
                    query = (
                        """
                        SELECT COUNT(*) FROM CompletedImages
                        WHERE {}_present = 1 OR {}_present = 0;
                        """.format(field, field)
                    )
                    break
            cursor.execute(query)
            completed_images_count = cursor.fetchone()[0]

            cls.connection.close()

            return completed_images_count

        except Exception as e:
            return e

    @classmethod
    def percent_images_completed(cls, field):
        """Return the percent of completed images from the total."""
        try:
            cursor = cls.__get_cursor()

            # Load number of total images
            cursor.execute('SELECT COUNT(*) FROM Images;')
            total_images = cursor.fetchone()[0]

            # Get completed images count
            completed_images_count = cls.completed_images_count(field)

            percent = float(completed_images_count) / total_images
            percent *= 100
            percent = round(percent, 2)

            cls.connection.close()

            return percent

        except Exception as e:
            return e
