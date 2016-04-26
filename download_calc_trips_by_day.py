import os
import sys
import urllib
import pandas as pd

df_list = []

for year in range(2010,2011):
    for month in range(2,3):
        try:
            month = ("%02d" % (month))
            url = 'https://storage.googleapis.com/tlc-trip-data/' \
                  + str(year) + '/yellow_tripdata_' + str(year)   \
                  + '-' + month + '.csv'
            saved_as = str(year) + '-' + month + '.csv'
            urllib.urlretrieve (url, saved_as)
            df = pd.read_csv(saved_as,index_col=False,error_bad_lines=False)
            pickup_datetime_col = list(df.columns.values)[1]
            date = pd.to_datetime(df[pickup_datetime_col])
            date = date.map(pd.Timestamp.date)
            df = date.value_counts(sort=False)
            df = df.to_frame()
            df.columns = ['count']
            df_list.append(df)
            os.remove(saved_as)
        except:
            print 'failed to download', month, str(year)

final = pd.concat(df_list)
final.to_csv("daily_trip_totals.csv")