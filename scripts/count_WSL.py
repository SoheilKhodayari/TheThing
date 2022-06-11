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
	WSL = Webpages Scripts LoC

	Counts the number of webpages per site, 
	the number of scripts per webpage, 
	and the LoC per webpage

"""

import json, os, sys
import hashlib


BASE_DIR= os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


sites = []
with open('./outputs/sitelist.out', 'r') as fd:
	lines = fd.readlines()
	for line in lines:
		sites.append(line.strip().rstrip('\n').strip())


sites_folder = []
with open('./outputs/sitelist_folder_names.out', 'r') as fd:
	lines = fd.readlines()
	for line in lines:
		sites_folder.append(line.strip().rstrip('\n').strip())



def get_scripts(directory):

	files = os.listdir(directory)
	outputs = []
	for file in files:
		if file.endswith('.js'):
			outputs.append(os.path.join(directory, file))

	return outputs

## see: https://stackoverflow.com/questions/9629179/python-counting-lines-in-a-huge-10gb-file-as-fast-as-possible
def blocks(files, size=65536):
	while True:
		b = files.read(size)
		if not b: break
		yield b


def get_webpage_loc_and_scripts(scripts):
	lines = 0
	scripts_count = 0
	# filter out empty scripts and those that contain a single character due to crawler/CDP error
	for script in scripts:
		with open(script, "r", encoding="utf-8", errors='ignore') as f:
			current_line = sum(bl.count("\n") for bl in blocks(f))
			lines += current_line
			if current_line <= 1:
				if len(str(f.readlines())) > 25:
					scripts_count+=1
			else:
				scripts_count+=1
	return lines, scripts_count


def sha256sum(filename):
	h  = hashlib.sha256()
	b  = bytearray(128*1024)
	mv = memoryview(b)
	with open(filename, 'rb', buffering=0) as f:
		for n in iter(lambda : f.readinto(mv), 0):
			h.update(mv[:n])
	return h.hexdigest()


with open('./outputs/webpages-scripts-loc-github.out', 'w+') as main_fd:
	for idx in range(len(sites_folder)):

		website = sites[idx]
		folder_name = sites_folder[idx]

		count_webpages = 0

		count_scripts = 0
		min_scripts = 0
		max_scripts = -1

		count_loc = 0
		min_loc = 0
		max_loc = -1

		script_hashs = []

		website_folder = os.path.join(DATA_DIR, folder_name)
		webpages = os.listdir(website_folder)
		for webpage_hash in webpages:
			webpage_folder = os.path.join(website_folder, webpage_hash)
			if os.path.exists(webpage_folder) and os.path.isdir(webpage_folder):
				count_webpages += 1

				current_scripts = get_scripts(webpage_folder)
				count_current_scripts = len(current_scripts)


				count_current_loc, count_current_scripts = get_webpage_loc_and_scripts(current_scripts)
				count_loc+=count_current_loc
				if count_current_loc < min_loc or min_loc == 0:
					min_loc = count_current_loc
				if count_current_loc > max_loc or max_loc == -1:
					max_loc = count_current_loc	


				count_scripts += count_current_scripts
				if count_current_scripts < min_scripts or min_scripts == 0:
					min_scripts = count_current_scripts
				if count_current_scripts > max_scripts or max_scripts == -1:
					max_scripts = count_current_scripts




				for s in current_scripts:
					digest = sha256sum(s)
					if digest not in script_hashs:
						script_hashs.append(digest)

		count_unique_scripts = len(script_hashs)
		avg_loc = count_loc / count_webpages
		avg_scripts = count_scripts / count_webpages

		writeme = "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
			website,
			count_webpages,
			min_scripts,
			avg_scripts,
			max_scripts,
			count_scripts,
			count_unique_scripts,
			min_loc,
			avg_loc,
			max_loc,
			count_loc
		)
		main_fd.write(writeme)


