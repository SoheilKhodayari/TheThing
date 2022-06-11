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
	Counts the number of webpages per site

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

with open('./outputs/webpages.out', 'w+') as main_fd:
	for idx in range(len(sites_folder)):

		website = sites[idx]
		folder_name = sites_folder[idx]

		count_webpages = 0

		website_folder = os.path.join(DATA_DIR, folder_name)
		webpages = os.listdir(website_folder)
		for webpage_hash in webpages:
			webpage_folder = os.path.join(website_folder, webpage_hash)
			if os.path.exists(webpage_folder) and os.path.isdir(webpage_folder):
				count_webpages += 1
		writeme = "{}\t{}\n".format(
			website,
			count_webpages
		)
		main_fd.write(writeme)


