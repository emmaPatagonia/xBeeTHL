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
#
import MySQLdb
import datetime
from obspy.core import read, UTCDateTime, Trace, Stream
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, num2date, DateFormatter
import matplotlib.animation as animation

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


host = "201.239.95.50" # , 192.168.0.12, 201.239.95.50
user = "diego"
password = "None"
database = "test"


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# funcion que entra a la base de datos e imprime todas las columnas

def check_all_db(host, user, password, database):
  db = MySQLdb.connect(host=host,
                       user=user,   
                       passwd=password, 
                       db=database)
  cur = db.cursor()
  cur.execute("select * from modulo")
  res = cur.fetchall()
  count = 0
  allmodname = []
  for row in res:
    print( "[Nrow =", count, "]; ", list(row) )
    allmodname.append(row[0])
    count += 1

  print( "\n[info] largo total de la base de datos =", len(res) ) 

  return np.unique(np.array(allmodname))

allmodname = check_all_db(host, user, password, database)



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# funcion que consulta a la base de datos dentro de un rango de tiempo t1 y t2

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

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# funcion que obtiene fecha en formato number

def convert_date_format(date_vec):
  ti = []
  for date in date_vec:
    pattern = "%s-%s-%sT%s:%s:%sZ" % ( date.split(' ')[0].split('/')[0], date.split(' ')[0].split('/')[1], date.split(' ')[0].split('/')[2], date.split(' ')[1].split(':')[0], date.split(' ')[1].split(':')[1], date.split(' ')[1].split(':')[2] )
    ti.append( date2num(UTCDateTime( pattern ).datetime) )

  dates = np.array(ti)

  return dates


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# graficar la consulta ask_now

#name = "0013A2004127CAEF" # 0013A20041646DE7, 0013A2004127CAEF
count = 0
for modname in allmodname:
  print("[%i] module name = %s" % (count, modname))
  count+=1

ind = input("type the # for desired module name to plot: ")
name = allmodname[int(ind)]

timewindow =  86400.*5  # in seconds
t1 = UTCDateTime(datetime.datetime.now()) - timewindow
t2 = UTCDateTime(datetime.datetime.now())
date_vec, names, H, L = ask_now(host, user, password, database, t1, t2, name)

dates = convert_date_format(date_vec)
date_format = DateFormatter('%H:%M:%S')



fig = plt.figure()
ax1 = plt.subplot(211)
ax1.set_title("last update: %s" % (t2.strftime("%Y/%m/%d %H:%M:%S")), y=1.0, fontsize=10)
ax1.plot(dates,H,color='C0',label=name,lw=1., ls='--')
ax1.scatter(dates,H,color='C0',lw=.0, s=4)
ax1.legend()
ax1.xaxis.set_major_formatter(date_format)
ax1.minorticks_on()
ax1.tick_params(axis='both', which='major', labelsize=8, bottom='on', top='off', left='on', right='off')
ax1.tick_params(axis='both', which='minor', labelsize=6, bottom='on', top='off', left='on', right='off')
ax1.set_ylim([0,100])
ax1.set_ylabel("humedad del suelo (%)")
#ax1.set_xlim([dates[0],dates[-1]])
ax1.set_xlim([date2num(t1.datetime), date2num(t2.datetime)])

ax2 = plt.subplot(212)
ax2.plot(dates,L,color='C0',label=name,lw=1., ls='--')
ax2.scatter(dates,L,color='C0',lw=.0, s=4)
ax2.legend()
ax2.xaxis.set_major_formatter(date_format)
ax2.minorticks_on()
ax2.tick_params(axis='both', which='major', labelsize=8, bottom='on', top='off', left='on', right='off')
ax2.tick_params(axis='both', which='minor', labelsize=6, bottom='on', top='off', left='on', right='off')
ax2.set_ylabel(r"luz ambiental ($\Omega$)")
#ax2.set_xlim([dates[0],dates[-1]])
ax2.set_xlim([date2num(t1.datetime), date2num(t2.datetime)])
ax2.set_yscale('log')

plt.show(block=True)









