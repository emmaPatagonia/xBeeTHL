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
password = "soy un aguila"
database = "test"

modname = "Indoor" # Indoor, Exterior

timewindow = 60.*60 * 24
t1 = UTCDateTime(datetime.datetime.now()) - timewindow
t2 = UTCDateTime(datetime.datetime.now())

timeh, humidity, humidity_ohm = asknow_humidity_fc28(host, user, password, database, t1, t2, modname, verbose=True, doplot=True)
timel, lux, lux_ohm = asknow_photoresistor(host, user, password, database, t1, t2, modname, verbose=True, doplot=True)


