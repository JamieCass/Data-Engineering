from pyspark.sql import SparkSession

if __name__ == '__main__':
	'''
	example program to show how to submit applications
	'''
spark = SparkSession\
	.builder\
	.appName('LowerSongTitles')\
	.getOrCreate()

	log_of_songs = [
	        "Despacito",
	        "Nice for what",
	        "No tears left to cry",
	        "Despacito",
	        "Havana",
	        "In my feelings",
	        "Nice for what",
	        "despacito",
	        "All the stars"
	]

distributed_song_lod = spark.sparkContext.parallelize(log_of_songs) # we have to name sparkContext rather than just using sc like we did in the maps and lazy evaluation notebook.

print(distributed_song_lod.map(lambda x: x.lower()).collect())

spark.stop()