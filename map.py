import pandas as pd
import streamlit as st


# Function to read the CSV file and convert it to a pandas DataFrame
def read_airports_csv(file_path:str) -> pd.DataFrame:
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return None

def find_midpoint(df:pd.DataFrame)-> (float, float):
    left_most, right_most = df['LONGITUDE'].min(), df['LONGITUDE'].max()
    upper, lower = df['LATITUDE'].max(), df['LATITUDE'].min()
    if (right_most - left_most) <= 180:
        midpoint_horizontal = (right_most - left_most) / 2
    else:
        midpoint_horizontal = ((left_most+360)- right_most) / 2
    if (upper - lower) <= 180:
        midpoint_vertical = (upper - lower) / 2
    else:
        midpoint_vertical = ((lower+360)- upper) / 2
    return (midpoint_horizontal, midpoint_vertical)

def find_distance(x1, y1, x2, y2)-> float:

    if abs(x1 - x2) <= 180:
        distance_horizontal = (x1 - x2)
    else:
        distance_horizontal = ((x2 + 360) - x1)
    if abs(upper - lower) <= 180:
        distance_vertical = (upper - lower)
    else:
        distance_vertical = ((lower + 360) - upper)
    return (distance_vertical ** 2 + distance_horizontal ** 2) ** 0.5 / 2 + 1
def is_in_circle(df:pd.DataFrame, long, lat)-> bool:
    x, y = find_midpoint(df)


# Path to the sample CSV file
file_path = "processed_airports.csv"

# Read the CSV and convert it to a pandas DataFrame
all_airports_df = read_airports_csv(file_path)
readable = [f"{airport_name} ({iata_code})" for airport_name, iata_code in
            zip(all_airports_df['Name'], all_airports_df['IATA'])]

departing_airport_readable = st.selectbox("Departing City", readable, index=None)
arriving_airport_readable = st.selectbox("Arriving City", readable, index=None)
user_date = st.date_input("When do you wish to leave?", value="default_value_today")

if departing_airport_readable and arriving_airport_readable:
    st.subheader(f"Finding path from {departing_airport_readable} to {arriving_airport_readable}")
    departing_iata = departing_airport_readable[-4:-1]
    arriving_iata = arriving_airport_readable[-4:-1]
    flight_df = all_airports_df.query(f"IATA in ['{departing_iata}', '{arriving_iata}']")
    # TODO: Make this better by including going backward in other direction

    x2, x1 = flight_df['LONGITUDE'].min(), flight_df['LONGITUDE'].max()
    upper, lower = flight_df['LATITUDE'].max(), flight_df['LATITUDE'].min()
    all_airports_df["color"] = all_airports_df['IATA'].apply(
        lambda row: "#000218" if row in [departing_iata, arriving_iata] else "#a9b2ff")
    st.map(all_airports_df.query(
        f"LONGITUDE >= {x2} and LONGITUDE <= {x1} and LATITUDE >= {lower} and LATITUDE <= {upper}"), color ='color')
else:
    st.map(all_airports_df)


#TODO: Implement API