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
	check the state of the analysis

	Run:
	------------
	python3 stat.py

"""

import json, os, sys

BASE_DIR= os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

webapps_list = os.listdir(DATA_DIR)

total_webpages = 0 # total count
sites = set()
total_webpages_with_data = 0
total_webpages_finished_analysis = 0 # count finished


top_n = 5000

ranking = {}
with open('./../input/ranking_folder.out', 'r') as fd:
	ranking = json.load(fd)

not_analyzed = []

for webapp_folder_name in webapps_list:
	not_analyzed_flag = True
	has_data = False
	if webapp_folder_name in ranking and ranking[webapp_folder_name] <= top_n:
		webapp_folder = os.path.join(DATA_DIR, webapp_folder_name)
		if os.path.exists(webapp_folder) and os.path.isdir(webapp_folder):
			webpages = os.listdir(webapp_folder)
			for webpage_hash in webpages:
				webpage_folder = os.path.join(webapp_folder, webpage_hash)
				if os.path.exists(webpage_folder) and os.path.isdir(webpage_folder):
					total_webpages+=1
					if len(os.listdir(webpage_folder)) > 0 and os.path.exists(os.path.join(webpage_folder, "0.js")):
						total_webpages_with_data+=1
						has_data = True
					# check if `time.static_analysis.out` exists
					# if that is the case, then the static analysis has successsfully finished for that webpage
					f= os.path.join(webpage_folder, "time.static_analysis.out")
					if os.path.exists(f):
						total_webpages_finished_analysis+=1
						sites.add(webapp_folder_name)
						not_analyzed_flag = False

	if not_analyzed_flag and has_data:
		not_analyzed.append(webapp_folder_name)


print("total sites having data and analyzed (from %s): "%(top_n) + str(len(list(sites))))
print("total webpage: "+ str(total_webpages))
print("total webpage with data: "+ str(total_webpages_with_data))
print("total webpages analyzed: "+ str(total_webpages_finished_analysis))
print(not_analyzed)
