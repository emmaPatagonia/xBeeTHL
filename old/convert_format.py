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
from obspy.core import read, UTCDateTime, Trace, Stream
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, num2date, DateFormatter
import matplotlib.animation as animation

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def convert_date_format(date_vec):
  ti = []
  for date in date_vec:
    pattern = "%s-%s-%sT%s:%s:%sZ" % ( date.split(' ')[0].split('/')[0], date.split(' ')[0].split('/')[1], date.split(' ')[0].split('/')[2], date.split(' ')[1].split(':')[0], date.split(' ')[1].split(':')[1], date.split(' ')[1].split(':')[2] )
    ti.append( date2num(UTCDateTime( pattern ).datetime) )

  dates = np.array(ti)

  return dates

