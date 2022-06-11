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
	script to run the static analyzer for a single webpage

	Run
	------------
	screen -dmS r1 bash -c 'python3 -m scripts.analyze_webpage --from=1 --to=200 --memory=12000 --timeout=1800; exec sh'

"""

import argparse
import pandas as pd
import os, sys
import utils.io as IOModule
from utils.logging import logger as LOGGER
import analyses.domclobbering.domc_neo4j_traversals as DOMCTraversalsModule


def main():


	p = argparse.ArgumentParser(description='This script runs the static analyzer process per webpage.')
	p.add_argument('--from', "-f", type=str)
	p.add_argument('--to', "-t", type=str)
	p.add_argument('--memory', "-m", type=str, default='16000') # default: 16 GB
	p.add_argument('--timeout', "-e", type=str, default='7200') # default: 2 hours
	args= vars(p.parse_args())

	from_row = int(args["from"])
	to_row =  int(args["to"])
	memory = args["memory"]
	timeout = args["timeout"]
	LOGGER.info("testing range %d %d"%(from_row, to_row))

	BASE_DIR= os.path.dirname(os.path.realpath(__file__))
	DATA_DIR = os.path.join(BASE_DIR, "data")
	analyses_command_cwd = os.path.join(BASE_DIR, "analyses/domclobbering")
	
	# static analysis
	static_analysis_memory = memory
	static_analysis_timeout = int(timeout)

	static_analysis_command = "node --max-old-space-size=%s DRIVER_ENTRY --singlefolder=SINGLE_FOLDER"%static_analysis_memory
	node_static_analysis_driver_program = os.path.join(analyses_command_cwd, "static_analysis.js")
	static_analysis_command = static_analysis_command.replace("DRIVER_ENTRY", node_static_analysis_driver_program)
	



	testbed_filename = os.path.join(BASE_DIR, 'input/to-be-analyzed.csv')
	

	chunksize = 10**4
	iteration = 0
	done = False
	PRINT_ANALYZER_MESSAGES = False
	for chunk_df in pd.read_csv(testbed_filename, chunksize=chunksize, usecols=[0], header=None, skip_blank_lines=True):
		if done:
			break

		iteration = iteration + 1
		LOGGER.info("starting to test chunk: %s -- %s"%((iteration-1)*chunksize, iteration*chunksize))
		
		for (index, row) in chunk_df.iterrows():
			g_index = iteration*index+1
			if g_index >= from_row and g_index <= to_row:


				# website_folder_name = row[0]
				website_url = 'http://' + row[0]
				website_folder_name = website_url.replace(':', '-').replace('/', '')

				website_folder= os.path.join(DATA_DIR, website_folder_name)
				website_pages = os.listdir(website_folder)
				for webpage_name in website_pages:
					webpage_path_name = os.path.join(website_folder, webpage_name)
					if os.path.isdir(webpage_path_name):
						LOGGER.info("static analysis for site %s - webpage %s"%(website_folder_name, webpage_name)) 
						cmd = static_analysis_command.replace('SINGLE_FOLDER', webpage_path_name)
						IOModule.run_os_command(cmd, print_stdout=PRINT_ANALYZER_MESSAGES, cwd=analyses_command_cwd, timeout= static_analysis_timeout)
						LOGGER.info("successfully finished static analysis for site %s - webpage %s"%(website_folder_name, webpage_name)) 


			if g_index > to_row:
				done = True
				LOGGER.info("successfully tested sites, terminating!") 
				break

if __name__ == "__main__":
	main()


