#! /usr/bin/env python
# This file takes in a csv file from smartmetertexas.com
# and produces csv files with various statistics (Daily, Hourly, etc...)

import csv
import time
import calendar

# Read log file
# Format is: ESIID,USAGE_DATE,USAGE_START_TIME,USAGE_END_TIME,USAGE_KWH,ESTIMATED_ACTUAL
meterlog = csv.reader( open( 'log.csv', 'rb') )

first_row = 0

# Initialize dictionaries
daily_usage={}
weekday_usage={}
hourly_usage={}

for row in meterlog:
  # Skip the first row with the column titles
  if first_row:
     
    #print calendar.timegm(time.strptime( (row[1] + row[2]), "%Y-%m-%d %H:%M")) , ' ', row[4]
    
    # Add up the power used each day
    daily_usage[row[1]] = daily_usage.get(row[1],0) + float(row[4])
    
    # Add up the power used each weekday
    weekday = time.strftime("%a", time.strptime( (row[1] + row[2]), "%Y-%m-%d %H:%M"))
    weekday_usage[weekday] = weekday_usage.get(weekday,0) + float(row[4])
    
    # Add up the power used each 15 minute interval (all days)
    hourly_usage[row[2]] = hourly_usage.get(row[2],0) + float(row[4])
  
  # We're not in the first row anymore!
  first_row = 1;


# open daily csv file
dayfile = open('daily.csv', 'w')

# First row
dayfile.write('Date, Usage (kWh)\n')
for day, kwh in sorted(daily_usage.iteritems()):
  dayfile.write(day + ',' + str(kwh) + '\n')

  
# open weekday csv file
weekdayfile = open('weekday.csv', 'w')

# First row
weekdayfile.write('Day, Usage (kWh)\n')

# Instead of figuring out a way to sort by day, just print manually...
weekdayfile.write('Mon,' + str(weekday_usage['Mon']) + '\n')
weekdayfile.write('Tue,' + str(weekday_usage['Tue']) + '\n')
weekdayfile.write('Wed,' + str(weekday_usage['Wed']) + '\n')
weekdayfile.write('Thu,' + str(weekday_usage['Thu']) + '\n')
weekdayfile.write('Fri,' + str(weekday_usage['Fri']) + '\n')
weekdayfile.write('Sat,' + str(weekday_usage['Sat']) + '\n')
weekdayfile.write('Sun,' + str(weekday_usage['Sun']) + '\n')
  

# open hourly csv file
hourfile = open('hourly.csv', 'w')

# First row
hourfile.write('Time, Usage (kWh)\n')
for hour, kwh in sorted(hourly_usage.iteritems()):
  hourfile.write(hour + ',' + str(kwh) + '\n')
