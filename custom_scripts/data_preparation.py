import os
import pickle
import pandas as pd
from collections import Counter
from numpy.random import choice
import random
import re
import simplejson


data_dir = '/home/hsinghal/workspace/DB_AS_A_SERVICE/input_data'
store_into = '/home/hsinghal/workspace/DB_AS_A_SERVICE/custom_scripts'


# -------------------------------
# Identify the population distribution across cities
# -------------------------------
# World cities data
world_cities = pd.read_table(os.path.join(data_dir, 'worldcitiespop.txt'), sep=",", index_col=None)
# Keep only US cities
us_cities = world_cities[world_cities.Country == 'us']
# Keep cities with available population numbers
us_cities_with_pop = us_cities[us_cities.Population > 0]
# Get population probabilities
us_cities_with_pop['population_prob'] = us_cities_with_pop.Population / us_cities_with_pop.Population.sum()
# Keep only relevant columns
us_cities_data = us_cities_with_pop[['City', 'Region', 'population_prob']]

# Create list of (city,state) and a list of probabilities
city_state = []
city_state_population_prob = []
for each_row in us_cities_data.iterrows():
    row = each_row[1]
    # city_state.append((row['City'].title(), row['Region']))
    city_state.append(row['City'].title())
    city_state_population_prob.append(row['population_prob'])

choice(city_state, p=city_state_population_prob)

# Store pickled
with open(os.path.join(store_into, 'city_pop_distr.pkl'), 'wb') as fout:
    pickle.dump([city_state, city_state_population_prob], fout, -1)


# -----------------
# Get Names data
# -----------------
# Read all names from NationalNames.csv
national_names = pd.read_table(os.path.join(data_dir, 'NationalNames.csv'), sep=",", index_col=False)
national_names.columns
national_names.head()
firstnames_namedb = pd.read_table(os.path.join(data_dir, 'namedb_first_names_us.txt'), header=None)
firstnames_namedb.columns = ['firstname']
firstnames_namedb.head()
# Get all first names
first_names = list(set(national_names.Name.tolist() + firstnames_namedb.firstname.tolist()))

# Get last names
lastnames_namedb = pd.read_table(os.path.join(data_dir, 'namedb_surnames_us.txt'),header=None)
lastnames_namedb.columns = ['lastname']
last_names = list(set(lastnames_namedb.lastname.tolist()))
len(last_names)

# Get last names for uk
lastnames_namedb_uk = pd.read_table(os.path.join(data_dir, 'namedb_surnames_uk.txt'),header=None)
lastnames_namedb_uk.columns = ['lastname']
last_names_uk = list(set(lastnames_namedb_uk.lastname.tolist()))
len(last_names_uk)

last_names_list = list(set(last_names + last_names_uk))

with open(os.path.join(store_into,'first_last_names.pkl'),'wb') as fout:
    pickle.dump([first_names, last_names_list], fout, -1)


# -----------------
# Get Email Address
# -----------------
# Get domains
popular_domains_distr = [
    ("gmail.com", 0.1),
    ("yahoo.com", 0.08),
    ("hotmail.com", 0.07),
    ("aol.com", 0.05),
    ("msn.com", 0.04)]

