import re
from dataclasses import dataclass

from pantheondle.model.person import FamousPerson, Gender


@dataclass(slots=True, frozen=True)
class CitiesHint:
    birth_city: str
    death_city: str

    @classmethod
    def from_person(cls, person: FamousPerson) -> "CitiesHint":
        return cls(birth_city=person.birth.name, death_city=person.death.name)


@dataclass(slots=True, frozen=True)
class DatesHint:
    birth_year: int
    death_year: int

    @classmethod
    def from_person(cls, person: FamousPerson) -> "DatesHint":
        return cls(
            birth_year=int(person.birth.year),
            death_year=int(person.death.year),
        )


@dataclass(slots=True, frozen=True)
class GenderHint:
    gender: Gender

    @classmethod
    def from_person(cls, person: FamousPerson) -> "GenderHint":

        return cls(gender=person.gender)


@dataclass(slots=True, frozen=True)
class OccupationHint:
    occupation: str

    @classmethod
    def from_person(cls, person: FamousPerson) -> "OccupationHint":
        return cls(occupation=person.occupation)


@dataclass(slots=True, frozen=True)
class HiddenNameHint:
    name: str

    @classmethod
    def from_person(cls, person: FamousPerson) -> "HiddenNameHint":
        return cls(name=re.sub("[a-zA-Z]", "_", person.name))


Hint = CitiesHint | DatesHint | GenderHint | OccupationHint | HiddenNameHint
