from dataclasses import dataclass
from typing import Set, List, Optional, Dict
import heapq

@dataclass
class FlightData:
    """Data related to a flight that is used for weighting"""

    price: float

    def weight(self) -> float:
        return self.price


@dataclass
class Flight:
    """A flight from one airport to another"""

    source: str
    dest: str
    data: FlightData

    def __str__(self) -> str:
        """Get string representation of a flight"""
        return f"Origin: {self.source}; Destination: {self.dest}"


class FlightGraph:
    """Graph containing flights between airports"""

    airports: List[str]
    flight_matrix: List[List[Optional[FlightData]]]

    def __init__(self, airports: Set[str]) -> None:
        """Initialize a graph using a set of airports"""
        self.airports = list(airports)
        # Sort to ensure consistent ordering of airports - important for
        # test cases
        self.airports.sort()

        self.flight_matrix = [[None for x in airports] for y in airports]

    def update_flight(self, flight: Flight):
        """Update the data for a flight"""
        row = self.airports.index(flight.source)
        col = self.airports.index(flight.dest)

        self.flight_matrix[row][col] = flight.data

    def __str__(self) -> str:
        """Get string representation of stored flights"""
        out = "Airports: "
        out += ", ".join(self.airports) + "\n"
        for idx, airport in enumerate(self.airports):
            out += f"\nFlights from {airport}:\n"
            for j, flight_data in enumerate(self.flight_matrix[idx]):
                if flight_data is not None:
                    # fmt: off
                    out += (
                            f"Origin: {airport}; "
                            f"Destination: {self.airports[j]}\n"
                    )
                    # fmt: on

        return out

    def find_route(self, start: str, end: str):
        if (start in self.airports) and (end in self.airports):
            visited = []
            airports_to_visit = heapq.heapify([start])

            flight_path = []

            weights_to_dest: Dict[str, Optional[float]] = {a: None for a in self.airports}
            weights_to_dest[start] = 0

            weights_and_distance_to_dest: Dict[str, Optional[float]] = {a: None for a in self.airports}
            weights_and_distance_to_dest[start] =

            while airports_to_visit:
                current = heapq.heappop(airports_to_visit)

                row = self.airports.index(current)
                if current == end:
                    return flight_path

                for flight in self.flight_matrix[row]:

        else:
            return None
