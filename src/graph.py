import heapq
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

from airport_locations import airport_distance


@dataclass
class Flight:
    """A flight from one airport to another"""

    source: str
    dest: str
    price: float

    def __str__(self) -> str:
        """Get string representation of a flight"""
        return f"Origin: {self.source}; Destination: {self.dest}"


class FlightGraph:
    """Graph containing flights between airports"""

    airports: List[str]
    flight_matrix: List[List[Optional[float]]]

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

        self.flight_matrix[row][col] = flight.price

    def __str__(self) -> str:
        """Get string representation of stored flights"""
        out = "Airports: "
        out += ", ".join(self.airports) + "\n"
        for idx, airport in enumerate(self.airports):
            out += f"\nFlights from {airport}:\n"
            for j, flight_data in enumerate(self.flight_matrix[idx]):
                if flight_data is not None:
                    out += (
                        f"Origin: {airport}; Destination: {self.airports[j]}\n"
                    )

        return out

    def find_route(self, start: str, end: str) -> Optional[List[str]]:
        if (start in self.airports) and (end in self.airports):
            airports_to_visit = [start]

            via_list: Dict[str, str] = {a: "" for a in self.airports}

            cumulative_weights: Dict[str, float] = {
                a: float("inf") for a in self.airports
            }
            cumulative_weights[start] = 0

            cumulative_weights_and_distances: Dict[str, float] = {
                a: float("inf") for a in self.airports
            }
            cumulative_weights_and_distances[start] = 0

            while airports_to_visit:
                current = heapq.heappop(airports_to_visit)

                row = self.airports.index(current)

                if current == end:
                    flight_plan = []

                    while current is not start:
                        origin = via_list[current]
                        row = self.airports.index(origin)
                        col = self.airports.index(current)
                        flight_plan.insert(
                            0,
                            Flight(
                                origin,
                                current,
                                self.flight_matrix[row][col],
                            ),
                        )
                        current = origin

                    return flight_plan

                dest_and_weights: List[Tuple[int, float]] = [
                    (self.airports[i], data)
                    for i, data in enumerate(self.flight_matrix[row])
                    if data
                ]

                for dest, weight in dest_and_weights:
                    new_cumulative_weight = (
                        cumulative_weights[current] or 0
                    ) + weight
                    if new_cumulative_weight < cumulative_weights[dest]:
                        via_list[dest] = current
                        cumulative_weights[dest] = new_cumulative_weight
                        cumulative_weights_and_distances[dest] = (
                            new_cumulative_weight
                            + airport_distance(current, dest)
                        )
                        heapq.heappush(airports_to_visit, dest)

        else:
            return None
