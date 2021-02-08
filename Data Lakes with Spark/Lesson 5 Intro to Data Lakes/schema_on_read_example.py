from pyspark.sql import SparkSession
import pandas as pd 
import matplotlib

spark = SparkSession.builder.getOrCreate()

# -------------------------------- Load the dataset --------------------------------
# Data Source: http://ita.ee.lbl.gov/traces/NASA_access_log_Jul95.gz
dfLog = spark.read.text('/Users/jamie/Downloads/NASA_access_log_Jul95.gz')

# Quick inspection of the dataset
# See the schema
dfLog.printSchema()

# Number of lines
dfLog.count()

# Whats in there? 
dfLog.show(5)

# A better show
dfLog.show(5, truncate=False) # Still a little ugle

# Pandas to the rescue
pd.set_option('max_colwidth', 200)
dfLog.limit(5).toPandas() # limit will prevent loading the whole file onto pandas, it will only load the first 5


# -------------------------------- Lets try a simple parsing with split --------------------------------
from pyspark.sql.functions import split
dfArrays = dfLog.withColumn('tokenized', split('value', ' '))
dfArrays.limit(10).toPandas()


# Second attempt, lets build a custom parsing UDF
from pyspark.sql.functions import udf 

@udf(MapType(StringType(),StringType()))
def parseUDF(line):
	import re 
	PATTERN = '^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+)\s*(\S+)\s*" (\d{3}) (\S+)' # general REGEX for weblogs 
	match = re.search(PATTERN, line)
	if match is None:
		return (line, 0)
	size_field = match.group(9)
	if size_field == '-':
		size = 0 
	else:
		size = match.group(9)
	return {
		'host' 		 	: match.group(1),
		'client_identd' : match.group(2),
		'user_id' 		: match.group(3),
		'date_time'		: match.group(4),
		'method' 		: match.group(5),
		'endpoint' 		: match.group(6),
		'protocol' 		: match.group(7),
		'response_code' : int(match.group(8)),
		'content_size' 	: size
	}
	
# Lets start at the beginning 
dfParsed = dfLog.withColumn('parsed', parseUDF('value'))
dfParsed.limit(10).toPandes()

# Check the schema again to see if we have a column tyope map with the fields parsed
dfParsed.printSchema()

dfParsed.select('parsed').limit(10).toPandas() # We need to split the keys into columns... 


# -------------------------------- Lets build seperate columns --------------------------------
dfParsed.selectExpr('pardes["host"] as host').limit(5).show(5)

dfParsed.selectExpr(['parsed["host"]', 'parsed["date_time"]']).show(5)

# Now we can use a list comprehenshion to do it for all the fields... 
fields = ['host', 'client_identd', 'user_id', 'date_time', 'method', 'endpoint', 'protocol', 'response_code', 'content_size']
exprs = ['parsed["{}"] as {}'.format(field,field) for field in fields]
print(exprs)

dfClean = dfParsed.selectExpr(*exprs) # The '*' will load all exprs rather than making us list all of them..
dfClean.limit(5).toPandas() # This will show a DF will all the columns with the data and names we just specified.


# -------------------------------- Popular hosts --------------------------------
# This will show a count for all hosts
from pyspark.sql.functions import desc 
dfClean.groupBy('host').count().orderBy(desc('count')).limit(10).toPandas()


# -------------------------------- Popular hosts --------------------------------
# This will show the most popular content and how many times it was viewed.
dfClean.groupBy('endpoint').count().orderBy(desc('count')).limit(10).toPandas()


# -------------------------------- Large files --------------------------------
# See what are largest files (This isnt correct, because it is sorted by strings, not integers.)
dfClean.createOrReplaceTempView('cleanlog')
spark.sql("""
select endpoint, content_size
from cleanlog
order by content_size desc
""").limit(10).toPandas()


# To fix the above problem and make the content size into an integer
from pyspark.sql.functions import expr 
dfCleanTyped = dfClean.withColumn('content_size_bytes', expr('cast(content_size as int')) # Here we cast the content size as an int
dfCleanTyped.limit(5).toPandas()

# Lets test and see if the new data is correct (this is correct, and will show the correct file sizes in order)
dfClean.createOrReplaceTempView('cleantypedlog')
spark.sql("""
select endpoint, content_size
from cleanlog
order by content_size desc
""").limit(10).toPandas()



# -------------------------------- Something you can do --------------------------------
# Left for you, clean the date column
# 1- Create a udf that parses that weird format,
# 2- Create a new column with a date time string that spark would understand 
# 3- Add a new date-time column properly types
# 4- Print your schema







