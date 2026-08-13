from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True, slots=True)
class Place:
    name: str
    lat: float
    lon: float
    year: int

    @classmethod
    def from_row(cls, row) -> "Place":
        return cls(
            name=row["bplace_name"],
            lat=row["bplace_lat"],
            lon=row["bplace_lon"],
            year=int(row["birthyear"]),
        )

class Gender(Enum):
    OTHER = 0
    MALE = 1
    FEMALE = 2


@dataclass(frozen=True, slots=True)
class FamousPerson:
    birth_place: Place
    death_place: Place
    gender: Gender
    occupation: str
    name: str

    @classmethod
    def from_row(cls, row) -> "FamousPerson":
        raw_gender = row["gender"]
        gender = Gender.OTHER
        match raw_gender:
            case "M":
                gender = Gender.MALE
            case "F":
                gender = Gender.FEMALE

        return cls(
            birth_place=Place.from_row(row),
            death_place=Place.from_row(row),
            gender=gender,
            occupation=row["occupation"],
            name=row["name"],
        )
