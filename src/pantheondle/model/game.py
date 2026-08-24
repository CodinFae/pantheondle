import logging
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

import pandas as pd

from pantheondle.model.hints import (
    CitiesHint,
    DatesHint,
    GenderHint,
    HiddenNameHint,
    Hint,
    OccupationHint,
)
from pantheondle.model.person import FamousPerson

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


class GameStatus(Enum):
    FAILED = -1
    ONGOING = 0
    SUCCESS = 1


class Game:
    def __init__(self, parquet_path: Path) -> None:
        df = pd.read_parquet(parquet_path)
        logger.info(f"Loaded {len(df)} persons")
        self.persons = df

    def _get_persons_by_level(self, difficulty: Difficulty) -> pd.DataFrame:
        return self.persons[self.persons["hpi"] > difficulty.value.cutoff]

    def start(self, difficulty: Difficulty):
        all_persons = self._get_persons_by_level(difficulty)
        row = all_persons.sample(1).iloc[0]

        return GameSession(
            selected_person=FamousPerson.from_row(row), candidates=all_persons["name"].to_list()
        )


@dataclass(slots=True)
class GameSession:
    selected_person: FamousPerson
    candidates: list[str]
    guesses: list[str | None] = field(default_factory=list)

    game_status: GameStatus = GameStatus.ONGOING

    hints: list[Hint] = field(init=False)

    def __post_init__(self):
        self.hints = [
            CitiesHint.from_person(self.selected_person),
            DatesHint.from_person(self.selected_person),
            GenderHint.from_person(self.selected_person),
            OccupationHint.from_person(self.selected_person),
            HiddenNameHint.from_person(self.selected_person),
        ]

    def get_hints(self) -> list[Hint]:
        return self.hints[:len(self.guesses)]

    def get_guesses(self) -> list[str | None]:
        return self.guesses

    def guess(self, guess_name: str | None):
        self.guesses.append(guess_name)
        if (
            guess_name == self.selected_person.name
            and self.game_status is not GameStatus.FAILED
        ):
            self.game_status = GameStatus.SUCCESS

        if len(self.guesses) > len(self.hints) and self.game_status is not GameStatus.SUCCESS:
            self.game_status = GameStatus.FAILED

        logger.info(f"Status {self.game_status} at step {len(self.guesses)}")
        return self.game_status
