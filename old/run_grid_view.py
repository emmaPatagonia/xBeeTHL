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
from matplotlib.mlab import griddata
import matplotlib as mpl
from matplotlib.colors import LogNorm

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

host = "192.168.0.12"
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

modules = [("0013A20041646DE7", 3, 0), ("0013A2004127CAEF", -4, -1)] #name, xpos, ypos
t1 = UTCDateTime(datetime.datetime.now()) - 60.*5
t2 = UTCDateTime(datetime.datetime.now())


fig = plt.figure()

ax1 = plt.subplot(211)
ax2 = plt.subplot(212)

soil_humidity = []
ambient_light = []
xaxis = []
yaxis = []
for mod in modules:
  name = mod[0]
  xpos = mod[1]
  ypos = mod[2]
  date_vec, names, H, L = ask_now(host, user, password, database, t1, t2, name)
  dates = convert_date_format(date_vec)
  soil_humidity.append(H[-1])
  ambient_light.append(L[-1])
  xaxis.append(xpos)
  yaxis.append(ypos)
  ax1.scatter(xpos,ypos,label=name,s=50,marker='s',zorder=1000)
  ax2.scatter(xpos,ypos,label=name,s=50,marker='s',zorder=1000)

soil_humidity.append(np.mean(soil_humidity))
ambient_light.append(np.mean(ambient_light))
xaxis.append(-2)
yaxis.append(1)


numcols, numrows = 200, 200
xi = np.linspace(np.min(xaxis), np.max(xaxis), numcols)
yi = np.linspace(np.min(yaxis), np.max(yaxis), numrows)
xi, yi = np.meshgrid(xi, yi)
zi_humidity = griddata(xaxis, yaxis, soil_humidity, xi, yi,interp="linear") # linear or nn
zi_light = griddata(xaxis, yaxis, ambient_light, xi, yi,interp="linear") # linear or nn

# add humedad del suelo
hmin = np.nanmin(zi_humidity) #60
hmax = np.nanmax(zi_humidity )#80
cmap = plt.cm.jet
nlevels = 10
bounds = np.linspace(hmin, hmax, nlevels, endpoint=True)
levels = np.linspace(hmin, hmax, nlevels, endpoint=True)
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
hgrid = ax1.contourf(xi, yi, zi_humidity.T, cmap=cmap, zorder=100, norm=norm, bounds=bounds, vmin=hmin, vmax=hmax)
cb1 = plt.colorbar(hgrid, format='%.1f', extend='neither', norm=norm, spacing='proportional', orientation='vertical', ticks = np.linspace(hmin, hmax, 6), ax=ax1) 
cb1.set_label('humedad del suelo (%)', size=10)
for j in cb1.ax.get_yticklabels(): j.set_fontsize(10)


# # add luz ambiental
lmin = np.nanmin(zi_light) #20
lmax = np.nanmax(zi_light) #200
cmap = plt.cm.hot_r
nlevels = 10
bounds = np.linspace(lmin, lmax, nlevels, endpoint=True)
levels = np.linspace(lmin, lmax, nlevels, endpoint=True)
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
hgrid = ax2.contourf(xi, yi, zi_light.T, cmap=cmap, zorder=100, norm=norm, bounds=bounds, vmin=lmin, vmax=lmax)
cb2 = plt.colorbar(hgrid, format='%.1f', extend='neither', norm=norm, spacing='proportional', orientation='vertical', ticks = np.linspace(lmin, lmax, 6), ax=ax2) 
cb2.set_label(r"luz ambiental ($\Omega$)", size=10)
for j in cb2.ax.get_yticklabels(): j.set_fontsize(10)




ax1.set_ylim([-3,3])
ax1.set_ylabel("y-axis")
ax1.set_xlim([-5,5])
ax1.set_xlabel("x-axis")
ax1.minorticks_on()
ax1.tick_params(axis='both', which='major', labelsize=8, bottom='on', top='off', left='on', right='off')
ax1.tick_params(axis='both', which='minor', labelsize=6, bottom='on', top='off', left='on', right='off')

ax2.set_ylim([-3,3])
ax2.set_ylabel("y-axis")
ax2.set_xlim([-5,5])
ax2.set_xlabel("x-axis")
ax2.minorticks_on()
ax2.tick_params(axis='both', which='major', labelsize=8, bottom='on', top='off', left='on', right='off')
ax2.tick_params(axis='both', which='minor', labelsize=6, bottom='on', top='off', left='on', right='off')

ax1.legend(fontsize=6)
ax1.set_title("last update: %s" % (t2.strftime("%Y/%m/%d %H:%M:%S")), y=1.0, fontsize=10)
ax2.legend(fontsize=6)
ax2.set_title("last update: %s" % (t2.strftime("%Y/%m/%d %H:%M:%S")), y=1.0, fontsize=10)

plt.subplots_adjust(wspace=0.6, hspace=0.5)
plt.show(block=False)





