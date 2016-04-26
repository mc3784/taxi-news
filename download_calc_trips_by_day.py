import os
import sys
import urllib
import pandas as pd

for year in range(2010,2016):
    for month in range(1,13):
        month = ("%02d" % (month))
        url = 'https://storage.googleapis.com/tlc-trip-data/' \
              + str(year) + '/yellow_tripdata_' + str(year)   \
              + '-' + month + '.csv'
        saved_as = str(year) + '-' + month + '.csv'
        urllib.urlretrieve (url, saved_as)      
        df = pd.DataFrame.from_csv(saved_as,index_col=False)
        pickup_datetime_col = list(df.columns.values)[1]
        date = pd.to_datetime(df[pickup_datetime_col])
        date = date.map(pd.Timestamp.date)
        df = date.value_counts(sort=False)
        df = df.to_frame()
        df.columns = ['count']
        os.remove(saved_as)
        df.to_csv(saved_as)