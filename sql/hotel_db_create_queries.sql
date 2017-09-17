
-- You may need to create the database if it does not exist
-- CREATE DATABASE hotel_bookings;

CREATE TABLE Hotels (hotel_id int PRIMARY KEY NOT NULL,
    hotel_full_name varchar(255)  NOT NULL,
    hotel_latitude decimal(8,3),
    hotel_longitude decimal(8,3),
    hotel_address varchar(255)  NOT NULL,
    hotel_country varchar(255) NOT NULL,
    hotel_currency varchar(10) NOT NULL,
    hotel_star_rating varchar(10) NOT NULL,
    hotel_location varchar(255) NOT NULL
);

CREATE TABLE Ref_Hotel_Facilities (
    facility_code int PRIMARY KEY NOT NULL,
    facility_description varchar(255)  NOT NULL
);

CREATE TABLE Hotel_Facilities (
    hotel_id int references hotels(hotel_id),
    facility_code int  references Ref_Hotel_Facilities(facility_code),
    UNIQUE(hotel_id, facility_code)
);


CREATE TABLE Ref_Booking_Status (
    booking_status_code int PRIMARY KEY NOT NULL,
    booking_status_description varchar(25)  NOT NULL
);


CREATE TABLE Ref_Hotel_Room_Type (
    room_type_code int PRIMARY KEY NOT NULL,
    room_type_description varchar(255) NOT NULL
);

CREATE TABLE Guests (
    guest_id int  PRIMARY KEY NOT NULL,
    first_name varchar(50)  NOT NULL,
    last_name varchar(50)  NOT NULL,
    date_of_birth date  NOT NULL,
    email_address varchar(100) NOT NULL,
    city varchar(100) NOT NULL,
    country varchar(100) NOT NULL
);

CREATE TABLE Hotel_Bookings (
    hotel_booking_id int  PRIMARY KEY NOT NULL,
    hotel_id int  references hotels(hotel_id),
    guest_id int  references guests(guest_id),
    booking_status_code int references Ref_Booking_Status(booking_status_code),
    booking_start_date date  NOT NULL,
    booking_end_date date  NOT NULL,
    room_type_code int references Ref_Hotel_Room_Type(room_type_code),
    room_rate decimal(8,3) NOT NULL,
    booking_referrer varchar(255)  NOT NULL
);