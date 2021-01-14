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

# 4) create a view to use with your SQL queries
user_log.createOrReplaceTempView("sql_table")


########################## Question 1 ##########################
# Which page did user id '' NOT visit?
user_log.printSchema()

# TODO: write your code to answer question 1
spark.sql('''
        SELECT *
        FROM(
            SELECT DISTINCT page
            FROM sql_table
            WHERE userId = "") AS pages_visited
        RIGHT JOIN (
            SELECT DISTINCT page
            FROM sql_table) AS all_pages
        ON pages_visited.page = all_pages.page
        WHERE pages_visited.page is NULL
        ORDER BY 2
        ''').show()


########################## Question 2 ##########################
# What type of user does the empty string user id most likely refer to?
# TODO: use this space to explore the behavior of the user with an empty string
print('Some people might prefer to writes SQL queries over using Pandas to get their results.')

########################## Question 3 ##########################
# How many users are female?
# TODO: write your code to answer question 3
spark.sql('''
        SELECT COUNT(DISTINCT userId)
        FROM sql_table
        WHERE gender = 'F'
        ''').show()


########################## Question 4 ##########################
# How many songs were played from the most played artist?
# TODO: write your code to answer question 4
spark.sql('''
        SELECT Artist, COUNT(Artist)
        FROM sql_table
        GROUP BY 1
        ORDER BY 2 DESC
        LIMIT 1''').show()

# ------------ OR ------------
# Get the artist play counts
play_counts = spark.sql("SELECT Artist, COUNT(Artist) AS plays \
        FROM sql_table \
        GROUP BY Artist")
# save the results in a new view
play_counts.createOrReplaceTempView("artist_counts")

# use a self join to find where the max play equals the count value
spark.sql("SELECT a2.Artist, a2.plays FROM \
          (SELECT max(plays) AS max_plays FROM artist_counts) AS a1 \
          JOIN artist_counts AS a2 \
          ON a1.max_plays = a2.plays \
          ").show()


########################## Question 5 (challenge) ##########################
# How many songs do users listen to on average between visint our home page? Round to closest integer
# TODO: write your code to answer question 5
# SELECT CASE WHEN 1 > 0 THEN 1 WHEN 2 > 0 THEN 2.0 ELSE 1.2 END;
is_home = spark.sql('''SELECT userID, page, ts, CASE WHEN page = 'Home' THEN 1 ELSE 0 END AS is_home 
            FROM sql_table 
            WHERE (page = 'NextSong') or (page = 'Home') 
            ''')

# keep the results in a new view
is_home.createOrReplaceTempView("is_home_table")

# find the cumulative sum over the is_home column
cumulative_sum = spark.sql('''SELECT *, SUM(is_home) OVER 
    (PARTITION BY userID ORDER BY ts DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS period 
    FROM is_home_table''')

# keep the results in a view
cumulative_sum.createOrReplaceTempView("period_table")

# find the average count for NextSong
spark.sql('''SELECT AVG(count_results) FROM 
          (SELECT COUNT(*) AS count_results FROM period_table 
GROUP BY userID, period, page HAVING page = "NextSong") AS counts''').show()








