from dataclasses import dataclass


@dataclass()
class Place:
    name: str
    lat: float
    lon: float
    year: int


@dataclass()
class FamousPerson:
    birth_place: Place
    death_place: Place
    gender: str
    occupation: str
    name: str
