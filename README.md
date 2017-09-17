# SQL Tap
I developed this project to help some of my friends learn SQL by trying to mimic the kind of data
that would be available in a real company. With access to real world like data they would be able to 
learn SQL the hard way.

This project consists of a collection of Python scripts to create multiple datasets that can be inserted 
into any relational database. This project uses data sources available online to create a hotels reservation database.

## Getting Started
I did not intend to open source this when developing it but I'm doing so now to share this with some of my friends who 
want to tinker with this project. Admittedly, in trying to run these scripts you might encounter
minor errors related to source directory paths, package installations which should be easy to fix.


## Deployment
1) Run custom_scripts/data_preparation.py to create the input data resources
* Note that RoomTypeList.txt, AttributeList.txt and ActivePropertyList.txt need to be copied into input_data directory. These files
are available via developer.ean.com/database

2) Run custom_scripts/write_guests.py to create a list of guests. 
Change the number of guests in the script to control how many guest profiles you want to create

3) Run custom_scripts/write_hotel_bookings.py to create hotel bookings
 
4) After invoking psql run the following to create the tables
\i DB_AS_A_SERVICE/sql/hotel_db_create_queries.sql

5) As postgres user run the copy commands in 
DB_AS_A_SERVICE/sql/insert_from_files.sql

## Built With
* Python

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details