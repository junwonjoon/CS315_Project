from node import FlightGraph, Flight
import pytest
from typing import List


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


def generate_string_from_flights(flights: List[Flight]) -> str:
    """Generate the FlightGraph string from a list of flights"""
    out = ""

    airport_set = set()

    for f in flights:
        airport_set.add(f.source)
        airport_set.add(f.dest)

    airports = list(airport_set)
    airports.sort()

    out = "Airports: "
    out += ", ".join(airports) + "\n"

    for a in airports:
        outgoing_flighs = [f for f in flights if f.source == a]
        out += f"\nFlights from {a}:\n"
        for f in outgoing_flighs:
            out += str(f) + "\n"

    return out


def test_helper_fn(single_flight, single_flight_string):
    """Verify that generate_string_from_flights behaves correctly"""
    assert generate_string_from_flights([single_flight]) == single_flight_string


def test_update_1_flight(single_flight, single_flight_string):
    """Test FlightGraph.update_flight function"""
    flight_lst = FlightGraph(set([single_flight.source, single_flight.dest]))
    flight_lst.update_flight(single_flight)
    assert str(flight_lst) == single_flight_string


def test_init():
    """Verify that FlightGraph initializer initializes airports"""
    flight_lst = FlightGraph(set(["PHX", "LAS"]))
    assert (
        str(flight_lst)
        == "Airports: LAS, PHX\n\nFlights from LAS:\n\nFlights from PHX:\n"
    )
