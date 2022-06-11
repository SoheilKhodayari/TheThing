"""
	Creates a mapping for output folder names of the crawler to a given top-site list rank
"""



import pandas as pd
import os, sys, json



def main():

	input_testbed_filename = 'tranco_Y3JG_unique.csv'
	
	results = {}
	from_row = 1
	to_row = 6500

	chunksize = 10**4
	iteration = 0
	done = False
	for chunk_df in pd.read_csv(input_testbed_filename, chunksize=chunksize, usecols=[0, 1], header=None, skip_blank_lines=True):
		if done:
			break

		iteration = iteration + 1
		
		for (index, row) in chunk_df.iterrows():
			g_index = iteration*index+1
			if g_index >= from_row and g_index <= to_row:

				website_rank = row[0]
				website_url = 'http-' + row[1]
				results[website_url] = website_rank

			if g_index > to_row:
				done = True
				LOGGER.info("successfully tested sites, terminating!") 
				break


	with open('ranking_folder.out', 'w+') as fd:
		json.dump(results, fd)


if __name__ == '__main__':
	main()