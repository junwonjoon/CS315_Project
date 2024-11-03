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