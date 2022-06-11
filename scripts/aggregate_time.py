# -*- coding: utf-8 -*-

"""
	Name: count_WSL = Webpages Scripts LoC

	Counts the number of webpages per site, 
	the number of scripts per webpage, 
	and the LoC per webpage
"""
import json, os, sys
import hashlib
import time as timeModule


BASE_DIR= os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

TIME_AGG_FILE_NAME = './outputs/aggregated_time.out'

def collect_all_processing_times_into_one_file():

	sites = []
	with open('./../input/top5k.out', 'r') as fd:
		lines = fd.readlines()
		for line in lines:
			sites.append(line.strip().rstrip('\n').strip())


	data_dict = {}

	with open(TIME_AGG_FILE_NAME, 'w+') as main_fd:
		for idx in range(len(sites)):

			website = sites[idx]
			folder_name = 'http-' + website

			website_folder = os.path.join(DATA_DIR, folder_name)

			crawling_time = -1 
			crawling_time_file_name = os.path.join(website_folder, "time.crawling.out")
			if os.path.exists(crawling_time_file_name):
				fd = open(crawling_time_file_name, "r")
				json_data = json.load(fd)
				fd.close()
				crawling_time = json_data["crawling_time"].strip().rstrip('\n').strip()


			webpage_times = {
				"crawling_time": crawling_time,
				"total_static_timer": [],
				"csv_hpg_construction_timer": [],
				"in_memory_hpg_construction_timer": [],
				"source_detection_timer": [],
				"sink_detection_timer": []
			}
			webpages = os.listdir(website_folder)
			for webpage_hash in webpages:
				webpage_folder = os.path.join(website_folder, webpage_hash)
				if os.path.exists(webpage_folder) and os.path.isdir(webpage_folder):
					static_analysis_time_file_name = os.path.join(webpage_folder, "time.static_analysis.out")
					if os.path.exists(static_analysis_time_file_name):
						fd = open(static_analysis_time_file_name, "r")
						json_data = json.load(fd)
						fd.close()

						if "total_static_timer" in json_data:
							t1 = json_data["total_static_timer"].strip().rstrip('\n').strip()
							webpage_times["total_static_timer"].append(t1)

						if "csv_hpg_construction_timer" in json_data:
							t2 = json_data["csv_hpg_construction_timer"].strip().rstrip('\n').strip()
							webpage_times["csv_hpg_construction_timer"].append(t2)

						if "in_memory_hpg_construction_timer" in json_data:
							t3 = json_data["in_memory_hpg_construction_timer"].strip().rstrip('\n').strip()
							webpage_times["in_memory_hpg_construction_timer"].append(t3)

						if "source_detection_timer" in json_data:
							t4 = json_data["source_detection_timer"].strip().rstrip('\n').strip()
							webpage_times["source_detection_timer"].append(t4)

						if "sink_detection_timer" in json_data:
							t5 = json_data["sink_detection_timer"].strip().rstrip('\n').strip()
							webpage_times["sink_detection_timer"].append(t5)


			data_dict[website] = webpage_times

		json.dump(data_dict, main_fd)


### --------------------------------
def get_elapsed_time_in_ms(time_str):

	if time_str == '' or time_str == '-1' or time_str == -1:
		return 0

	# example: 1 hours 8 minutes 56.72 seconds
	# 1 hours 56.72 seconds
	# 1 hours
	if 'hours' in time_str:
		parts = time_str.split(' ')
		hrs = float(parts[0])
		secs= 0
		mins = 0
		if 'minutes' in time_str:
			mins = float(parts[2])

		if 'seconds' in time_str:
			if 'minutes' in time_str:
				secs = float(parts[4])
			else:
				secs = float(parts[2])
		time_ms = (hrs*3600 + mins*60 + secs)*1000
		return time_ms


	# example: 8 minutes 56.72 seconds
	elif 'minutes' in time_str:
		parts = time_str.split(' ')
		mins = float(parts[0])
		secs = 0
		if 'seconds' in time_str:
			secs = float(parts[2])
		time_ms = (mins*60 + secs)*1000
		return time_ms
	# example: 56.72 seconds
	elif 'seconds' in time_str:
		time = time_str.replace('seconds', '').replace(' ', '')
		time_ms = float(time) * 1000
		return time_ms
	# example: 11ms
	else:
		time_str = time_str.replace('ms', '').replace(' ', '')
		time_ms = float(time_str)
			
		return time_ms


