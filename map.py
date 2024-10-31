import pandas as pd
import streamlit as st
from variables import *
from funclib import *

# Function to read the CSV file and convert it to a pandas DataFrame

# Path to the sample CSV file
file_path = "processed_airports.csv"
# Read the CSV and convert it to a pandas DataFrame
st.title("Path Finder")
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
    departing_iata = departing_airport_readable[-4:-1]
    arriving_iata = arriving_airport_readable[-4:-1]
    # city = "CJU"
    flight_df = all_airports_df.query(f"IATA in ['{departing_iata}', '{arriving_iata}']")
    # TODO: Make this better by including going backward in other direction, Delete KWJ

    x1, y1 = flight_df.iloc[0]['LONGITUDE'], flight_df.iloc[0]['LATITUDE']
    x2, y2 = flight_df.iloc[1]['LONGITUDE'], flight_df.iloc[1]['LATITUDE']

    results = find_distance_and_midpoint(x1, y1, x2, y2)
    mid_x, mid_y = results[1:]
    st.write(f"Finding the midpoint between {departing_airport_readable} and {arriving_airport_readable}")
    data = {"LONGITUDE": [x1, x2, mid_x],
            "LATITUDE": [y1, y2, mid_y]}

    df_midpoint = pd.DataFrame(data)
    df_midpoint["color"] = df_midpoint['LONGITUDE'].apply(
        lambda row: "#000218" if row in [x1, x2] else "#FF2400")
    st.map(df_midpoint, color = "color")
    popular_100_airport_df = all_airports_df.query(
        f"IATA in @list_of_popular_airports_100 or IATA == '{arriving_iata}' or IATA == '{departing_iata}'").copy()
    popular_100_airport_df["color"] = popular_100_airport_df['IATA'].apply(
        lambda row: "#000218" if row in [departing_iata, arriving_iata] else "#FFA500")
    popular_100_airport_df['in_circle'] = popular_100_airport_df.apply(
        lambda row: is_in_circle(row['LONGITUDE'], row['LATITUDE'], mid_x, mid_y, results[0] * 0.501), axis=1
    )
    # st.write(all_airports_df)
    # st.write(
    #     f"is {all_airports_df.iloc[num]['IATA']} in circle? {is_in_circle(all_airports_df.iloc[num]['LONGITUDE'], all_airports_df.iloc[num]['LATITUDE'], mid_x, mid_y, radius)}")
    st.write(
        f"Have located all of popular airports in between {departing_airport_readable} and {arriving_airport_readable}",
        popular_100_airport_df.query("in_circle == True")["Name"], f"Displaying a map view")
    st.map(popular_100_airport_df.query("in_circle == True"), color="color")

else:
    st.map(all_airports_df)

# TODO: Implement API, Eliminate the nodes without direct flights
