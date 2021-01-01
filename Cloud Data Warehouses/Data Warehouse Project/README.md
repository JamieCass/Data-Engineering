# Data Warehouse project

## Project Overview:
A music streaming startup, Sparkify has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

## Database Design:
Database has been designed to optimize queries on songplay analysis. 5 tables make up the database with the Fact Table being 'songplays'. I have created the dataframe in the Star Schema for its simple design and ease of joins and aggregation speed.

Tables include:
songplays (Fact Table) - records log data associated with song plays
users - users in the app
songs - songs in the music database
artists - artists in the music database
time - timestamp records in songplays



## ETL Process:
ETL process will allow us to process the data from the JSON files residing in the S3 bucket and load them into the staging tables in Redshift, from there we can insert the data into our 5 analytic tables where the analytics team will be able to run their queries.

