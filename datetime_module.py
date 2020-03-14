#!/usr/bin/env python3
from math import exp,log,sqrt
import re
from datetime import date, time, datetime, timedelta

#date without time element
today = date.today()
print("today: {0!s}".format(today))
print('year:{0!s}'.format(today.year))
print("month:{0!s}".format(today.month))

#datetime
print("today datetime: {0!s}".format(datetime.today()))

#calculate a new date using timedelta
yesterday = today + timedelta(days=-1)
print("yesterday: {0!s}".format(yesterday))
one_hr = timedelta(hours=-1)
print('{0!s} {1!s}'.format(one_hr.days, one_hr.seconds))

#calculate the number of days (hrs mins secs) between two dates
datediff = today - yesterday
# the result datediff is a datetime object
print('{0!s}'.format(datediff))
print('{0!s}'.format(str(datediff).split()[0]))

# create a string with a specific format from a date object
print('{:s}'.format(today.strftime('%m/%d/%Y')))
print('{:s}'.format(today.strftime('%b %d, %Y')))
print('{:s}'.format(today.strftime('%Y-%m-%d')))
print('{:s}'.format(today.strftime('%B %d, %Y')))

# create a datetime object from a string with specific format
date1 = today.strftime('%m/%d/%Y')
date2 = today.strftime('%b %d, %Y')
date3 = today.strftime('%Y-%m-%d')
date4 = today.strftime('%B %d, %Y')

print('{!s}'.format(datetime.strptime(date1, '%m/%d/%Y')))
print('{!s}'.format(datetime.strptime(date2, '%b %d, %Y')))

# show date portion only
print('{!s}'.format(datetime.date(datetime.strptime(date3, '%Y-%m-%d'))))