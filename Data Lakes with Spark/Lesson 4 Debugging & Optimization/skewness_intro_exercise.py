from pyspark.sql import SparkSession
from pyspark.sql.functions import desc 

def explore_dataframe():
	
	spark = SparkSession.builder.appName("Skewness Introduction").getOrCreate()

	#TODO get your file path from s3 for parking_violation.csv
	input_path = "/Users/jamie/data/parking_violation.csv"
	df = spark.read.format("csv").option("header", True).load(input_path)

	# investigate what columns you have
	col_list = df.columns
	print(col_list)

    # TODO groupby month and year to get count
	year_df = df.groupby("year")
	month_df = df.groupby("month")

	year_df.count().orderBy(desc('count')).show()
	month_df.count().orderBy(desc('count')).show()

    # TODO write file partition by year, and study the executor in the spark UI
    # TODO use repartition function
	df.write.partitionBy('year').csv('trial-year')


if __name__ == "__main__":
	explore_dataframe()