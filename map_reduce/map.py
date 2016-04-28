#!/usr/bin/python

import sys
import imp
# import get_neb

rows = []
loc = 'PolygonConverted_NYC.csv'
with open(loc,'rU') as f:
    lines = f.readlines()
    for i in range(1,len(lines)):
        row = lines[i].strip().split(",")
        row[-2], row[-1] = float(row[-2]), float(row[-1])
        rows.append(row)

get_neb = imp.load_source('get_neb', 'get_neb.py')
nebs = get_neb.NebChecker(rows)

for line in sys.stdin:
    line = line.strip()
    values = line.split(",")
    v_0 = values[0]
    if (v_0 <> 'VendorID' and v_0 <> 'vendor_id' and v_0 <> ''):
        print values[1].split(" ")[0] + "," + nebs.get_neb(values[5],values[6]) + "\t" + '1'
