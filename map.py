import pandas as pd
import streamlit as st
from variables import *
from funclib import *
import networkx as nx
import matplotlib.pyplot as plt

# Function to read the CSV file and convert it to a pandas DataFrame

# Path to the sample CSV file
file_path = "processed_airports.csv"
# Read the CSV and convert it to a pandas DataFrame
st.title("Path Finder")
all_airports_df = read_airports_csv(file_path)
# Create a readable format for the dropdown selections
readable = [f"{airport_name} ({iata_code})" for airport_name, iata_code in
            zip(all_airports_df['Name'], all_airports_df['IATA'])]
# User input for selecting departing and arriving airports
departing_airport_readable = st.selectbox("Departing City", readable, index=None)
arriving_airport_readable = st.selectbox("Arriving City", readable, index=None)
# User input for selecting the departure date
user_date = st.date_input("When do you wish to leave?", value="default_value_today")
# Check if the departing and arriving airports are the same
if departing_airport_readable and departing_airport_readable == arriving_airport_readable:
    st.subheader("Departing city and destination city must be different")
    # Display a map with only the selected airport highlighted
    st.map(
        all_airports_df.query(f"IATA in ['{departing_airport_readable[-4:-1]}', '{arriving_airport_readable[-4:-1]}']"))
elif departing_airport_readable and arriving_airport_readable:
    # Extract IATA codes from the selected options for ex. Hong Kong -> HKG
    departing_iata = departing_airport_readable[-4:-1]
    arriving_iata = arriving_airport_readable[-4:-1]
    # Get coordinates for the departure and arrival airports
    departure_row = all_airports_df.loc[all_airports_df['IATA'] == departing_iata]
    arrival_row = all_airports_df.loc[all_airports_df['IATA'] == arriving_iata]
    x1, y1 = departure_row.iloc[0]['LONGITUDE'], departure_row.iloc[0]['LATITUDE']
    x2, y2 = arrival_row.iloc[0]['LONGITUDE'], arrival_row.iloc[0]['LATITUDE']
    # Find distance and midpoint between the two airports
    results = find_distance_and_midpoint(x1, y1, x2, y2)
    mid_x, mid_y = results[1:3]
    st.write(f"Finding the midpoint between {departing_airport_readable} and {arriving_airport_readable}")
    data = {"LONGITUDE": [x1, x2, mid_x],
            "LATITUDE": [y1, y2, mid_y]}
    df_midpoint = pd.DataFrame(data)
    # Applying different color to the midpoint
    df_midpoint["color"] = df_midpoint['LONGITUDE'].apply(
        lambda row: "#000218" if row in [x1, x2] else "#FF2400")
    st.map(df_midpoint, color="color")
    # Creating a list of 100 popular airports + departure and arrival airports
    popular_100_airport_df = all_airports_df.query(
        f"IATA in @list_of_popular_airports_100 or IATA == '{arriving_iata}' or IATA == '{departing_iata}'").copy()
    # Determine which airports are within the circle defined by the midpoint and distance
    popular_100_airport_df['in_circle'] = popular_100_airport_df.apply(
        lambda row: is_in_circle(row['LONGITUDE'], row['LATITUDE'], mid_x, mid_y, results[0] * 0.501), axis=1
    )
    # Filter 100 popular airports along with the departure and arrival airports
    popular_100_airport_filtered_df = popular_100_airport_df.query("in_circle == True")
    popular_100_airport_filtered_df["color"] = popular_100_airport_filtered_df['IATA'].apply(
        lambda row: "#000218" if row in [departing_iata, arriving_iata] else "#FFA500")
    # Display filtered airport data and the maps
    st.write(
        f"Have located all of popular airports in between {departing_airport_readable} and {arriving_airport_readable}",
        popular_100_airport_filtered_df.drop(columns=['color', 'in_circle']), f"Displaying a map view")
    st.map(popular_100_airport_filtered_df, color="color")
    st.write(
        f"The flight from {departing_airport_readable} to {arriving_airport_readable} is heading {results[3]} bound.")
    st.write(popular_100_airport_filtered_df)
    edges_raw = get_valid_heading(departing_iata, arriving_iata, popular_100_airport_filtered_df)
    edges = edges_raw[0]
    graph = edges_raw[1]
    edges_df = pd.DataFrame(edges)
    st.subheader("Showing a table of all of possibilities")
    st.write(edges_df)
    if edges_df[edges_df.columns[0]].count() <= 400 and edges_df[edges_df.columns[0]].nunique() <= 200:
        # Get valid edges and graph representation for the possible paths max 200 Nodes; max 400 edges.
        # Sometimes it doesn't get displayed
        st.subheader("Displaying a graph of all of possibilities")
        st.graphviz_chart(graph)

    # Below is from chatGPT, I was trying to visualize the graph in different way.
    # if st.button("Generate"):
    #     G = nx.DiGraph()
    #
    #     # Add edges with weights
    #     for departing_city, arriving_city, price in edges:
    #         G.add_edge(departing_city, arriving_city, weight=price)
    #
    #     # Get edge weights for display
    #     edge_labels = {(u, v): f'${d["weight"]}' for u, v, d in G.edges(data=True)}
    #
    #     # Adjust layout to space nodes
    #     pos = nx.spring_layout(G, k=2, seed=42)  # Increase `k` to spread nodes out
    #
    #     plt.figure(figsize=(12, 10))
    #     nx.draw(G, pos, with_labels=True, node_size=2000, node_color='orange', font_size=10, font_weight='bold',
    #             edge_color='black', arrowsize=20)
    #     nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black')
    #
    #     plt.title('City Connections with Prices (Spaced Out)')
    #     plt.savefig('graph_output.png')
else:
    st.map(all_airports_df)

# TODO: Implement API, Eliminate the nodes without direct flights