# ref https://github.com/mailcheck/mailcheck/wiki/List-of-Popular-Domains
# the list below is not used
email_domains_all = ["aol.com", "att.net", "comcast.net", "facebook.com", "gmail.com", "gmx.com", "googlemail.com",
  "google.com", "hotmail.com", "hotmail.co.uk", "mac.com", "me.com", "mail.com", "msn.com",
  "live.com", "sbcglobal.net", "verizon.net", "yahoo.com", "yahoo.co.uk",
  "email.com", "games.com", "gmx.net", "hush.com", "hushmail.com", "icloud.com", "inbox.com",
  "lavabit.com", "love.com" , "outlook.com", "pobox.com", "rocketmail.com",
  "safe-mail.net", "wow.com", "ygm.com" , "ymail.com", "zoho.com", "fastmail.fm",
  "yandex.com","iname.com",
  "bellsouth.net", "charter.net", "comcast.net", "cox.net", "earthlink.net", "juno.com",
  "btinternet.com", "virginmedia.com", "blueyonder.co.uk", "freeserve.co.uk", "live.co.uk",
  "ntlworld.com", "o2.co.uk", "orange.net", "sky.com", "talktalk.co.uk", "tiscali.co.uk",
  "virgin.net", "wanadoo.co.uk", "bt.com",
  "sina.com", "qq.com", "naver.com", "hanmail.net", "daum.net", "nate.com", "yahoo.co.jp", "yahoo.co.kr", "yahoo.co.id", "yahoo.co.in", "yahoo.com.sg", "yahoo.com.ph",
  "hotmail.fr", "live.fr", "laposte.net", "yahoo.fr", "wanadoo.fr", "orange.fr", "gmx.fr", "sfr.fr", "neuf.fr", "free.fr",
  "gmx.de", "hotmail.de", "live.de", "online.de", "t-online.de", "web.de", "yahoo.de",
  "mail.ru", "rambler.ru", "yandex.ru", "ya.ru", "list.ru",
  "hotmail.be", "live.be", "skynet.be", "voo.be", "tvcablenet.be", "telenet.be",
  "hotmail.com.ar", "live.com.ar", "yahoo.com.ar", "fibertel.com.ar", "speedy.com.ar", "arnet.com.ar",
  "hotmail.com", "gmail.com", "yahoo.com.mx", "live.com.mx", "yahoo.com", "hotmail.es", "live.com", "hotmail.com.mx", "prodigy.net.mx", "msn.com",
  "yahoo.com.br", "hotmail.com.br", "outlook.com.br", "uol.com.br", "bol.com.br", "terra.com.br", "ig.com.br", "itelefonica.com.br", "r7.com", "zipmail.com.br", "globo.com", "globomail.com", "oi.com.br"]

email_domains = pd.read_table(os.path.join(data_dir, 'email_domains.txt'), header=None, index_col=False)
email_domains.columns = ['email_domain']
email_domains_more = [k for k in email_domains.email_domain.tolist() if re.search("com$", k) and 'mail2' not in k]
prob_of_other_domains = (1 - sum([k[1] for k in popular_domains_distr])) / len(email_domains_more)
email_domains_items = [k[0] for k in popular_domains_distr] + email_domains_more
email_domains_prob = [k[1] for k in popular_domains_distr] + [prob_of_other_domains] * len(email_domains_more)

choice(email_domains_items, p=email_domains_prob)
with open(os.path.join(store_into,'email_domains_distr.pkl'),'wb') as fout:
    pickle.dump([email_domains_items, email_domains_prob], fout, -1)


# ----------------
# Get Git user name for email address
# ----------------

gitdata = open(os.path.join(data_dir, '2015-01-01-15.json'), 'r').readlines()
git_userids = []
for i in gitdata:
    i = i.strip()
    d = simplejson.loads(i)
    git_userids.append(d['actor']['login'])

with open(os.path.join(store_into,'git_user_names.pkl'),'wb') as fout:
    pickle.dump(git_userids, fout, -1)

# ***************************************************
# ***************************************************

# ---------------------
#  Create Table Hotels
# ---------------------

def address_clean(addr):
    if len(str(addr)) < 4:
        return ''
    elif str(addr) == 'NaN':
        return ''
    return str(addr)


"""

CREATE TABLE Hotels (
    hotel_id int NOT NULL,
    hotel_full_name varchar(255)  NOT NULL,
    hotel_latitude decimal(8,3),
    hotel_longitude decimal(8,3),
    hotel_address varchar(255)  NOT NULL,
    hotel_country varchar(255) NOT NULL,
    hotel_currency varchar(10) NOT NULL,
    hotel_star_rating varchar(10) NOT NULL,
    hotel_location varchar(255) NOT NULL
);

"""

