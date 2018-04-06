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

fig = plt.figure()
ax1 = plt.subplot(211)
ax2 = plt.subplot(212)

def animate(i):
  ax1.clear()
  ax2.clear()
  date_format = DateFormatter('%H:%M:%S')

  host = "192.168.0.12"
  user = "diego"
  password = "soy un aguila"
  database = "test"

  t1 = UTCDateTime(datetime.datetime.now()) - 60.*5
  t2 = UTCDateTime(datetime.datetime.now())

  modules = ["Indoor", "Exterior"]
  for modname in modules:

    timeh, humidity, humidity_ohm = asknow_humidity_fc28(host, user, password, database, t1, t2, modname, verbose=True, doplot=False)
    if len(humidity)>0:
      ax1.plot(timeh, humidity, label="%s (%.1f %%)"%(modname, humidity[-1]),lw=0.8, ls='--')
      ax1.scatter(timeh, humidity, lw=.0, s=5)

    ax1.xaxis.set_major_formatter(date_format)
    ax1.minorticks_on()
    ax1.tick_params(axis='both', which='major', labelsize=8, bottom='on', top='off', left='on', right='off')
    ax1.tick_params(axis='both', which='minor', labelsize=6, bottom='on', top='off', left='on', right='off')
    ax1.set_ylim([0,100])
    ax1.set_ylabel("humedad de suelo (%)")
    ax1.set_xlim([date2num(t1.datetime),date2num(t2.datetime)])
    ax1.axhline(70, lw=.8, ls='--', color="C2")

    timel, lux, lux_ohm = asknow_photoresistor(host, user, password, database, t1, t2, modname, verbose=True, doplot=False)
    if len(lux)>0:
      ax2.plot(timel, lux, label="%s (%i lux)"%(modname, lux[-1]),lw=0.8, ls='--')
      ax2.scatter(timel, lux, lw=.0, s=5)

    ax2.set_ylabel("luz ambiental (lux)")
    ax2.xaxis.set_major_formatter(date_format)
    ax2.minorticks_on()
    ax2.tick_params(axis='both', which='major', labelsize=8, bottom='on', top='off', left='on', right='off')
    ax2.tick_params(axis='both', which='minor', labelsize=6, bottom='on', top='off', left='on', right='off')
    ax2.set_ylim([1,100000])
    ax2.set_xlim([date2num(t1.datetime),date2num(t2.datetime)])
    ax2.set_yscale('log')
    ax2.axhline(1000, lw=.8, ls='--', color="C2")
    #ax2.axhline(1000, lw=.8, ls='--', color="gold")
    #ax2.axhline(10, lw=.8, ls='--', color="C3")

  ax1.legend(fontsize=8)
  ax2.legend(fontsize=8)
  ax1.set_title("last update: %s" % (t2.strftime("%Y/%m/%d %H:%M:%S")), y=1.0, fontsize=10)

ani = animation.FuncAnimation(fig, animate, interval=int(1*1000))
plt.show(block=True)




