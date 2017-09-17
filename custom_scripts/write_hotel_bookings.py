import sys
import os
import pandas as pd
import random
import pickle
import arrow
from numpy.random import choice

"""
CREATE TABLE Hotel_Bookings (
    hotel_booking_id int  NOT NULL AUTO_INCREMENT,
    hotel_id int  NOT NULL,
    guest_id int  NOT NULL,
    booking_status_code char(3)  NOT NULL,
    booking_start_date date  NOT NULL,
    booking_end_date date  NOT NULL,
    room_type_code varchar(10) NOT NULL,
    room_rate decimal(8,3) NOT NULL,
    booking_referrer varchar(255)  NOT NULL
);
"""
print "Generate Hotel Bookings"

# Read in all the hotels
print "read in hotels data"
hotels = pd.read_pickle('hotels.pkl')

# Read all the guests in
print "read in guests data"
guests = pd.read_pickle('../to_db/guests.pkl')

# Convert guests to list
list_of_guests = guests.values.tolist()

# read room rate code
print "read room rate distribution"
room_rate_distr = pd.read_pickle('rate_distr.pkl')
rate_items = room_rate_distr[0]
rate_probs = room_rate_distr[1]

# read booking referral distribution
print "read booking referral distribution"
booking_referrer_distr = pd.read_pickle('booking_referral_distr.pkl')
booking_referrer_items = booking_referrer_distr[0]
booking_referrer_probs = booking_referrer_distr[1]

# read room type code
print "read room type code distribution"
room_type_code = pd.read_pickle('room_type_distr.pkl')
room_type_items = room_type_code[0]
room_type_probs = room_type_code[1]

# booking status
print "read booking status"
booking_status_distr = pickle.load(open("booking_status_distr.pkl", 'rb'))
booking_status_items = booking_status_distr[0]
booking_status_probs = booking_status_distr[1]


# Start generating bookings
hotel_booking_id = 444234542
ctr = 0
all_results = []
START_DATE = '2015-03-01'
start_date_obj = arrow.get(START_DATE)

NUMBER_OF_BOOKING_DATES = 2
NUM_BOOKINGS_PER_DAY_MIN = 10
NUM_BOOKINGS_PER_DAY_MAX = 20

for each_hotel in hotels.iterrows():
    if len(list_of_guests) == 0:
        break
    # For each booking date
    for i in range(NUMBER_OF_BOOKING_DATES):
        booking_start_date = start_date_obj.replace(days=i)
        booking_start_date_str = booking_start_date.format('YYYY-MM-DD')
        number_of_booking = random.randint(NUM_BOOKINGS_PER_DAY_MIN, NUM_BOOKINGS_PER_DAY_MAX)
        # For each start_date of_booking cycle through hotels
        for j in range(number_of_booking):
            # Get a guest
            try:
                get_guest = list_of_guests.pop()
                booking_end_date_str = booking_start_date.replace(days=choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 1, p=[.1, 0.7, .1, .02, 0.01, 0.01, 0.01, 0.01, 0.01, 0.03])[0]).format('YYYY-MM-DD')
                temp_dict = {
                    'hotel_booking_id': hotel_booking_id + ctr,
                    'hotel_id': each_hotel[1]['hotel_id'],
                    'guest_id': get_guest[0],
                    'booking_status_code': choice(booking_status_items, 1, p=booking_status_probs)[0],
                    'booking_start_date': booking_start_date_str,
                    'booking_end_date': booking_end_date_str,
                    'room_type_code': choice(room_type_items, 1, p=room_type_probs)[0],
                    'room_rate': choice(rate_items, 1, p=rate_probs)[0],
                    'booking_referrer': choice(booking_referrer_items, 1, p=booking_referrer_probs)[0]
                }
                ctr += 1
                all_results.append(temp_dict)
            except IndexError:
                print "list of guests exhausted"
                break


bookings_df = pd.DataFrame.from_records(all_results)
bookings_df.to_pickle(os.path.join('../to_db', 'hotel_bookings.pkl'))