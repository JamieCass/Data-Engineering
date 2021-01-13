########################## Data wrangling Quiz ##########################

# TODOS: 
# 1) import any other libraries you might need
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
import matplotlib.pyplot as plt

# 2) instantiate a Spark session 
spark = SparkSession \
    .builder \
    .appName('Wrangling quiz') \
    .getOrCreate()

# 3) read in the data set located at the path "data/sparkify_log_small.json"
path = 'sparkify_log_small.json'
user_log = spark.read.json(path)


########################## Question 1 ##########################
# Which page did user id '' NOT visit?
user_log.select('page').dropDuplicates().show()
user_log.printSchema()
user_log.take(1)

# TODO: write your code to answer question 1
empty_user = user_log.filter(user_log.userId == '') \
    .select('page') \
    .alias('blank_pages')\
    .dropDuplicates()
all_pages = user_log.select('page').dropDuplicates()

print('Pages not visited:')
for row in set(all_pages.collect()) - set(empty_user.collect()):
    print(row.page)
   
print('\nPages visited:')
for row in set(empty_user.collect()):
    print(row.page)


########################## Question 2 ##########################
# What type of user does the empty string user id most likely refer to?
# TODO: use this space to explore the behavior of the user with an empty string
print('Someone without an account, they dont have access to anything such as settings or anything a member (free/paid) would, they havent even logged in. They would need to log in to acces anything like that.')


########################## Question 3 ##########################
# How many users are female?
# TODO: write your code to answer question 3
user_log.filter(user_log.gender == 'F') \
    .select('userId', 'gender') \
    .dropDuplicates() \
    .count()


########################## Question 4 ##########################
# How many songs were played from the most played artist?
# TODO: write your code to answer question 4
user_log.filter(user_log.page == 'NextSong') \
    .select('Artist') \
    .groupBy('Artist') \
    .agg({'Artist' : 'count'}) \
    .sort(desc('count(Artist)')) \
    .withColumnRenamed('count(Artist)', 'Play_count') \
    .show(1)


########################## Question 5 (challenge) ##########################
# How many songs do users listen to on average between visint our home page? Round to closest integer
function = udf(lambda ishome : int(ishome == 'Home'), IntegerType())

user_window = Window \
    .partitionBy('userID') \
    .orderBy(desc('ts')) \
    .rangeBetween(Window.unboundedPreceding, 0)

cusum = user_log.filter((user_log.page == 'NextSong') | (user_log.page == 'Home')) \
    .select('userID', 'page', 'ts') \
    .withColumn('homevisit', function('page')) \
    .withColumn('period', Fsum('homevisit').over(user_window))

cusum.filter((cusum.page == 'NextSong')) \
    .groupBy('userID', 'period') \
    .agg({'period':'count'}) \
    .agg({'count(period)':'avg'}).show()









