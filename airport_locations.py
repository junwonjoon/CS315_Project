from typing import Tuple

from geopy.distance import distance

from funclib import read_airports_csv

df = read_airports_csv("processed_airports.csv")


def airport_location(iata_code: str) -> Tuple[float, float]:
    """Determine the location of an airport from its IATA code"""
    entry = df.loc[df["IATA"] == iata_code]
    lon, lat = entry.iloc[0]["LONGITUDE"], entry.iloc[0]["LATITUDE"]

    return (lat, lon)


def airport_distance(iata_code1: str, iata_code2: str) -> float:
    """Determine the distance between two airports from their IATA codes"""
    return distance(
        airport_location(iata_code1), airport_location(iata_code2)
    ).km
