from typing import Tuple, Any

import pandas
import pandas as pd
import streamlit as st


# Function to read the CSV file and convert it to a pandas DataFrame
def read_airports_csv(file_path: str) -> pd.DataFrame:
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return None


# def find_midpoint(x1, y1, x2, y2) -> (float, float):
#     midpoint_x = x1 + x2 / 2
#     midpoint_y = y1 + y2 / 2
#     return midpoint_x, midpoint_y


def find_distance_and_midpoint(x1: float, y1: float, x2: float, y2: float) -> tuple[float | Any, float, float]:
    distance_x = max(x1, x2) - min(x1, x2)
    midpoint_x = (min(x1, x2) + distance_x / 2)
    if distance_x >= 180:
        distance_x = 360 - distance_x
        midpoint_x = (min(x1, x2) - distance_x / 2)
    distance_y = max(y1, y2) - min(y1, y2)
    midpoint_y = min(y1, y2) + distance_y / 2
    print(f"The distance x is {distance_x/2}")
    if distance_y >= 90:
        distance_y = 180 - distance_y
        midpoint_y = min(y1, y2) - distance_y / 2
    print(f"The distance y is {distance_y/2}")
    return (distance_y ** 2 + distance_x ** 2) ** 0.5 / 2, midpoint_x, midpoint_y


def is_in_circle(query_x, query_y, origin_x, origin_y, radius) -> bool:
    if find_distance_and_midpoint(query_x, query_y, origin_x, origin_y)[0] <= radius:
        return True
    else:
        return False


# Path to the sample CSV file
file_path = "processed_airports.csv"

# Read the CSV and convert it to a pandas DataFrame
all_airports_df = read_airports_csv(file_path)
readable = [f"{airport_name} ({iata_code})" for airport_name, iata_code in
            zip(all_airports_df['Name'], all_airports_df['IATA'])]

departing_airport_readable = st.selectbox("Departing City", readable, index=None)
arriving_airport_readable = st.selectbox("Arriving City", readable, index=None)
user_date = st.date_input("When do you wish to leave?", value="default_value_today")
if departing_airport_readable and departing_airport_readable == arriving_airport_readable:
    st.subheader("Departing city and destination city must be different")
    st.map(
        all_airports_df.query(f"IATA in ['{departing_airport_readable[-4:-1]}', '{arriving_airport_readable[-4:-1]}']"))
elif departing_airport_readable and arriving_airport_readable:
    st.subheader(f"Finding path from {departing_airport_readable} to {arriving_airport_readable}")
    departing_iata = departing_airport_readable[-4:-1]
    arriving_iata = arriving_airport_readable[-4:-1]
    #city = "CJU"
    flight_df = all_airports_df.query(f"IATA in ['{departing_iata}', '{arriving_iata}']")
    # TODO: Make this better by including going backward in other direction, Delete KWJ

    x1, y1 = flight_df.iloc[0]['LONGITUDE'], flight_df.iloc[0]['LATITUDE']
    x2, y2 = flight_df.iloc[1]['LONGITUDE'], flight_df.iloc[1]['LATITUDE']

    results = find_distance_and_midpoint(x1, y1, x2, y2)
    print(f"Location for departing city: {x1}, {y1}")
    print(f"Location for arriving city: {x2}, {y2}")
    mid_x, mid_y = results[1:]
    all_airports_df["color"] = all_airports_df['IATA'].apply(
        lambda row: "#000218" if row in [departing_iata, arriving_iata] else "#a9b2ff")
    st.write(f"{results[0]}")
    data = {"LONGITUDE" : [x1,x2,mid_x],
            "LATITUDE" : [y1,y2, mid_y]}
    df_midpoint = pandas.DataFrame(data)
    st.map(df_midpoint)
    radius = results[0] / 2
    num = 1780
    all_airports_df['in_circle'] = all_airports_df.apply(
        lambda row: is_in_circle(row['LONGITUDE'], row['LATITUDE'], mid_x, mid_y, radius), axis=1
    )
    st.write(all_airports_df)
    st.write(f"is {all_airports_df.iloc[num]['IATA']} in circle? {is_in_circle(all_airports_df.iloc[num]['LONGITUDE'],all_airports_df.iloc[num]['LATITUDE'],mid_x,mid_y,radius)}")
    st.map(all_airports_df.query("in_circle == True"), color="color")
else:
    st.map(all_airports_df)

# TODO: Implement API
