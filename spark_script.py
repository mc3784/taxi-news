# $ pyspark --packages com.databricks:spark-csv_2.10:1.2.0

from pyspark.sql.functions import UserDefinedFunction as udf
from pyspark.sql.types import StringType
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark.sql.functions import *

from pyspark import SparkFiles
sc.addFile('/Users/phil/taxi-news/PolygonConverted_NYC.csv')
sc.addPyFile('/Users/phil/taxi-news/ray_casting.py')
sc.addPyFile('/Users/phil/taxi-news/get_neb.py')

sqlContext = SQLContext(sc)

from get_neb import *
loc = SparkFiles.get('PolygonConverted_NYC.csv')
df = pd.DataFrame.from_csv(loc,index_col=False)
rows = df.as_matrix()
nebs = NebChecker(rows)
print nebs.get_neb('-73.97310741','40.72119878')

df = sqlContext.read.format('com.databricks.spark.csv').options(header='true').load('/Users/phil/Downloads/yellow_tripdata_2015-01.csv')
df = (df.withColumn('tpep_pickup_datetime', df.tpep_pickup_datetime.cast('timestamp')).withColumn('tpep_dropoff_datetime', df.tpep_dropoff_datetime.cast('timestamp')))

neb = udf(nebs.get_neb,StringType())
df2 = df.withColumn("neb",neb(df.pickup_longitude,df.pickup_latitude))

df2.groupBy([dayofmonth(df2.tpep_pickup_datetime),df2.neb]).count().show()