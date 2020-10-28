#!/usr/bin/env python3

import re
import os
import sys
import time
import json
import shutil
import zipfile as zf
import datetime as dt

with open('config.json') as f:
	config = json.load(f)

base = config['win'] if config['os'] == 'win' else config['unix']
source = base + config['active']
dest = base + config['archive']
zips = base + config['zips']

mode = config['mode']

def zipyfy(filenames,suffix):
	zname = zips + 'archive_' + dt.datetime.now().strftime("%d%m%Y_") + suffix + '.zip'
	zfile = zf.ZipFile(zname, 'w')
	with zfile:
		for filename in os.listdir(dest):
			print('Zipping ' + filename)
			zfile.write('archive/' + filename)
			try:
				os.remove(dest + filename)
			except:
				print('ERROR: while removing ' + dest + filename)
	print('Done Zipping')

	if os.path.exists(zname):
		for filename in filenames:
			try:
				os.remove(source + filename)
			except:
				print('ERROR: while removing ' + source + filename)

def copyimg(pattern,suffix):
	filenames = []
	for filename in os.listdir(source):
		if bool(re.match(pattern,filename)):
			print('Copying ' + filename)
			shutil.copy(source + filename, dest)
			filenames.append(filename)
	print('Done Copying')
	time.sleep(1)
	zipyfy(filenames,suffix)

def genpattern(mode):
	minute = dt.datetime.now().strftime("%H%M")
	hour = dt.datetime.now().strftime("%H")

	if mode == 1:
		print('\nMinute Selected!\n')
		while True:
			if minute != dt.datetime.now().strftime("%H%M"):
				pattern = r'cam[12]_([0-9]){8}_' + minute + r'([0-9]){2}_\d+\.jpg'
				suffix = minute
				minute = dt.datetime.now().strftime("%H%M")
				copyimg(pattern,suffix)

	elif mode == 2:
		print('\nHour Selected!\n')
		while True:
			if hour != dt.datetime.now().strftime("%H"):
				pattern = r'cam[12]_([0-9]){8}_' + hour + r'([0-9]){4}_\d+\.jpg'
				suffix = hour
				hour = dt.datetime.now().strftime("%H")
				copyimg(pattern,suffix)

	else:
		print('\nExiting!\n')
		sys.exit()

genpattern(mode)