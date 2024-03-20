import sqlite3
import time

import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Open the SQLite database
conn = sqlite3.connect('nuremberg_stops_immoscout.sqlite')

table_immoscout = "immoscout"

# Read data from the database into a DataFrame
df_immoscout = pd.read_sql_query(f'SELECT * FROM {table_immoscout}',
                                 conn)  # Replace "table_name" with the actual table name in the database

# Create a geocoder instance
geolocator = Nominatim(user_agent="my_app", timeout=10)

# Initialize lists to store latitude and longitude values
latitudes = []
longitudes = []

# Iterate over each row in the DataFrame
for index, row in df_immoscout.iterrows():
    try:

        # Construct the address using the available columns from the DataFrame
        address = f"{row['houseNumber']} {row['street']}, {row['cityTown']}, {row['district']}, {row['zipCode']} , {row['federalState']}"

        # Geocode the address to retrieve latitude and longitude
        location = geolocator.geocode(address)

        # Check if location was found
        if location is not None:
            latitudes.append(location.latitude)
            longitudes.append(location.longitude)
            print(address, ":", location.latitude, location.longitude)
        else:
            latitudes.append(None)
            longitudes.append(None)

    except GeocoderTimedOut:
        print(f"Geocoding timed out for: {address}. Skipping.")
        latitudes.append(None)
        longitudes.append(None)

# Add latitude and longitude columns to the DataFrame
df_immoscout['latitude'] = latitudes
df_immoscout['longitude'] = longitudes

# Save the updated DataFrame back to the database
df_immoscout.to_sql(table_immoscout, conn, if_exists='replace',
                    index=False)

# Close the database connection
conn.close()
