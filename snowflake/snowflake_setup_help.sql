-- Create a database. A database automatically includes a schema named 'public'.

create or replace database mydatabase;

/* Create target tables for CSV and JSON data. The tables are temporary, meaning they persist only for the duration of the user session and are not visible to other users. */

create or replace temporary table mycsvtable (
  id integer,
  last_name string,
  first_name string,
  company string,
  email string,
  workphone string,
  cellphone string,
  streetaddress string,
  city string,
  postalcode string);

create or replace temporary table myjsontable (
  json_data variant);

-- Create a warehouse

create or replace warehouse mywarehouse with
  warehouse_size='X-SMALL'
  auto_suspend = 120
  auto_resume = true
  initially_suspended=true;



-- Create file format for CSV 

create or replace file format mycsvformat
  type = 'CSV'
  field_delimiter = '|' -- ',' would be the usual one, but for this example we use '|'
  skip_header = 1;


-- Create file format for JSON 

create or replace file format myjsonformat
  type = 'JSON'
  strip_outer_array = true;



-- Stage for CSV data files 
create or replace stage my_csv_stage
  file_format = mycsvformat;


-- Stage for JSON data files 
create or replace stage my_json_stage
  file_format = myjsonformat;










