from graph import FlightGraph, Flight
import pytest
from typing import List, Set


@pytest.fixture
def single_flight() -> Flight:
    """Return a single flight object"""
    return Flight("PHX", "LAS", (5.99))


@pytest.fixture
def single_flight_string() -> str:
    """Return FlightGraph String from single_flight fixture in Graph"""
    # fmt: off
    return (
        "Airports: LAS, PHX\n"
        "\n"
        "Flights from LAS:\n"
        "\n"
        "Flights from PHX:\n"
        "Origin: PHX; Destination: LAS\n"
    )
    # fmt: on

@pytest.fixture
def example_flights():
    return [
        Flight("PHX", "LAS", (5.99)),
        Flight("JFK", "MDW", (12.99)),
        Flight("LAS", "MDW", (15.99)),
        Flight("PHX", "JFK", (17.99)),
        Flight("PHX", "MDW", (13.99))
    ]

def generate_airports_from_flights(flights: List[Flight]) -> List[str]:
    airport_set = set()

    for f in flights:
        airport_set.add(f.source)
        airport_set.add(f.dest)

    airports = list(airport_set)
    airports.sort()

    return airports



def generate_flightgraph_string(flights: List[Flight], airports: List[str]) -> str:
    """Generate the FlightGraph string from a list of flights"""
    out = ""

    out = "Airports: "
    out += ", ".join(airports) + "\n"

    for a in airports:
        outgoing_flighs = [f for f in flights if f.source == a]

        outgoing_flighs.sort(key=lambda f: str(f))

        out += f"\nFlights from {a}:\n"
        for f in outgoing_flighs:
            out += str(f) + "\n"

    return out


def test_helper_fn(single_flight, single_flight_string):
    """Verify that generate_string_from_flights behaves correctly"""
    assert generate_flightgraph_string([single_flight], generate_airports_from_flights([single_flight])) == single_flight_string


def test_update_1_flight(single_flight, single_flight_string):
    """Test FlightGraph.update_flight function with a single flight"""
    flight_lst = FlightGraph(set([single_flight.source, single_flight.dest]))
    flight_lst.update_flight(single_flight)
    assert str(flight_lst) == single_flight_string


def test_update_flight(example_flights):
    """Test Flightgraph.update_flight function"""
    airports = generate_airports_from_flights(example_flights)

    flight_lst = FlightGraph(set(airports))
    for f in example_flights:
        flight_lst.update_flight(f)

    print(flight_lst.airports)
    assert str(flight_lst) == generate_flightgraph_string(example_flights, airports)


def test_init():
    """Verify that FlightGraph initializer initializes airports"""
    flight_lst = FlightGraph(set(["PHX", "LAS"]))
    assert (
        str(flight_lst)
        == "Airports: LAS, PHX\n\nFlights from LAS:\n\nFlights from PHX:\n"
    )