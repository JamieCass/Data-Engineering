from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
from pyspark.sql.types import IntegerType
from pyspark.sql.functions import desc
from pyspark.sql.functions import asc
from pyspark.sql.functions import sum as Fsum
from pyspark.sql import Window
import datetime
import numpy as np
import pandas as pd
%matplotlib inline
import matplotlib.pyplot as plt


############################################################
# Instantiate a SparkSession
############################################################
spark = SparkSession \
    .builder \
    .appName("Wrangling Data") \
    .getOrCreate()
path = "/sparkify_log_small.json"
user_log = spark.read.json(path)


############################################################
# Explore the dataset
############################################################
user_log.take(5) # the top 5 rows

user_log.printSchema() # the schema

user_log.describe.show() # the count/summary of everything

user_log.describe('artist').show() # the count/summary of just artist

user_log.describe('sessionId').show() # the count/summary of sessionId

user_log.count() # count how many rows in the dataset

user_log.select('page').dropDuplicates().sort('page').show() # distinct page names

user_log.select(['userId', 'firstname', 'page', 'song']).where(userId == '1046').collect() # userID, firstname, etc.. of just user 1046


############################################################
# Calculating statistics by Hour
############################################################
get_hour = udf(lambda x: datetime.datetime.fromtimestamp(x / 1000.0).hour) # UDF function to calculate what hour in the timestamp songs are listened to

user_log = user_log.withColumn('hour', get_hour(user_log.ts)) # create new column hour

songs_in_hour = user_log.filter(user_log.page == 'NextSong').groupby(user_log.hour.cast('float'))

songs_in_hour.show() # count of how many NextSongs where played in what hour

songs_in_hour_pd = songs_in_hour.toPandas()
songs_in_hour_pd.hour = pd.to_numeric(songs_in_hour_pd.hour)

# plot into a scatterr graph
plt.scatter(songs_in_hour_pd['hour'], songs_in_hour_pd['count'])
plt.xlim(-1, 24);
plt.ylim(0, 1.2 * max(songs_in_hour_pd['count']))
plt.xlabel('Hour')
plt.ylabel('Songs Played')


############################################################ 
# Drop rows with duplicates
############################################################
# There are no missing values in userId or session columns, but there are userId values that are empty strings
user_log_valid = user_log.dropna(how = 'any', subset = ['userId', 'sessionId'])

user_log_valid.count() # see how many rows user_log_valid has in it

user_lod.select('userId').dropDuplicates().sort('userId').show() # all distinct userId's (we can see the first one doesnt have anything in)

user_log_valid = user_log_valid.filter(user_log_valid['userId'] != '') # filter out any userId's that = an empty string

user_log_valid.count() # you will see there are less that 10000


############################################################
# Users douwngrade their account
############################################################
# Find when users downgraded their accounts and flag the entries. The use a window funnction and cumulative sum to see each users data as either pre or post dongrade events
user_log_valid.filter("page = 'Submit Downgrade").show() # the user that has a downgrade submitted

user_log.select(["userId", "firstname", "page", "level", "song"]).where(user_log.userId == "1138").collect() # show more details of the specific user above

flag_downgrade_event = udf(lambda x: 1 if x == "Submit Downgrade" else 0, IntegerType()) # if downgraded there will be a 1 if not a 0

user_log_valid = user_log_valid.withColumn("downgraded", flag_downgrade_event("page")) # make a new column that will show 1/0 if a user has downgraded

user_log_valid.head() # check to see if the column is added

# not sure on this bit, will have to see what its about...
windowval = Window.partitionBy("userId").orderBy(desc("ts")).rangeBetween(Window.unboundedPreceding, 0) 

user_log_valid = user_log_valid.withColumn("phase", Fsum("downgraded").over(windowval))

user_log_valid.select(["userId", "firstname", "ts", "page", "level", "phase"]).where(user_log.userId == "1138").sort("ts").collect()






