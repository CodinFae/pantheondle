from dataclasses import dataclass
from enum import Enum
from typing import TypedDict


class PersonRow(TypedDict):
    bplace_name: str
    bplace_lat: float
    bplace_lon: float
    birthyear: int
    dplace_name: str
    dplace_lat: float
    dplace_lon: float
    deathyear: int
    gender: str
    occupation: str
    name: str


@dataclass(frozen=True, slots=True)
class LifeEvent:
    name: str
    lat: float
    lon: float
    year: int

    @classmethod
    def birth_from_row(cls, row: PersonRow) -> "LifeEvent":
        return cls(
            name=row["bplace_name"],
            lat=row["bplace_lat"],
            lon=row["bplace_lon"],
            year=int(row["birthyear"]),
        )

    @classmethod
    def death_from_row(cls, row: PersonRow) -> "LifeEvent":
        return cls(
            name=row["dplace_name"],
            lat=row["dplace_lat"],
            lon=row["dplace_lon"],
            year=int(row["deathyear"]),
        )


class Gender(Enum):
    OTHER = 0
    MALE = 1
    FEMALE = 2


@dataclass(frozen=True, slots=True)
class FamousPerson:
    birth: LifeEvent
    death: LifeEvent
    gender: Gender
    occupation: str
    name: str

    @classmethod
    def from_row(cls, row: PersonRow) -> "FamousPerson":
        raw_gender = row["gender"]
        gender = Gender.OTHER
        match raw_gender:
            case "M":
                gender = Gender.MALE
            case "F":
                gender = Gender.FEMALE

        return cls(
            birth_place=LifeEvent.birth_from_row(row),
            death_place=LifeEvent.death_from_row(row),
            gender=gender,
            occupation=row["occupation"],
            name=row["name"],
        )
