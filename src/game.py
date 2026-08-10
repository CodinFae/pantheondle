import logging
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Literal

import pandas as pd

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class DifficultyConfig:
    cutoff: float


class Difficulty(Enum):
    EASY = DifficultyConfig(cutoff=90)
    MEDIUM = DifficultyConfig(cutoff=80)
    HARD = DifficultyConfig(cutoff=70)
    EXPERTS = DifficultyConfig(cutoff=50)
    IMPOSSIBLE = DifficultyConfig(cutoff=0)


class Game:
    def __init__(self, csv_path) -> None:
        df = pd.read_csv(csv_path)
        logger.info(f"Loaded {len(df)} persons")
        self.persons = self._filter_persons(df)
        logger.info(f"Kept {len(self.persons)} persons")

    def _filter_persons(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filter the provided dataframe by removing people that are still alive and the one with corrupted data"""
        filtered = df[~df["alive"]]
        filtered = filtered[pd.notna(filtered["dplace_name"])]
        filtered = filtered[pd.notna(filtered["bplace_name"])]
        filtered = filtered[pd.notna(filtered["bplace_lat"])]
        filtered = filtered[pd.notna(filtered["dplace_lat"])]
        return filtered

    def _get_persons_by_level(self, difficulty: Difficulty) -> pd.DataFrame:
        return self.persons[self.persons["hpi"] > difficulty.value.cutoff]

    def start(self, difficulty: Difficulty):
        all_persons = self._get_persons_by_level(difficulty)
        row = all_persons.sample(1).iloc[0]
        selected_person = FamousPerson(
            birth_place=Place(
                name=row["bplace_name"],
                lat=row["bplace_lat"],
                lon=row["bplace_lon"],
                year=row["birthyear"],
            ),
            death_place=Place(
                name=row["dplace_name"],
                lat=row["dplace_lat"],
                lon=row["dplace_lon"],
                year=row["deathyear"],
            ),
            gender=row["gender"],
            occupation=row["occupation"],
            name=row["name"],
        )
        return GameSession(
            selected_person=selected_person, candidates=all_persons["name"].to_list()
        )


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


@dataclass()
class GameSession:
    selected_person: FamousPerson
    candidates: list[str]
    guesses: list[str] = field(default_factory=list)

    step: int = 0
    max_steps: int = 5

    game_status: Literal[0, -1, 1] = 0

    def get_hints(self) -> list[str]:
        hints = [
            f"Born in {self.selected_person.birth_place.name}, died in {self.selected_person.death_place.name}",
            f"Lived in {self.selected_person.birth_place.year} to {self.selected_person.death_place.year}",
            f"Gender: {self.selected_person.gender}",
            f"Occupation: {self.selected_person.occupation}",
            f"Format: {re.sub('[a-zA-Z]', '_', self.selected_person.name)}",
        ]

        select_index = min(self.step, len(hints))
        return hints[:select_index]

    def get_guesses(self) -> list[str]:
        return self.guesses

    def guess(self, guess_name: str):
        logger.debug(f"Guessing {guess_name}")
        self.guesses.append(guess_name)
        if guess_name == self.selected_person.name:
            self.game_status = 1

        self.step = self.step + 1
        # TODO: Make it depends on the amount of hints
        if self.step > self.max_steps and self.game_status != 1:
            self.game_status = -1

        logger.info(f"Status {self.game_status} at step {self.step}")
        return self.game_status
