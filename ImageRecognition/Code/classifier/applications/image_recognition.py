"""This module will contain all of the functionality for classifying images."""

from image_recognition_stats import ImageRecognitionStats

import sqlite3

__authors__ = [
    'Hayden Phothong, Research Anslyst Intern @ ITD'
]


class ImageRecognition(object):
    """Application to store/retrieve data from the SQLite3 database."""

    def __init__(self, database_filepath):
        """Create a connection to the database.

        Keyword arguments:
        database_filepath -- The filepath to the database

        Returns:
        asset_lt -- The list of assets to be executed

        """
        try:
            self.__connection = sqlite3.connect(database_filepath)
            self.__cursor = self.__connection.cursor()
            self.__load_assets()

        except sqlite3.Error as e:
            print(e)

    def __load_assets(self):
        """Load the assets into a list to be iterated over."""
        # Loads the assets into the asset list
        self.__cursor.execute("SELECT asset_name FROM Assets;")
        self.__asset_lt = []
        for row in self.__cursor:
            self.__asset_lt.append(str(row[0]).replace(" ", "_"))

        # Verifies all of the assets with column headers for completed assets
        for asset in self.__asset_lt:
            query = (
                "ALTER TABLE CompletedImages ADD {}_present INTEGER".format(
                    asset
                )
            )
            try:
                self.__cursor.execute(query)

            except sqlite3.Error:
                continue

    def classify_image(
            self,
            image_id,
            username,
            computername,
            datetime,
            **asset_value):
        """Classify the images.

        Keyword arguments:
        image_id -- The image id from the database
        username -- The user that is committing the change
        computername -- The computer that the user is logged into
        datetime -- The datetime in YYYY-MM-DD HH:MM:SS.SSS format
        asset_value -- The asset, value pair dictionary to add to the database
        """
        # Check if the row alread exists
        query = (
            """
            SELECT COUNT(*) FROM CompletedImages
            WHERE image_id = {};
            """.format(image_id)
        )
        self.__cursor.execute(query)
        for row in self.__cursor:
            if row[0] > 0:
                row_exists_in_table = True
            else:
                row_exists_in_table = False
            break

        if row_exists_in_table:
            # Update the existing row into the table
            query = (
                """
                UPDATE CompletedImages SET image_id={}, username=\"{}\",
                computername=\"{}\", datetime=\"{}\"
                """.format(
                    image_id,
                    username,
                    computername,
                    datetime
                )
            )

            for asset, value in asset_value.iteritems():
                query += ", {}_present={}".format(asset, value)

            query += " WHERE image_id={};".format(image_id)

        else:
            # Insert new row into the table
            query = (
                """
                INSERT INTO CompletedImages(image_id, username,
                computername, datetime
                """
            )

            for asset in asset_value.keys():
                query += ', {}_present'.format(asset)

            query += ') VALUES({}, \"{}\", \"{}\", \"{}\"'.format(
                image_id,
                username,
                computername,
                datetime
            )

            for value in asset_value.values():
                query += ", {}".format(value)

            query += ");"

        self.__cursor.execute(query)
        self.__connection.commit()

    def clear_unfinished_images(self, username):
        """Remove all of the images that contain an asset classification of -1.

        This is specific per user.

        Keyword arguments:
        username -- The username to query for uncomplete images
        """
        query = (
            """
            DELETE FROM CompletedImages WHERE (username = \"{}\") AND (
            """.format(username)
        )

        # Add asset = -1 to the query for each asset
        for i in range(len(self.__asset_lt)):
            if i != 0:
                query += " OR "
            query += "{}_present = -1".format(self.__asset_lt[i])

        query += ");"

        # Execute the delete query and commit the changes
        self.__cursor.execute(query)
        self.__connection.commit()

    def get_assets(self):
        """Return the asset list."""
        return self.__asset_lt

    def get_image_at(self, image_id):
        """Return the image filepath at the specified image_id."""
        query = (
            """
            SELECT image_id, image_name, image_filepath FROM Images
            WHERE image_id = {};
            """.format(image_id)
        )
        self.__cursor.execute(query)
        return self.__cursor.fetchone()

    def get_next_image(self, image_id=None):
        """Return the next image filepath randomly unless specified."""
        query = (
            """
            SELECT image_id, image_name, image_filepath FROM Images
            WHERE image_id NOT IN (
                SELECT image_id FROM CompletedImages
                WHERE
            """
        )

        # Query for -1 flags in the images
        for i in range(len(self.__asset_lt)):
            if i != 0:
                query += " OR "
            query += "{}_present != -1".format(self.__asset_lt[i])

        if image_id is not None:
            query += (
                """
                ) AND image_id > {image_id} ORDER BY image_id ASC LIMIT 1;
                """.format(
                    image_id=image_id
                )
            )
        else:
            query += ") ORDER BY RANDOM() LIMIT 1;"

        self.__cursor.execute(query)
        return self.__cursor.fetchone()

    def get_previous_image(self, username, *image_ids):
        """Return the image information to the previous image classified.

        Keyword arguments:
        username -- The user to get the previous image for.
        *image_ids -- The image_ids to skip over.
        """
        query = (
            """
            SELECT image_id, image_name, image_filepath FROM Images
            WHERE image_id IN (
                SELECT image_id FROM CompletedImages
                WHERE username = \"{user}\"
            """.format(user=username)
        )

        for image_id in image_ids:
            query += ' AND image_id != {} '.format(image_id)

        query += 'ORDER BY datetime DESC LIMIT 1);'

        self.__cursor.execute(query)
        return self.__cursor.fetchone()

    def get_statistics(self, *fields):
        """Return a string of the statistics for classification."""
        statistics_string = ''
        for field in fields:
            statistics_string += 'Percent Completed: {}%\n'.format(
                ImageRecognitionStats.percent_images_completed(field)
            )
            statistics_string += 'Total Classified: {} Images\n'.format(
                ImageRecognitionStats.completed_images_count(field)
            )
        return statistics_string
