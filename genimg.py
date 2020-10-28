#!/usr/bin/env python3

import cv2
import json
import time as t
import datetime as dt

with open('config.json') as f:
	config = json.load(f)

base = ''
camera = None

if config['os'] == 'win':
	base = config['win']
	camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
elif config['os'] == 'unix':
	base = config['unix']
	camera = cv2.VideoCapture(0)
else:
	print('ERR: Config os: ' + config['os'])

ext = config['ext']
folder = base + config['active']
img_counter = 1

while True:
	ret, frame = camera.read()
	now = dt.datetime.now()
	ts = now.strftime("%d%m%Y_%H%M%S")
	f1 = 'cam1_' + ts + '_{}.{}'.format(str(img_counter),ext)
	f2 = 'cam2_' + ts + '_{}.{}'.format(str(img_counter),ext)
	cv2.imwrite(folder + f1, frame)
	cv2.imwrite(folder + f2, frame)
	img_counter += 1
	print(f1,f2)
	t.sleep(5)

camera.release()