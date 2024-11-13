import pandas as pd
import streamlit as st
from funclib import find_distance_and_midpoint, is_in_circle, get_valid_heading, read_airports_csv
from graph import Flight, FlightGraph
from variables import list_of_popular_airports_100
import pydeck as pdk
import graphviz

# Path to the sample CSV file
file_path = "processed_airports.csv"
# Read the CSV and convert it to a pandas DataFrame
st.title("Cheapest Flight Finder")
all_airports_df = read_airports_csv(file_path)
# Create a readable format for the dropdown selections
readable = [f"{airport_name} ({iata_code})" for airport_name, iata_code in
            zip(all_airports_df['Name'], all_airports_df['IATA'])]
# User input for selecting departing and arriving airports

departing_airport_readable = st.selectbox("Departing City", readable, index=None, key=1)
arriving_airport_readable = st.selectbox("Arriving City", readable, index=None, key=2)

# User input for selecting the departure date
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
        popular_100_airport_filtered_df.drop(columns=['color', 'in_circle']),
        f"Displaying a map view of all of the popular airports in between {departing_airport_readable} and {arriving_airport_readable}", )
    st.map(popular_100_airport_filtered_df, color="color")
    st.write(
        f"The flight from {departing_airport_readable} to {arriving_airport_readable} is heading {results[3].upper()} bound.")
    st.write(
        f"Any flight in between that is heading opposite to {results[3].upper()} is filtered out.")
    edges_raw = get_valid_heading(departing_iata, arriving_iata, popular_100_airport_filtered_df)
    # edges is tuple containing (source, destination, price)
    edges = edges_raw[0]
    # graph is graphviz digraph
    graph = edges_raw[1]
    edges_df = pd.DataFrame(edges, columns=['Departure', 'Arrival', 'Price'])
    st.subheader("Showing a table of all possible paths")
    # reconstructing edges_df to use pydeck
    st.write(edges_df)
    edges_df = edges_df.merge(popular_100_airport_filtered_df, left_on='Departure', right_on='IATA')
    edges_df = edges_df.rename(
        columns={'LONGITUDE': 'departure_lon', 'LATITUDE': 'departure_lat', 'Name': 'departure_name'})
    edges_df = edges_df.drop(columns=['Country', 'in_circle', 'color', 'IATA', 'City'])
    edges_df = edges_df.merge(popular_100_airport_filtered_df, left_on='Arrival', right_on='IATA')
    edges_df = edges_df.rename(
        columns={'LONGITUDE': 'arrival_lon', 'LATITUDE': 'arrival_lat', 'Name': 'arrival_name'})
    edges_df = edges_df.drop(columns=['Country', 'in_circle', 'color', 'IATA', 'City'])
    # Applying A* Algorithm, Nikhil can explain this part
    list_of_flights = [Flight(x[0], x[1], x[2]) for x in edges]
    airport_set = set()
    for f in list_of_flights:
        airport_set.add(f.source)
        airport_set.add(f.dest)
    airports = list(airport_set)
    airports.sort()
    flight_lst = FlightGraph(set(airports))
    for f in list_of_flights:
        flight_lst.update_flight(f)
    shortest_path = flight_lst.find_route(departing_iata, arriving_iata)
    graph_simple = graphviz.Digraph()
    graph_complex = graph.copy()
    valid_vertex = [elem.get_source() for elem in shortest_path]
    valid_edge_pattern = [f"{elem.get_source()} -> {elem.get_dest()}" for elem in shortest_path]
    # This colors the existing nodes, if there is a match from the A* algorithm
    counter = -1
    for nodes in graph_complex.body:
        counter += 1
        if f"{nodes.split()[0]} -> {nodes.split()[2]}" in valid_edge_pattern:
            label = nodes[:-2]
            graph_complex.body[counter] = (label + ' color="#FFA500" penwidth=4]')
    for elem in shortest_path:
        departure_location = elem.get_source()
        arriving_location = elem.get_dest()
        price = elem.get_price()
        edge_pattern = f"{departure_location} -> {arriving_location}"
        graph_simple.edge(departure_location, arriving_location, label=str(round(price, 2)), color="#FFA500",
                          penwidth="2")
    # https://www.geeksforgeeks.org/exploring-geospatial-data-with-pydeck-advanced-visualizations/
    # Using pydeck to display the edges in the map
    flight_layer = pdk.Layer(
        "GreatCircleLayer",
        edges_df,
        pickable=True,
        get_stroke_width=12,
        get_source_position=["departure_lon", "departure_lat"],  # Starting point of the arc
        get_target_position=["arrival_lon", "arrival_lat"],
        get_source_color=[64, 255, 0],
        get_target_color=[0, 128, 200],
        auto_highlight=True,
    )
    initial_view_state = pdk.ViewState(latitude=50, longitude=-40, zoom=0, bearing=0, pitch=0)

    flight_deck = pdk.Deck(
        map_style=None,
        layers=[flight_layer],
        initial_view_state=initial_view_state,
        tooltip={"text": "{departure_name} to {arrival_name} : ${Price}"},
    )

    flight_deck.picking_radius = 10
    st.subheader("Visualizing the connections on the map")
    st.pydeck_chart(flight_deck)
    if edges_df[edges_df.columns[0]].count() <= 400 and edges_df[edges_df.columns[0]].nunique() <= 200:
        # Get valid edges and graph representation for the possible paths max 200 Nodes; max 400 edges.
        # Sometimes it doesn't get displayed so there is else clause
        st.subheader("Displaying a graph of all possible paths")
        st.graphviz_chart(graph)
        st.subheader("Displaying the cheapest path using A* algorithm")
        st.graphviz_chart(graph_complex)
        st.subheader("Displaying the simple version")
        st.graphviz_chart(graph_simple)
    else:
        st.subheader(
            "Unable to display more than 400 edges in a graph! Displaying the cheapest path using A* algorithm in a simplified graph")
        st.graphviz_chart(graph_simple)
else:
    st.subheader("Displaying All Possible Airport Selections")
    st.map(all_airports_df, color="#737CA1")
