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
import numpy as np
import matplotlib.pyplot as plt
from obspy.core import read, UTCDateTime, Trace, Stream


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def convert_date_format(date_vec):
  ti = []
  for date in date_vec:
    pattern = "%s-%s-%sT%s:%s:%sZ" % ( date.split(' ')[0].split('/')[0], date.split(' ')[0].split('/')[1], date.split(' ')[0].split('/')[2], date.split(' ')[1].split(':')[0], date.split(' ')[1].split(':')[1], date.split(' ')[1].split(':')[2] )
    ti.append( UTCDateTime( pattern ).datetime )

  dates = np.array(ti)
  return dates




# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def asknow_humidity_fc28(host, user, password, database, t1, t2, modname, verbose=False, doplot=True):

  # connect to database
  db = MySQLdb.connect(host=host, user=user, passwd=password, db=database)
  cur = db.cursor()

  # ask to mysql database data desidered
  val1 = UTCDateTime(t1).strftime("%Y/%m/%d %H:%M:%S")
  val2 = UTCDateTime(t2).strftime("%Y/%m/%d %H:%M:%S")
  pattern = "select * from modulo where date between '%s' and '%s' and nombre='%s'" % (val1,val2, modname)
  cur.execute(pattern)
  res = cur.fetchall()
  if verbose:
    print( "[mysql] modulo", modname, "leido entre ",val1,"y",val2, "(", len(res), "puntos )" )

  # read variable from mySQL database. Choose correctly the columns of the database
  analog_output = []
  date_vec = []
  for row in res:
    analog_output.append(row[1])
    date_vec.append(row[3])

  humidity_ohm = np.array(analog_output)
  time = convert_date_format(date_vec)
  cur.close()
  db.close()

  # calibration ohm to percentage
  #                         min_humidity; max_humidity
  humidity_vector =        np.array([0,            100])
  humidity_in_ohm_vector = np.array([1024,  0])
  m, b = np.polyfit(humidity_in_ohm_vector, humidity_vector, 1)
  humidity = m*humidity_ohm + b

  # do plot
  if doplot:
    plt.subplot(211)
    plt.scatter(humidity_in_ohm_vector, humidity_vector)
    plt.plot( np.linspace(1,1024,100), np.linspace(1,1024,100)*m+b   )
    plt.ylabel('soil humidity (%)')
    plt.xlabel('resitence (ohm)')
    plt.title("humidity as a function of resistence")
    #plt.show(block=True)

    plt.subplot(212)
    plt.plot(time, humidity)
    plt.ylabel('humidity (%)')
    plt.xlabel('time')
    plt.title("humidity vs time")

    plt.subplots_adjust(hspace=0.5)
    plt.show(block=True)

  return time, humidity, humidity_ohm


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def asknow_photoresistor(host, user, password, database, t1, t2, modname, verbose=False, doplot=True):

  # connect to database
  db = MySQLdb.connect(host=host, user=user, passwd=password, db=database)
  cur = db.cursor()

  # ask to mysql database data desidered
  val1 = UTCDateTime(t1).strftime("%Y/%m/%d %H:%M:%S")
  val2 = UTCDateTime(t2).strftime("%Y/%m/%d %H:%M:%S")
  pattern = "select * from modulo where date between '%s' and '%s' and nombre='%s'" % (val1,val2, modname)
  cur.execute(pattern)
  res = cur.fetchall()
  if verbose:
    print( "[mysql] modulo", modname, "leido entre ",val1,"y",val2, "(", len(res), "puntos )" )

  # read variable from mySQL database. Choose correctly the columns of the database
  analog_output = []
  date_vec = []
  for row in res:
    analog_output.append(row[2])
    date_vec.append(row[3])

  lux_ohm = np.array(analog_output)
  time = convert_date_format(date_vec)
  cur.close()
  db.close()

  # calibration ohm to percentage 
  """
  #                    night; room night; not direct sun; direct sun;
  lux_vector =        [1,     100,        1000,           10000] 
  lux_in_ohm_vector = [1024,  400,        100,            10] 
  """
  #                    night; direct sun;
  lux_vector =        [1,     10000] 
  lux_in_ohm_vector = [1050,  10] 
  m, b = np.polyfit(np.log10(lux_in_ohm_vector), np.log10(lux_vector), 1)
  lux = lux_ohm**m * 10**b # log10(lux) = m x log10(R) + b

  # do plot
  if doplot:
    plt.subplot(211)
    plt.scatter(np.log10(lux_in_ohm_vector), np.log10(lux_vector))
    plt.plot( np.log10(np.linspace(1,1024,100)), np.log10(np.linspace(1,1024,100))*m + b  )
    plt.ylabel('log(ambient light) (lux)')
    plt.xlabel('log10(resitence) (ohm)')
    plt.title("lux as a function of resistence")
    #plt.show(block=True)

    plt.subplot(212)
    plt.plot(time, lux)
    plt.ylabel('ambient light (lux)')
    plt.xlabel('time')
    plt.title("lux vs time")
    #plt.ylim(lux_vector[0]/2., 2.*lux_vector[-1])
    plt.yscale('log')
    for known_lux in lux_vector:
      plt.axhline(known_lux, color='k', ls='--', alpha=.8)

    plt.subplots_adjust(hspace=0.5)
    plt.show(block=True)

  return time, lux, lux_ohm