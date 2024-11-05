from typing import Tuple

from geopy.distance import distance


def airport_location(iata_code: str) -> Tuple[float, float]:
    # TODO
    #
    #
    location = (50, 50)

    return location


def airport_distance(iata_code1: str, iata_code2: str) -> float:
    return distance(
        airport_location(iata_code1), airport_location(iata_code2)
    ).km
