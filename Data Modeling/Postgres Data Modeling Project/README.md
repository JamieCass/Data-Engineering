# Data Modeling with PostgreSQL project

## Project Overview:
Sparkify a music listening company have been collecting data on songs and user activity for their music streaming app. They are particularly interested in understanding what songs users are currently listening to. 

## Database Design:
Database has been designed to optimize queries on songplay analysis. 5 tables make up the database with the Fact Table being 'songplays'. I have created the dataframe in the Star Schema for its simple design and ease of joins and aggregation speed.

Tables include:
songplays (Fact Table) - records log data associated with song plays
users - users in the app
songs - songs in the music database
artists - artists in the music database
time - timestamp records in songplays



## ETL Process:
ETL process will allow us to process the data from the JSON files and load it into the specified tables in the dataset. This will allow the analytics department to easily use the tables to analise the data.

