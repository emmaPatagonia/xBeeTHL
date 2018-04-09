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

import MySQLdb
import datetime
from obspy.core import read, UTCDateTime, Trace, Stream
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, num2date, DateFormatter
import matplotlib.animation as animation

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

host = "192.168.43.36"
user = "diego"
password = "None"
database = "test"


def ask_now(host, user, password, database, t1, t2, name):
  db = MySQLdb.connect(host=host,
                       user=user,   
                       passwd=password, 
                       db=database)

  cur = db.cursor()

  val1 = UTCDateTime(t1).strftime("%Y/%m/%d %H:%M:%S")
  val2 = UTCDateTime(t2).strftime("%Y/%m/%d %H:%M:%S")
  pattern = "select * from modulo where date between '%s' and '%s' and nombre='%s'" % (val1,val2, name)
  print( "[consulta] modulo", name, "leido entre ",val1,"y",val2 )

  cur.execute(pattern)
  res = cur.fetchall()
  print( "\n[info] largo total de la lectura =", len(res) ) 

  names = []
  H = []
  L = []
  date_vec = []
  for row in res:
    names.append(row[0])
    H.append(row[1])
    L.append(row[2])
    date_vec.append(row[3])

  cur.close()
  db.close()

  return date_vec, names, H, L



def convert_date_format(date_vec):
  ti = []
  for date in date_vec:
    pattern = "%s-%s-%sT%s:%s:%sZ" % ( date.split(' ')[0].split('/')[0], date.split(' ')[0].split('/')[1], date.split(' ')[0].split('/')[2], date.split(' ')[1].split(':')[0], date.split(' ')[1].split(':')[1], date.split(' ')[1].split(':')[2] )
    ti.append( date2num(UTCDateTime( pattern ).datetime) )

  dates = np.array(ti)

  return dates

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


fig = plt.figure()
ax1 = plt.subplot(211)
ax2 = plt.subplot(212)

def animate(i):
  name = "0013A20041646DE7"  # 0013A20041646DE7, 0013A2004127CAEF
  t1 = UTCDateTime(datetime.datetime.now()) - 60.*5
  t2 = UTCDateTime(datetime.datetime.now())
  date_vec, names, H, L = ask_now(host, user, password, database, t1, t2, name)
  dates = convert_date_format(date_vec)
  date_format = DateFormatter('%H:%M:%S')
  
  ax1.clear()
  ax2.clear()

  ax1.set_title("Modulo %s; last update: %s" % (name, t2.strftime("%Y/%m/%d %H:%M:%S")), y=1.0, fontsize=10)
  ax1.plot(dates,H,color='C0',label='humedad del suelo',lw=2.)
  ax1.legend()
  ax1.xaxis.set_major_formatter(date_format)
  ax1.minorticks_on()
  ax1.tick_params(axis='both', which='major', labelsize=8, bottom='on', top='off', left='on', right='off')
  ax1.tick_params(axis='both', which='minor', labelsize=6, bottom='on', top='off', left='on', right='off')
  ax1.set_ylim([0,100])
  ax1.set_ylabel("humedad (%)")
  ax1.set_xlim([date2num(t1.datetime),date2num(t2.datetime)])

  ax2.plot(dates,L,color='C1',label='luz ambiental',lw=2.)
  ax2.legend()
  ax2.xaxis.set_major_formatter(date_format)
  ax2.minorticks_on()
  ax2.tick_params(axis='both', which='major', labelsize=8, bottom='on', top='off', left='on', right='off')
  ax2.tick_params(axis='both', which='minor', labelsize=6, bottom='on', top='off', left='on', right='off')
  ax2.set_ylabel(r"resistencia ($\Omega$)")
  ax2.set_xlim([date2num(t1.datetime),date2num(t2.datetime)])


ani = animation.FuncAnimation(fig, animate, interval=int(1*1000))
plt.show(block=True)








