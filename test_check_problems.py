#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) Diego Gonzalez <diegogonzalezvidal@gmail.com>
#
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with This program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
import MySQLdb
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.dates import date2num, num2date, DateFormatter
from obspy.core import read, UTCDateTime, Trace, Stream
import time

import os, glob, itertools, shutil
from sys import path
path.append('src') # path to source folder of python functions
import imp

import asknow
imp.reload(asknow)
from asknow import asknow_humidity_fc28, asknow_photoresistor

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

host = "192.168.0.12"
user = "diego"
password = "None"
database = "test"

modname = "Exterior" # Indoor, Exterior

pause = 2
while 1 > 0:
  now = UTCDateTime(datetime.datetime.now())
  print("\n  [ %s ]Last update for module %s" % ( now.strftime("%Y/%m/%d %H:%M:%S"), modname ))

  # humidity threshold lower according to percentile 95
  humidity_threshold_1 = [20, 60*5.] # humidity in %, time in seconds

  t1 = now - humidity_threshold_1[1]
  t2 = now
  timeh, humidity, humidity_ohm = asknow_humidity_fc28(host, user, password, database, t1, t2, modname, verbose=False, doplot=False)

  per95 = np.percentile(humidity, 95)
  if per95<=humidity_threshold_1[0]:
    print("[status] checking humidity threshold 1: ALARM ACTIVATE (H=%.1f; thrhld=%.1f)" % (per95, humidity_threshold_1[0]) )
  else:
    print("[status] checking humidity threshold 1: NOTHING HAPPENS(H=%.1f; thrhld=%.1f)" % (per95, humidity_threshold_1[0]) )

  # lux threshold for night according to percentile 95
  lux_threshold_night = [10, 60*10.] # lux in lux, time in seconds

  t1 = now - lux_threshold_night[1]
  t2 = now
  timel, lux, lux_ohm = asknow_photoresistor(host, user, password, database, t1, t2, modname, verbose=False, doplot=False)

  per95 = np.percentile(lux, 95)
  if per95<=lux_threshold_night[0]:
    print("[status] checking lux threshold night: ALARM ACTIVATE (L=%.1f; thrhld=%.1f)" % (per95, lux_threshold_night[0]) )
  else:
    print("[status] checking lux threshold night: NOTHING HAPPENS (L=%.1f; thrhld=%.1f)" % (per95, lux_threshold_night[0]) )

  time.sleep(pause)

