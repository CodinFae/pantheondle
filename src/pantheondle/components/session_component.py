import logging

from nicegui import ui

from pantheondle.model.game import GameSession, GameStatus
from pantheondle.model.hints import (
    CitiesHint,
    DatesHint,
    GenderHint,
    HiddenNameHint,
    OccupationHint,
)

logger = logging.getLogger(__name__)


@ui.refreshable
def show_game(session: GameSession):
    if session.game_status is GameStatus.SUCCESS:
        ui.label("SUCCESS")
    if session.game_status is GameStatus.FAILED:
        ui.label(f"Failed should have guessed {session.selected_person.name}")
    with ui.grid(columns=len(session.hints)):
        for hint in session.get_hints():
            # TODO: Now that hints are classes, we can do one component per hint class
            match hint:
                case CitiesHint():
                    ui.label(f"Born in {hint.birth_city}, Died in {hint.death_city} ")
                case GenderHint():
                    ui.label(f"{hint.gender}")
                case OccupationHint():
                    ui.label(f"Considered a {hint.occupation}")
                case HiddenNameHint():
                    ui.label(f"{hint.name}")
                case DatesHint():
                    ui.label(f"Born on {hint.birth_year}, Died on {hint.death_year}")


def guess_refresh(guess: str | None, session: GameSession):
    session.guess(guess)
    guess_inputs.refresh()
    show_game.refresh()
    show_guesses.refresh()


@ui.refreshable
def show_guesses(session: GameSession):
    with ui.grid(columns=len(session.hints)):
        for guess in session.get_guesses():
            if guess is None:
                ui.label("Skipped")
            else:
                ui.label(guess)


@ui.refreshable
def guess_inputs(session: GameSession):
    with ui.row().classes(""):
        select_person = ui.select(
            label="Guess",
            with_input=True,
            options=session.candidates,
            on_change=lambda e: guess_refresh(e.value, session),
        ).classes("w-full")
        skip_button = ui.button(
            "Skip", on_click=lambda: guess_refresh(None, session=session)
        ).classes("col-auto")

        if session.game_status is not GameStatus.ONGOING:
            select_person.disable()
            skip_button.disable()


def game_session_card(session: GameSession):
    with ui.card().classes("w-full") as card:
        with ui.element("div").classes("flex flex-col gap-2 w-full"):
            guess_inputs(session=session)
            show_guesses(session=session)

        show_game(session=session)

    return card
