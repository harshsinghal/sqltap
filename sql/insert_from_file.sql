COPY guests FROM '/home/hsinghal/workspace/DB_AS_A_SERVICE/custom_scripts/guests.txt' DELIMITER '|';
COPY hotels FROM '/home/hsinghal/workspace/DB_AS_A_SERVICE/custom_scripts/hotels.txt' DELIMITER '|';
COPY ref_booking_status FROM '/home/hsinghal/workspace/DB_AS_A_SERVICE/custom_scripts/ref_booking_status.txt' DELIMITER '|' ;
COPY ref_hotel_facilities FROM '/home/hsinghal/workspace/DB_AS_A_SERVICE/custom_scripts/ref_hotel_facilities.txt' DELIMITER '|';
COPY ref_hotel_room_type FROM '/home/hsinghal/workspace/DB_AS_A_SERVICE/custom_scripts/ref_hotel_room_type.txt' DELIMITER '|';
COPY hotel_facilities FROM '/home/hsinghal/workspace/DB_AS_A_SERVICE/custom_scripts/hotel_facilities.txt' DELIMITER '|';
COPY hotel_bookings FROM '/home/hsinghal/workspace/DB_AS_A_SERVICE/custom_scripts/hotel_bookings.txt' DELIMITER '|';