# Read Active Properties List
df_active_props = pd.read_table(os.path.join(data_dir, 'ActivePropertyList.txt'), sep="|", index_col=None)

df_active_props.head(10)
# Iterate over each row and only keep US hotels
result_rows = []
START_ID = 53689
for each_row in df_active_props.iterrows():
    row = each_row[1]
    temp_dict = {
        'hotel_id': each_row[0] + START_ID,
        'hotel_full_name': row['Name'],
        'hotel_latitude': row['Latitude'],
        'hotel_longitude': row['Longitude'],
        'hotel_address': ' '.join([address_clean(row['Address1']), address_clean(row['Address2'])]),
        'hotel_country': row['Country'],
        'hotel_currency': row['PropertyCurrency'],
        'hotel_star_rating': row['StarRating'],
        'hotel_location': row['Location']
    }
    if row['Country'] == 'US':
        result_rows.append(temp_dict)

# Create pandas data frame
hotels_df = pd.DataFrame.from_records(result_rows)
hotels_df.head()

hotels_df = hotels_df[['hotel_id', 'hotel_full_name', 'hotel_latitude', 'hotel_longitude', 'hotel_address', 'hotel_country', 'hotel_currency','hotel_star_rating','hotel_location']]
# Store results in results_data directory
hotels_df.to_pickle(os.path.join(store_into, 'hotels.pkl'))

# ------------------
# Hotel Facilities Reference List
# -----------------
"""
CREATE TABLE Ref_Hotel_Facilities (
    facility_code int  NOT NULL,
    facility_description varchar(50)  NOT NULL
);
"""

# Read hotel facilities list
df_ref_hotel_facilities = pd.read_table(os.path.join(data_dir, 'AttributeList.txt'), sep="|", index_col=None)
df_ref_hotel_facilities.head()
hotel_facilities_list = df_ref_hotel_facilities['AttributeDesc'].values.tolist()

result_rows = []
START_ID = 34213
ctr = 0
for each_row in hotel_facilities_list:
    temp_dict = {
        'facility_code': ctr + START_ID,
        'facility_description': each_row
    }
    result_rows.append(temp_dict)
    ctr += 1
# Create pandas data frame
ref_hotel_facilities = pd.DataFrame.from_records(result_rows)
# Store results in results_data directory
ref_hotel_facilities[['facility_code', 'facility_description']].to_pickle(os.path.join(store_into, 'ref_hotel_facilities.pkl'))

# ------------------
# Hotel Facilities - For Each Hotel
# -----------------

"""
CREATE TABLE Hotel_Facilities (
    hotel_id int  NOT NULL,
    facility_code int  NOT NULL
);
"""


# Read in hotels.pkl and ref_hotel_facilities.pkl
# For each hotel, identify hotel facilities

# Read ref_hotel_facilities.pkl
ref_hotel_facilities = pd.read_pickle('ref_hotel_facilities.pkl')
ref_hotel_facilities.head()

# Read hotels.pkl
hotels_df = pd.read_pickle('hotels.pkl')

# Iterate over each hotel
# For each hotel, get a random selection of facilities
all_results = []
for each_row in hotels_df.iterrows():
    row = each_row[1]
    # Get a random selection of facilities
    random_percent = random.uniform(1, 5) / 100
    hotels_ref = ref_hotel_facilities.sample(frac=random_percent, replace=False)
    for each_facility in hotels_ref.iterrows():
        temp_dict = {
            'hotel_id': row['hotel_id'],
            'facility_code': each_facility[1]['facility_code']
        }
        all_results.append(temp_dict)


# Create data frame
hotel_facilities_df = hotel_facilities = pd.DataFrame.from_records(all_results)
hotel_facilities_df.head()
hotel_facilities_df[['hotel_id','facility_code']].to_pickle(os.path.join(store_into, 'hotel_facilities.pkl'))


