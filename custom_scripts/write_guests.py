from numpy.random import choice
import pickle
from collections import defaultdict
import os
import random
import pandas as pd
import arrow

# -----------------
# Get location data
# -----------------
print "Loading City Probability Distribution"
city_pop_distr = pickle.load(open('city_pop_distr.pkl', 'rb'))
city_state = city_pop_distr[0]
city_state_population_prob = city_pop_distr[1]
choice(city_state, p=city_state_population_prob)

# -----------------
# Get Names data
# -----------------
print "Loading Names Data"
first_last_names = pickle.load(open('first_last_names.pkl', 'rb'))
first_names = first_last_names[0]
last_names = first_last_names[1]

# -----------------
# Get Random Date of Birth
# -----------------
print " Test - generate random date"
cur_date = arrow.utcnow()
print cur_date.replace(years=-1 * random.randint(20, 70), days=-1 * random.randint(0, 365)).format("YYYY-MM-DD")

# -----------------
# Get Email Address
# -----------------
print "Loading Email Address Domains distribution "
email_domains_distr = pickle.load(open('email_domains_distr.pkl', 'rb'))
email_domains_items = email_domains_distr[0]
email_domains_prob = email_domains_distr[1]
choice(email_domains_items, p=email_domains_prob)

# ----------------
# Get User name for email address
# ----------------
print "Loading git user ids"
git_userids = pickle.load(open('git_user_names.pkl', 'rb'))

print "Define email user name modifiers"


def user_asis(fname, lname):
    choice(['', '_', '.'], p=[0.3, 0.3, 0.4])
    return ''.join([
        fname.lower(),
        choice(['', '_', '.'], p=[0.3, 0.3, 0.4]),
        lname.lower()]
    )


def user_with_num_trailing(fname, lname):
    choice(['', '_', '.'], p=[0.3, 0.3, 0.4])
    return ''.join([
        fname.lower(),
        choice(['', '_', '.'], p=[0.3, 0.3, 0.4]),
        lname.lower(),
        str(random.randint(20, 1000))]
    )


def get_a_git_user_id(fname, lname):
    return choice(git_userids)


email_trans_func_items = [user_asis, user_with_num_trailing, get_a_git_user_id]
email_trans_func_probs = [0.1, 0.6, 0.3]

choice(email_trans_func_items, p=email_trans_func_probs)('Harsh', 'Singhal')


"""
CREATE TABLE Guests (
    guest_id int  NOT NULL,
    first_name varchar(50)  NOT NULL,
    last_name varchar(50)  NOT NULL,
    date_of_birth date  NOT NULL,
    email_address varchar(100) NOT NULL,
    city varchar(100) NOT NULL,
    country varchar(100) NOT NULL
);
"""

# Total number of guests to simulate
NUM_GUESTS = 100000
START_ID = 34566732
# Counter to increment the START_ID to obtain value for guest_id
guest_num = 0
# Store results
result_rows = []
# Dictionary to check if generate guest exists or not
guest_key = defaultdict(int)
# Chunk size for sampling
each_chunk = 1000

while len(result_rows) <= NUM_GUESTS:
    # Sample from probability distribution in each_chunk size
    first_name_list = choice(first_names, each_chunk)
    last_name_list = choice(last_names, each_chunk)
    date_of_births_list = [(cur_date.replace(years=-1 * random.randint(20, 70), days=-1 * random.randint(0, 365)).format("YYYY-MM-DD")) \
                      for k in range(each_chunk)]
    city_list = choice(city_state, each_chunk, p=city_state_population_prob)
    email_mod_func_list = choice(email_trans_func_items, each_chunk, p=email_trans_func_probs)
    email_domains_list = choice(email_domains_items,each_chunk, p=email_domains_prob)
    print len(result_rows)
    for i in range(each_chunk):
        first_name = first_name_list[i]
        last_name = last_name_list[i]
        date_of_birth = date_of_births_list[i]
        email_user_name = email_mod_func_list[i](first_name, last_name)
        email_domain = email_domains_list[i]
        email_address = '@'.join([email_user_name, email_domain])
        city = city_list[i]
        country = 'USA'
        # Check if generated guest already exists
        guest_unique_key = (first_name, last_name, date_of_birth, email_address, city)
        if guest_unique_key not in guest_key:
            # If guest does not exist, then store record
            #  Mark as exists
            guest_key[guest_unique_key] = 1
            # Generate guest_id
            guest_id = START_ID + guest_num
            # Store in temp dictionary
            temp_dict = {
                'guest_id': guest_id,
                'first_name': first_name,
                'last_name': last_name,
                'date_of_birth': date_of_birth,
                'email_address': email_address,
                'city': city,
                'country': country
            }
            # append to results list
            result_rows.append(temp_dict)
            guest_num += 1


# Create data frame
guests_df = pd.DataFrame.from_records(result_rows)

guests_df = guests_df[['guest_id', 'first_name', 'last_name', 'date_of_birth', 'email_address', 'city', 'country']]
# Write to pickle
guests_df.to_pickle(os.path.join('../to_db', 'guests.pkl'))
