# -*- coding: utf-8 -*-

""" 
	gets the top 5000 analyzed site folder names in the data directory 
"""



import json, os, sys

BASE_DIR= os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

ordered_sites = []
with open('./../input/tranco_Y3JG_unique.csv', 'r') as fd:
	lines = fd.readlines()
	for line in lines:
		website = line.split(',')[1].strip().rstrip('\n').strip()
		website_url = 'http://' + website
		website_folder_name = website_url.replace(':', '-').replace('/', '')
		ordered_sites.append([website,website_folder_name])


output = [] 
sites_count = 0
for website_entry in ordered_sites:
	add_site = False
	website_folder_name = website_entry[1]
	website_folder = os.path.join(DATA_DIR, website_folder_name)
	if os.path.exists(website_folder) and os.path.isdir(website_folder):
		webpages = os.listdir(website_folder)
		for webpage_hash in webpages:
			webpage_folder = os.path.join(website_folder, webpage_hash)
			if os.path.exists(webpage_folder) and os.path.isdir(webpage_folder):
				if os.path.exists(os.path.join(webpage_folder, "0.js")):
					# check if `time.static_analysis.out` exists
					# if that is the case, then the static analysis has finished for that webpage
					f= os.path.join(webpage_folder, "time.static_analysis.out")
					if os.path.exists(f):
						add_site = True
						continue

	if add_site:
		output.append(website_entry)
		sites_count+=1

	if sites_count >= 5500:
		break

with open('./outputs/sitelist.out', 'w+') as fd:
	for entry in output:
		fd.write(entry[0] + '\n')

with open('./outputs/sitelist_folder_names.out', 'w+') as fd:
	for entry in output:
		fd.write(entry[1] + '\n')