# ------------------
# Hotel Booking Status
# -----------------

"""
CREATE TABLE Ref_Booking_Status (
    booking_status_code char(3)  NOT NULL,
    booking_status_description varchar(25)  NOT NULL
);
"""


booking_status = [
    [12541, 'Confirmed', 0.85],
    [12542, '6 PM Release', 0.01],
    [12552, 'Tentative / Provisional', 0.01],
    [12562, 'Waitlist', 0.03],
    [12572, 'Turn away', 0.01],
    [12582, 'Cancelled', 0.04],
    [12592, 'No Show', 0.01],
    [12642, 'Company Guarantee', 0.01],
    [12652, 'Travel Agent Guarantee', 0.03]
]

booking_status_df = pd.DataFrame.from_records(booking_status)
booking_status_df.columns = ['booking_status_code', 'booking_status_description', 'booking_status_prob']


booking_status_df[['booking_status_code', 'booking_status_description']].to_pickle(os.path.join(store_into, 'ref_booking_status.pkl'))

booking_status_items = [k[0] for k in booking_status]
booking_status_probs = [k[2] for k in booking_status]
sum(booking_status_probs)

pickle.dump([booking_status_items, booking_status_probs], open(os.path.join(store_into, 'booking_status_distr.pkl'),'wb'), -1)


# ------------------------
# Hotel Room Rate Distribution
# ------------------------

# Read Active Properties List
df_active_props = pd.read_table(os.path.join(data_dir, 'ActivePropertyList.txt'), sep="|", index_col=None)
high_rate = df_active_props[(df_active_props.PropertyCurrency == 'USD') & (df_active_props.Country == 'US') & (df_active_props.HighRate > 0)]['HighRate']
low_rate = df_active_props[(df_active_props.PropertyCurrency == 'USD') & (df_active_props.Country == 'US') & (df_active_props.HighRate > 0)]['LowRate']
rate_ctr = Counter(high_rate + low_rate).most_common(500)
sum_val = sum([k[1] for k in rate_ctr])  * 1.0
rate_items = [k[0] for k in rate_ctr]
rate_probs = [k[1]/sum_val for k in rate_ctr]
choice(rate_items, 1 , p=rate_probs)[0]
pickle.dump([rate_items, rate_probs], open(os.path.join(store_into, 'rate_distr.pkl'), 'wb'), -1)


# ------------------------------
# Hotel Room Type
# -----------------------------
"""
CREATE TABLE Ref_Hotel_Room_Type (
    room_type_code varchar(10) NOT NULL,
    room_type_description varchar(50) NOT NULL
);
"""


df_room_type_list = pd.read_table(os.path.join(data_dir, 'RoomTypeList.txt'), sep="|", index_col=False)
room_types_ctr = Counter(df_room_type_list.RoomTypeName.tolist())

room_types_most_common = room_types_ctr.most_common(1000)
sum_val = sum([k[1] for k in room_types_most_common]) * 1.0
result_rows = []
START_ID = 887878
start_ctr = 0
for each_val in room_types_most_common:
    temp_dict = {
        'room_type_code': START_ID + start_ctr,
        'room_type_description': each_val[0],
        'room_type_prob': each_val[1]/ sum_val,
    }
    result_rows.append(temp_dict)
    start_ctr += 1

# Create data frame
ref_hotel_room_type_df = pd.DataFrame.from_records(result_rows)

# Store data frame
ref_hotel_room_type_df[['room_type_code', 'room_type_description']].to_pickle(os.path.join(store_into, 'ref_hotel_room_type.pkl'))
pickle.dump([ref_hotel_room_type_df.room_type_code.values.tolist(), ref_hotel_room_type_df.room_type_prob.values.tolist()], open(os.path.join(store_into, 'room_type_distr.pkl'), 'wb'), -1)


