# -*- coding: utf-8 -*-

"""
	Copyright (C) 2021  Soheil Khodayari, CISPA
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
	script to delete collected data, when necessary due to disk shortage!!

"""

import argparse
import pandas as pd
import os, sys
import utils.io as IOModule
from utils.logging import logger as LOGGER
import analyses.domclobbering.domc_neo4j_traversals as DOMCTraversalsModule
import shutil

BASE_DIR= os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

def get_data_directory(website_url):

	folder = website_url.replace('/', '').replace(':', '-')
	return os.path.join(DATA_DIR, folder)


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

	LOGGER.info("loading config: %s"%str(config))


	if True: 
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

			for (index, row) in chunk_df.iterrows():
				g_index = iteration*index+1
				if g_index >= from_row and g_index <= to_row:

					website_rank = int(row[0])
					website_url = 'http://' + row[1]
					
					if g_index > 4500 and website_rank>4500:
						folder_name = get_data_directory(website_url)
						if os.path.exists(folder_name):
							try:
							    shutil.rmtree(folder_name)
							except OSError as e:
							    print("Error: %s - %s." % (e.filename, e.strerror))

				if g_index > to_row:
					done = True
					break

if __name__ == "__main__":
	main()


