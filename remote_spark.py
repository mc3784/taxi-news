# $ pyspark --packages com.databricks:spark-csv_2.10:1.2.0

from pyspark.sql.functions import UserDefinedFunction as udf
from pyspark.sql.types import StringType
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark.sql.functions import *

from pyspark import SparkFiles
sc.addFile('/root/s3/PolygonConverted_NYC.csv')
sc.addPyFile('/root/s3/ray_casting.py')
sc.addPyFile('/root/s3/get_neb.py')

sqlContext = SQLContext(sc)

from get_neb import *
rows = []
loc = SparkFiles.get('PolygonConverted_NYC.csv')
with open(loc,'rU') as f:
    lines = f.readlines()
    for i in range(1,len(lines)):
        row = lines[i].strip().split(",")
        row[-2], row[-1] = float(row[-2]), float(row[-1])
        rows.append(row)

nebs = NebChecker(rows)

df = sqlContext.read.format('com.databricks.spark.csv').options(header='true').load('hdfs://ec2-54-187-241-63.us-west-2.compute.amazonaws.com:9010/data/yellow_tripdata_2010-01.csv')
df = (df.withColumn('pickup_datetime', df.pickup_datetime.cast('timestamp')).withColumn('dropoff_datetime', df.dropoff_datetime.cast('timestamp')))

neb = udf(nebs.get_neb,StringType())
df2 = df.withColumn("neb",neb(df.pickup_longitude,df.pickup_latitude))

df3 = df2.groupBy([dayofmonth(df2.tpep_pickup_datetime),df2.neb]).count().collect()

df3.write.format("com.databricks.spark.csv").option("header", "true").save("/root/s3/counts.csv")