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

    def find_route(self, start: str, end: str) -> list[Flight] | None:
        """Determine the best set of flights between two airports"""
        # Make sure both airports are in the graph
        if (start in self.airports) and (end in self.airports):
            # Queue of airports to visit
            airports_to_visit = [(0, start)]
            # Ideal originating airport for each airport
            via_table: Dict[str, str] = {a: "" for a in self.airports}

            # The cumulative price for flights to get to an airport
            total_price: Dict[str, float] = {
                a: float("inf") for a in self.airports
            }
            total_price[start] = 0

            # Cumulative price + the A* heuristic - in this case, distance
            total_price_plus_distances: Dict[str, float] = {
                a: float("inf") for a in self.airports
            }
            total_price_plus_distances[start] = airport_distance(start, end)

            # While we have airports to visit
            while airports_to_visit:
                # Get current airport
                _, current = heapq.heappop(airports_to_visit)

                row = self.airports.index(current)

                if current == end:
                    # If we've reached the destination, reconstruct set of
                    # flights needed to get to the destination from the source
                    flight_plan = []

                    while current is not start:
                        # Build list of flights to get to the destination
                        origin = via_table[current]
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

                # Get all destinations for flights from this airport
                dest_and_weights: List[Tuple[int, float]] = [
                    (self.airports[i], data)
                    for i, data in enumerate(self.flight_matrix[row])
                    if data
                ]

                for dest, weight in dest_and_weights:
                    new_total_price = (total_price[current]) + weight
                    if new_total_price < total_price[dest]:
                        # If the new total price is cheaper than what's
                        # recorded update the route for this airport to use
                        # the originating airport
                        via_table[dest] = current
                        total_price[dest] = new_total_price
                        total_price_plus_distances[dest] = (
                                new_total_price + airport_distance(current, dest)
                        )

                        # If we don't currently plan to visit this airport, add
                        # it to the list
                        if not any(
                                [d == dest for (_, d) in airports_to_visit]
                        ):
                            heapq.heappush(
                                airports_to_visit,
                                (total_price_plus_distances[dest], dest),
                            )

        return None
