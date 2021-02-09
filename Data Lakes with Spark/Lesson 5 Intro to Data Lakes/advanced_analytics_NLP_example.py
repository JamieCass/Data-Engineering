import pandas as pd 
pd.set_option('max_colwidth', 800)

# -------------------------------- Create a spark context that includes a 3rd party jar for NLP --------------------------------
# jarPath = 'spark-nlp-assembly-2.7.3.jar'
from pyspark.sql import SparkSession
spark = SparkSession.builder \
	.config('spark.jars.packages', 'JohnSnowLabs:spark-nlp:1.8.2') \
	.getOrCreate()
spark 

# -------------------------------- Read multiple file in a dir as one dataframe --------------------------------
dataPath = '/Users/jamie/data/*.json' # The * will read every file that is followed by .json. ?I think its called a wildcard
df = spark.read.json(dataPath)
print(df.count())
df.printSchema()


# -------------------------------- Deal with struct type to query subfields --------------------------------\
title = 'data.title'
author = 'data.author'
dfAuthorTitle = df.select(title, author) # This will select just the title and author from the reddit file
dfAuthorTitle.limit(5).toPandas()


# -------------------------------- Try to implement the equivalent of flatMap in dataframes --------------------------------
# We want to know what sort of things the reddit post is talking about
import pyspark.sql.functions as F 
dfWordCount = df.select(F.explode(F.split(title, '\\s+')).alias('word').count().orderBy(F.desc('count')))
dfWordCount.limit(10).toPandas()


# -------------------------------- Use a NLP library to do part-of-speech tagging --------------------------------
from com.johnsnowlabs.nlp.pretrained.pipeline.en import BasicPipeline as bp 
dfAnnotated = bp.annotate(dfAuthorTitle, 'title')
dfAnnotated.printSchema()

# -------------------------------- Deal with Map type to query subfields -------------------------------- 
dfPos = dfAnnotated.select('text', 'pos.metadata', 'pos.result') # pos stands for part of speech 
dfPos.limit(5).toPandas()

dfPos = dfAnnotated.select(F.explode('pos').alias('pos'))
dfPos.printSchema()
dfPos.toPandas()

# -------------------------------- Keep only the proper nouns NNP or NNPS -------------------------------- 
nnpFilter = 'pos.result = "NNP" or pos.result = "NNPS" '
dfNNP = dfPos.where(nnpFilter)
dfNNP.limit(10).toPandas()


# -------------------------------- Extract columns for a map in a col --------------------------------
dfWordTag = dfNNP('pos.metadata["word"] as word', 'pos.result as tag') 
dfWordTag.limit(10).toPandas()

# Group by what words show up the most 
from pyspark.sql.functions import desc 
dfWordTag.groupBY('word').count().orderBy(desc('count')).show()