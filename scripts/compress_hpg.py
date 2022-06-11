# -*- coding: utf-8 -*-

"""
	Copyright (C) 2022  Soheil Khodayari, CISPA
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU Affero General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.
	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU Affero General Public License for more details.
	You should have received a copy of the GNU Affero General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.


	Description:
	------------
	Script to compress property graphs

"""

import zipfile
import argparse
import pandas as pd
import os
import utils.io as IOModule
from utils.logging import logger as LOGGER
import shutil

BASE_DIR= os.path.dirname(os.path.realpath(__file__))


def remove_if_exists(file_path_name):
	if os.path.isfile(file_path_name):
		os.remove(file_path_name)


def get_name_from_url(url):

	"""
	 @param url: eTLD+1 domain name
	 @return converts the url to a string name suitable for a directory by removing the colon and slash symbols

	"""
	return url.replace(':', '-').replace('/', '')


# https://stackoverflow.com/questions/8156707/gzip-a-file-in-python
def unzip(path_to_zip_file, directory_to_extract_to):
	
	with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
		zip_ref.extractall(directory_to_extract_to)


def compress_graph(webpage_folder_path):

	nodes_file = os.path.join(webpage_folder_path, 'nodes.csv')
	rels_file = os.path.join(webpage_folder_path, 'rels.csv')

	if os.path.exists(nodes_file) and os.path.exists(rels_file):
		compression = zipfile.ZIP_DEFLATED
		zip_file_name = os.path.join(webpage_folder_path,'graph.zip')
		zip_fd = zipfile.ZipFile(zip_file_name, 'w')
		zip_fd.write(nodes_file, 'nodes.csv', compress_type=compression)
		zip_fd.write(rels_file, 'rels.csv', compress_type=compression)
		
		### https://docs.python.org/3/library/zipfile.html#zipfile.ZipFile.testzip
		# zip_status = zip_fd.testzip()
		# if zip_status is None:
		# 	print('ZIP CRC header does not match.')

		zip_fd.close()

		os.remove(nodes_file)
		os.remove(rels_file)


## https://www.tecmint.com/compress-files-faster-in-linux/
def compress_graph_pigz(webpage_folder_path):

	compress_command = "pigz {0}/nodes.csv".format(webpage_folder_path)
	IOModule.run_os_command(compress_command, print_stdout=False)

	compress_command = "pigz {0}/rels.csv".format(webpage_folder_path)
	IOModule.run_os_command(compress_command, print_stdout=False)


## https://www.tecmint.com/compress-files-faster-in-linux/
def decompress_graph_pigz(webpage_folder_path):

	decompress_command = "pigz -d {0}/nodes.csv".format(webpage_folder_path)
	IOModule.run_os_command(decompress_command, print_stdout=False)

	decompress_command = "pigz -d {0}/rels.csv".format(webpage_folder_path)
	IOModule.run_os_command(decompress_command, print_stdout=False)


def decompress_graph(webpage_folder_path):

	zip_file = os.path.join(webpage_folder_path,'graph.zip')
	if os.path.exists(zip_file):
		unzip(zip_file, webpage_folder_path)
		os.remove(zip_file)

def zip_and_delete_graph(website_url):
	
	webapp_directory_name = get_name_from_url(website_url)
	webapp_data_directory = os.path.join(os.path.join(BASE_DIR, "data"), webapp_directory_name)
	if os.path.exists(webapp_data_directory):
		webapp_url_folder_names = os.listdir(webapp_data_directory)
		for webapp_url_folder_name in webapp_url_folder_names:
			webapp_url_folder_path_name = os.path.join(webapp_data_directory, webapp_url_folder_name)
			if os.path.exists(webapp_url_folder_path_name) and os.path.isdir(webapp_url_folder_path_name):
				nodes_file = os.path.join(webapp_url_folder_path_name, 'nodes.csv')
				rels_file = os.path.join(webapp_url_folder_path_name, 'rels.csv')
				zip_file = os.path.join(webapp_url_folder_path_name,'graph.zip')
				nodes_file_gz = os.path.join(webapp_url_folder_path_name, 'nodes.csv.gz')
				rels_file_gz = os.path.join(webapp_url_folder_path_name, 'rels.csv.gz')

				if os.path.exists(nodes_file) and os.path.exists(rels_file):
					# compress_graph(webapp_url_folder_path_name)
					compress_graph_pigz(webapp_url_folder_path_name)
				
				# elif os.path.exists(zip_file):
				# 	decompress_graph(webapp_url_folder_path_name)
					
				# elif os.path.exists(nodes_file_gz) and os.path.exists(rels_file_gz):
				# 	decompress_graph_pigz(webapp_url_folder_path_name)





def main():

	CONFIG_FILE_DEFAULT = 'config.domclobbering.yaml'
	p = argparse.ArgumentParser(description='This script runs the tool pipeline.')
	p.add_argument('--conf', "-C",
					metavar="FILE",
					default=CONFIG_FILE_DEFAULT,
					help='Pipeline configuration file. (default: %(default)s)',
					type=str)

	args= vars(p.parse_args())
	config = IOModule.load_config_yaml(args["conf"])
	BASE_DIR= os.path.dirname(os.path.realpath(__file__))
	testbed_filename = BASE_DIR.rstrip('/') + config["testbed"]["sitelist"].strip().strip('\n').strip()
	from_row = int(config["testbed"]["from_row"])
	to_row = int(config["testbed"]["to_row"])

	chunksize = 10**4
	iteration = 0
	done = False

	for chunk_df in pd.read_csv(testbed_filename, chunksize=chunksize, usecols=[0, 1], header=None, skip_blank_lines=True):
		if done:
			break

		iteration = iteration + 1
		LOGGER.info("starting to zip chunk: %s -- %s"%((iteration-1)*chunksize, iteration*chunksize))
		
		for (index, row) in chunk_df.iterrows():
			g_index = iteration*index+1
			if g_index >= from_row and g_index <= to_row:

				website_rank = row[0]
				website_url = 'http://' + row[1]
				LOGGER.info('compressing data of: {0} - {1}'.format(website_rank, website_url))
				zip_and_delete_graph(website_url)
			

			if g_index > to_row:
					done = True
					LOGGER.info("successfully zipped sites' data, terminating!") 
					break


if __name__ == "__main__":
	main()