def process_collected_time():

	sites = []
	with open('./../input/top5k.out', 'r') as fd:
		lines = fd.readlines()
		for line in lines:
			sites.append(line.strip().rstrip('\n').strip())


	with open('./outputs/processing_time.out', 'w+') as main_fd:
		with open(TIME_AGG_FILE_NAME, 'r') as fd:
			json_data = json.load(fd)
			for site in sites:
				current_record = json_data[site]

				crawling_time = current_record["crawling_time"]
				crawling_time_ms = get_elapsed_time_in_ms(crawling_time)

				lst_total_static_times = current_record["total_static_timer"]
				lst_total_static_times_ms = []
				for t in lst_total_static_times:
					t_ms = get_elapsed_time_in_ms(t)
					lst_total_static_times_ms.append(t_ms)
				##
				sum_total_static_times_ms = sum(lst_total_static_times_ms)
				divided_by = len(lst_total_static_times_ms)
				if divided_by == 0:
					avg_total_static_times_ms = 0
				else:
					avg_total_static_times_ms = sum_total_static_times_ms / len(lst_total_static_times_ms)
				

				lst_csv_hpg_construction_times = current_record["csv_hpg_construction_timer"]
				lst_csv_hpg_construction_times_ms = []
				for t in lst_csv_hpg_construction_times:
					t_ms = get_elapsed_time_in_ms(t)
					lst_csv_hpg_construction_times_ms.append(t_ms)

				lst_in_memory_hpg_construction_times = current_record["in_memory_hpg_construction_timer"]
				lst_in_memory_hpg_construction_times_ms = []
				for t in lst_in_memory_hpg_construction_times:
					t_ms = get_elapsed_time_in_ms(t)
					lst_in_memory_hpg_construction_times_ms.append(t_ms)
				##
				sum_hpg_construction_times_ms = sum(lst_csv_hpg_construction_times_ms) + sum(lst_in_memory_hpg_construction_times_ms)
				divided_by = max(len(lst_csv_hpg_construction_times_ms),len(lst_in_memory_hpg_construction_times_ms))
				if divided_by == 0:
					avg_hpg_construction_times_ms = 0
				else:
					avg_hpg_construction_times_ms = sum_hpg_construction_times_ms / divided_by


				lst_source_det_timer = current_record["source_detection_timer"]
				lst_source_det_timer_ms = []
				for t in lst_source_det_timer:
					t_ms = get_elapsed_time_in_ms(t)
					lst_source_det_timer_ms.append(t_ms)
				##
				sum_source_det_timer_ms = sum(lst_source_det_timer_ms)
				divided_by = len(lst_source_det_timer_ms)
				if divided_by == 0:
					avg_source_det_timer_ms = 0
				else:
					avg_source_det_timer_ms = sum_source_det_timer_ms / len(lst_source_det_timer_ms)
				


				lst_sink_det_timer = current_record["sink_detection_timer"]
				lst_sink_det_timer_ms = []
				for t in lst_sink_det_timer:
					t_ms = get_elapsed_time_in_ms(t)
					lst_sink_det_timer_ms.append(t_ms)
				##
				sum_sink_det_timer_ms = sum(lst_sink_det_timer_ms)
				divided_by = len(lst_sink_det_timer_ms)
				if divided_by == 0:
					avg_sink_det_timer_ms = 0
				else:
					avg_sink_det_timer_ms = sum_sink_det_timer_ms / len(lst_sink_det_timer_ms)
				


				writeme="{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
					crawling_time_ms,
					avg_hpg_construction_times_ms,
					sum_hpg_construction_times_ms,
					avg_source_det_timer_ms,
					sum_source_det_timer_ms,
					avg_sink_det_timer_ms,
					sum_sink_det_timer_ms,
					avg_total_static_times_ms,
					sum_total_static_times_ms,
				)
				main_fd.write(writeme)


if __name__ == "__main__":
	
	recollect = False
	## step 1: create aggregated_time.out
	if recollect or not os.path.exists(TIME_AGG_FILE_NAME):
		collect_all_processing_times_into_one_file()
	else:
		process_collected_time()



