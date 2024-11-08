from typing import Any, Tuple, List
import random
import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup
import requests
import graphviz
from graphviz import Digraph


def read_airports_csv(file_path: str) -> pd.DataFrame or None:
    """
    Reads a CSV file containing airport data and loads it into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame or None: The DataFrame containing the data if read successfully,
                              or None if an error occurs.
    """

from typing import Any
import pandas as pd
import requests


def read_airports_csv(file_path: str) -> pd.DataFrame:
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return None


def find_distance_and_midpoint(x1: float, y1: float, x2: float, y2: float) -> tuple[float | Any, float, float, str]:
    """
      Calculates the distance, midpoint, and heading between two geographical points.

      Args:
          x1 (float): Longitude of the first point.
          y1 (float): Latitude of the first point.
          x2 (float): Longitude of the second point.
          y2 (float): Latitude of the second point.

      Returns:
          tuple: A tuple containing:
                 - The half-distance between the points (float),
                 - The longitude of the midpoint (float),
                 - The latitude of the midpoint (float),
                 - The primary heading direction (str).
      """
    distance_x = max(x1, x2) - min(x1, x2)
    midpoint_x = (min(x1, x2) + distance_x / 2)
    heading_horizontal = "east" if x2 > x1 else "west"
    if distance_x >= 180:
        distance_x = 360 - distance_x
        midpoint_x = (min(x1, x2) - distance_x / 2)
        heading_horizontal = "west" if heading_horizontal == "east" else "east"
    distance_y = max(y1, y2) - min(y1, y2)
    midpoint_y = min(y1, y2) + distance_y / 2
    heading_vertical = "south" if y1 > y2 else "north"
    if distance_y >= 90:
        distance_y = 180 - distance_y
        midpoint_y = min(y1, y2) - distance_y / 2
        heading_vertical = "south" if heading_vertical == "north" else "north"
    main_heading = heading_horizontal if distance_x >= distance_y else heading_vertical
    return (distance_y ** 2 + distance_x ** 2) ** 0.5 / 2, midpoint_x, midpoint_y, main_heading


def is_in_circle(query_x: float, query_y: float, origin_x: float, origin_y: float, radius: float) -> bool:
    """
    Determines if a query point is within a given radius from an origin point.

    Args:
        query_x (float): Longitude of the query point.
        query_y (float): Latitude of the query point.
        origin_x (float): Longitude of the origin point.
        origin_y (float): Latitude of the origin point.
        radius (float): Radius distance for comparison.

    Returns:
        bool: True if the query point is within the radius, False otherwise.
    """
=======
def find_distance_and_midpoint(x1: float, y1: float, x2: float, y2: float) -> tuple[float | Any, float, float]:
    distance_x = max(x1, x2) - min(x1, x2)
    midpoint_x = (min(x1, x2) + distance_x / 2)
    if distance_x >= 180:
        distance_x = 360 - distance_x
        midpoint_x = (min(x1, x2) - distance_x / 2)
    distance_y = max(y1, y2) - min(y1, y2)
    midpoint_y = min(y1, y2) + distance_y / 2
    if distance_y >= 90:
        distance_y = 180 - distance_y
        midpoint_y = min(y1, y2) - distance_y / 2
    return (distance_y ** 2 + distance_x ** 2) ** 0.5 / 2, midpoint_x, midpoint_y


def is_in_circle(query_x, query_y, origin_x, origin_y, radius) -> bool:
    if find_distance_and_midpoint(query_x, query_y, origin_x, origin_y)[0] <= radius:
        return True
    else:
        return False


# if suitable api is found replace this
def generate_price(distance: float) -> float:
    """
    Generates a random price based on the distance. Currently, it generates random value based on the distance. However,
    If there are good APIs, I will implement API in this function.

    Args:
        distance (float): The distance value to base the price on.

    Returns:
        float: The generated price, calculated as a random multiplier of the distance.
    """
    #TODO: Find and Implement API
    return distance * random.uniform(12, 18)


def get_valid_heading(departing_iata: str, arriving_iata: str, in_circle_df: pd.DataFrame)-> tuple[
    list[tuple[Any, Any, float]], Digraph]:
    """
    Generates a list of valid route edges between airports and creates a graph visualization.

    Args:
        departing_iata (str): The IATA code of the departing airport.
        arriving_iata (str): The IATA code of the arriving airport.
        in_circle_df (pd.DataFrame): A DataFrame containing airport data within a given radius.

    Returns:
        tuple: A tuple containing:
               - A list of valid edges (list of tuples),
               - A Graphviz Digraph object representing the graph.
    """
    departure_row = in_circle_df.loc[in_circle_df['IATA'] == departing_iata]
    arrival_row = in_circle_df.loc[in_circle_df['IATA'] == arriving_iata]
    x1, y1 = departure_row.iloc[0]['LONGITUDE'], departure_row.iloc[0]['LATITUDE']
    x2, y2 = arrival_row.iloc[0]['LONGITUDE'], arrival_row.iloc[0]['LATITUDE']
    initial_heading = find_distance_and_midpoint(x1, y1, x2, y2)[3]
    list_of_valid_edges = []
    graph = graphviz.Digraph()
    if initial_heading == "north":
        opposite_heading = "south"
    elif initial_heading == "south":
        opposite_heading = "north"
    elif initial_heading == "east":
        opposite_heading = "west"
    else:
        opposite_heading = "east"
    for outer in in_circle_df['IATA']:
        if outer == arriving_iata:
            graph.node(outer, outer, color='#000218')
            continue
        elif outer == departing_iata:
            graph.node(outer, outer, color='#000218')
        else:
            graph.node(outer, outer, color='#FFA500')
        departure_row_in_loop = in_circle_df.loc[in_circle_df['IATA'] == outer]
        x1, y1 = departure_row_in_loop.iloc[0]['LONGITUDE'], departure_row_in_loop.iloc[0]['LATITUDE']
        for inner in in_circle_df['IATA']:
            arrival_row_in_loop = in_circle_df.loc[in_circle_df['IATA'] == inner]
            x2, y2 = arrival_row_in_loop.iloc[0]['LONGITUDE'], arrival_row_in_loop.iloc[0]['LATITUDE']
            result = find_distance_and_midpoint(x1, y1, x2, y2)
            distance, heading = result[0], result[3]
            if heading != opposite_heading and outer != inner and inner != departing_iata:
                price = generate_price(distance)
                graph.edge(outer,inner, label = str(round(price,2)))
                list_of_valid_edges.append((outer, inner, round(price, 2)))
    return list_of_valid_edges, graph
def getHTMLdocument(url):
    """
    from https://www.geeksforgeeks.org/beautifulsoup-scraping-link-from-html/
    :param url:
    :return:
    """
    # request for HTML document of given url
    response = requests.get(url)
    # response will be provided in JSON format
    return response.text
