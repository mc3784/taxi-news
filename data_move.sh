#!/bin/bash
# get taxi data and send it to s3
# to make this executable, type 'chmod +x name_of_file.sh'
# to run, type 'type sh ./name_of_file.sh'

for year in {2010..2015}
do
  for month in {1..12}
  do
    month=$(printf "%02d" $month)
    wget https://storage.googleapis.com/tlc-trip-data/$year/yellow_tripdata_$year-$month.csv
    aws s3 cp yellow_tripdata_$year-$month.csv s3://taxi-news
    rm yellow_tripdata_$year-$month.csv
  done
done
echo complete
