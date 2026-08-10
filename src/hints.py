import re
from abc import abstractmethod
from enum import Enum

from pydantic.dataclasses import dataclass

from src.person import FamousPerson


@dataclass(slots=True, frozen=True)
class Hint:
    @classmethod
    @abstractmethod
    def from_person(cls, person: FamousPerson) -> "Hint": ...


@dataclass(slots=True, frozen=True)
class MapHint(Hint): ...


@dataclass(slots=True, frozen=True)
class CitiesHint(Hint):
    birth_city: str
    death_city: str

    @classmethod
    def from_person(cls, person: FamousPerson) -> "CitiesHint":
        return cls(
            birth_city=person.birth_place.name, death_city=person.death_place.name
        )


@dataclass(slots=True, frozen=True)
class DatesHint(Hint):
    birth_year: int
    death_year: int

    @classmethod
    def from_person(cls, person: FamousPerson) -> "DatesHint":
        return cls(
            birth_year=int(person.birth_place.year),
            death_year=int(person.death_place.year),
        )


class Gender(Enum):
    OTHER = 0
    MALE = 1
    FEMALE = 2


@dataclass(slots=True, frozen=True)
class GenderHint(Hint):
    gender: Gender

    @classmethod
    def from_person(cls, person: FamousPerson) -> "GenderHint":
        raw_gender = person.gender
        gender = Gender.OTHER
        match raw_gender:
            case "M":
                gender = Gender.MALE
            case "F":
                gender = Gender.FEMALE
        return cls(gender=gender)


@dataclass(slots=True, frozen=True)
class OccupationHint(Hint):
    occupation: str

    @classmethod
    def from_person(cls, person: FamousPerson) -> "OccupationHint":
        return cls(occupation=person.occupation)


@dataclass(slots=True, frozen=True)
class HiddenNameHint(Hint):
    name: str

    @classmethod
    def from_person(cls, person: FamousPerson) -> "HiddenNameHint":
        return cls(name=re.sub("[a-zA-Z]", "_", person.name))
