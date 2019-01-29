"""Module that will contain image training helper functions."""

import os
import pickle
import re
import sqlite3
import sys

__authors__ = [
    'Hayden Phothong, Research Analyst Intern @ ITD'
]


def get_image_set(field, number_of_true_images=None):
    """Create the image set.

    Keyword arguments:
    field -- The field to search for a true value
    number_of_true_images -- The number of filepaths to return.
    """
    # Connect to database
    DATABASE = '../../ImageRecognition.db'

    database_connection = sqlite3.connect(DATABASE)
    database_cursor = database_connection.cursor()

    # Get column names with arbitrary query
    database_cursor.execute("SELECT * FROM CompletedImages LIMIT 1;")
    column_names = []
    for column_tuple in database_cursor.description:
        column_names.append(column_tuple[0])

    # Fuzzy match field with the column name from the sqlite3 database
    regex = str(field)
    column_match = None
    for column_name in column_names:
        found = re.match(regex, column_name, re.IGNORECASE)
        if found is not None:
            column_match = column_name
            del(column_names)
            break

    if column_match is None:
        raise RuntimeError("Could not fuzzy-match field to column name")
    else:
        file = open(".TrainingSet", "w")

    # Query for True or 1 in the matched column
    query = (
        """
        SELECT image_filepath FROM Images
        WHERE image_id IN (
            SELECT image_id FROM CompletedImages
            WHERE {column_name} = 1
            ORDER BY datetime DESC
        """.format(
            column_name=column_match
        )
    )

    # Limit the results if a number was passed to the method
    if number_of_true_images is not None:
        query += " LIMIT {}".format(number_of_true_images)
    query += ");"
    database_cursor.execute(query)

    # Pickle all of the filepaths:field_present pairs to the file
    # Progress count is used for number of true images is None
    progress_count = 0
    for row in database_cursor:
        progress_count += 1
        image_data = (row[0], 1)
        pickle.dump(image_data, file)

    # Query for False or 0 in the matched column
    query = (
        """
        SELECT image_filepath FROM Images
        WHERE image_id IN (
            SELECT image_id FROM CompletedImages
            WHERE {column_name} = 0
            ORDER BY datetime DESC
        """.format(
            column_name=column_match
        )
    )

    # Limit the results if a number was passed to the method
    if number_of_true_images is not None:
        query += " LIMIT {}".format(number_of_true_images)
    else:
        query += " LIMIT {}".format(progress_count)
    query += ");"
    database_cursor.execute(query)

    # Pickle all of the filepaths:field_present pairs to the file
    for row in database_cursor:
        image_data = (row[0], 0)
        pickle.dump(image_data, file)

    # Close the file and return it's filepath
    file.close()
    database_connection.close()
    return os.path.abspath(".TrainingSet")


def get_true_images(field):
    """Create a list of tuples that contain the image filepath.

    The value of 1 for the field specified.

    Keyword Arguments:
    field -- The field to search for in the column names

    Returns:
    image_set -- The set of (image_filepath, 1) tuples

    """
    # Connect to the database.
    DATABASE = '../../ImageRecognition.db'

    database_connection = sqlite3.connect(DATABASE)
    database_cursor = database_connection.cursor()

    # Get column names with arbitrary query.
    database_cursor.execute("SELECT * FROM CompletedImages LIMIT 1;")
    column_names = []
    for column_tuple in database_cursor.description:
        column_names.append(column_tuple[0])

    # Fuzzy match field with the column name from the sqlite3 database.
    regex = str(field)
    column_match = None
    for column_name in column_names:
        found = re.match(regex, column_name, re.IGNORECASE)
        if found is not None:
            column_match = column_name
            del(column_names)
            break

    if column_match is None:
        raise RuntimeError("Could not fuzzy-match field to column name")

    # Query for True or 1 in the matched column.
    query = (
        """
        SELECT image_filepath FROM Images
        WHERE image_id IN (
            SELECT image_id FROM CompletedImages
            WHERE {column_name} = 1
            ORDER BY datetime DESC
        );
        """.format(
            column_name=column_match
        )
    )
    database_cursor.execute(query)

    # Build the list of tuples
    image_set = []
    for row in database_cursor:
        data = (str(row[0]), 1)
        image_set.append(data)

    database_connection.close()
    return image_set


def get_false_images(field):
    """Create a list of tuples that contain the image filepath.

    The value of 0 for the field specified.

    Keyword Arguments:
    field -- The field to search for in the column names

    Returns:
    image_set -- The set of (image_filepath, 1) tuples

    """
    # Connect to the database.
    DATABASE = '../../ImageRecognition.db'

    database_connection = sqlite3.connect(DATABASE)
    database_cursor = database_connection.cursor()

    # Get column names with arbitrary query.
    database_cursor.execute("SELECT * FROM CompletedImages LIMIT 1;")
    column_names = []
    for column_tuple in database_cursor.description:
        column_names.append(column_tuple[0])

    # Fuzzy match field with the column name from the sqlite3 database.
    regex = str(field)
    column_match = None
    for column_name in column_names:
        found = re.match(regex, column_name, re.IGNORECASE)
        if found is not None:
            column_match = column_name
            del(column_names)
            break

    if column_match is None:
        raise RuntimeError("Could not fuzzy-match field to column name")

    # Query for True or 1 in the matched column.
    query = (
        """
        SELECT image_filepath FROM Images
        WHERE image_id IN (
            SELECT image_id FROM CompletedImages
            WHERE {column_name} = 0
            ORDER BY datetime DESC
        );
        """.format(
            column_name=column_match
        )
    )
    database_cursor.execute(query)

    # Build the list of tuples
    image_set = []
    for row in database_cursor:
        data = (str(row[0]), 0)
        image_set.append(data)

    database_connection.close()
    return image_set
