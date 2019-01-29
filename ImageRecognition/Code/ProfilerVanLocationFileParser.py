"""
File: HPMSBigFiveFormatting.py

Authors:
	Chapman Munn, Research Analyst Principal @ ITD.......08/24/2018

Description:
	Parses Pathways Profiler Van index files, extracts geometric location
	and image data, and writes that data to a predefined SQLITE3 database
"""

import os
import sqlite3

#image recognition filepath
image_recognition_filepath = '//itdhwy/DESFiles/DES/TransportationSystems/Common/ImageRecognition/'

#test filepath
fp = '//itdd03fsp01/Videolog/Dist32016Final.SEC'


def parse_index_file(filepath):
	"""
	Parses an index file into a list of lists 
	
	Keyword arguments:
	
	filepath -- the filepath of the index file

	returns -- a list of lists
	"""
	with open (filepath, 'r') as r:
		data = r.readlines()
	return data

def structure_index_data(index_lt):
	"""
	Parses lines from the index file and creates dictionaries for each
	possible image name 
	
	Keyword arguments:
	
	index_lt -- list of lines from parse_index_file()

	returns -- a list of dictionaries of parsed index data
	"""
	value_lt = []
	for i in index_lt:
		split_lines  = i.split('!')
		segment_code = split_lines[4]
		district     = split_lines[7]
		route        = split_lines[9]
		from_measure = split_lines[12]
		to_measure   = split_lines[13]
		direction    = split_lines[16]
		set_number   = split_lines[41]
		image_start  = split_lines[42]
		image_end    = split_lines[43]
		view         = '1'
		potential_images = [c for c in range(int(image_start), int(image_end) + 1)]
		for item in potential_images:
			image_data = {
			'route_id'     : segment_code,
			'district'     : district,
			'route_name'   : route,
			'from_measure' : from_measure,
			'to_measure'   : to_measure,
			'direction'    : direction,
			'set_number'   : set_number,
			'image_start'  : image_start,
			'image_end'    : image_end,
			'image_name'   : str(item) + view,
			}
			value_lt.append(image_data)
	return value_lt
		
def port_to_database(data_lt, database, table):
	"""
	Writes the parsed and structured index file data to a pre-existing 
	SQLITE3 database and table
	
	Keyword arguments:
	
	data_lt -- list of dictionaries from structure_index_data()
	database -- database location
	table -- table within data base to write to
	"""
	database_connection = sqlite3.connect(database)
	cursor = database_connection.cursor()
	
	raw_line = """
	INSERT INTO {0} VALUES(
	'{1}',
	'{2}',
	'{3}',
	'{4}',
	'{5}',
	'{6}',
	'{7}',
	'{8}',
	'{9}',
	'{10}'
	)
	"""
	for item in data_lt:
		insert_line = raw_line.format(
		table, 
		str(item['route_id']), 
		str(item['district']), 
		str(item['route_name']), 
		str(item['from_measure']), 
		str(item['to_measure']),
		str(item['direction']),
		str(item['set_number']),
		str(item['image_start']),
		str(item['image_end']),
		str(item['image_name'])
		)
		print (insert_line)
		cursor.execute(insert_line)
	database_connection.commit()
	database_connection.close()
		
port_to_database(structure_index_data(parse_index_file(fp)), image_recognition_filepath + 'Database/ImageRecognition.db', 'Location')
