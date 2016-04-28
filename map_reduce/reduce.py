#!/usr/bin/python

import sys

current_date_neb = None
current_count = 0
date_neb = None

for line in sys.stdin:
    line = line.strip()
    date_neb, count = line.split("\t",1)
    if current_date_neb == date_neb:
        current_count += 1
    else:
        if current_date_neb:
            print current_date_neb + "," + str(current_count)
        current_count = int(count)
        current_date_neb = date_neb

print current_date_neb + "," + str(current_count)