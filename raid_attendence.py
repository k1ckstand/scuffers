#!/usr/bin/env python3

import calendar
from datetime import date

RAID_DAYS = ['Wednesday', 'Thursday']
found_dates = list()

d = date.today()
j = d.toordinal()

while len(found_dates) != len(RAID_DAYS):
    j += 1
    d = date.fromordinal(j)
    x = calendar.day_name[d.weekday()]
    if x in RAID_DAYS:
        found_dates.append(d)

for d in found_dates:
    print(f'Raid night: {d.strftime("%A %B %d")}')
