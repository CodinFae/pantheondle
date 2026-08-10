import logging

from nicegui import ui

from src.game import GameSession

logger = logging.getLogger(__name__)


@ui.refreshable
def show_game(session: GameSession):
    if session.game_status == 1:
        ui.label("SUCCESS")
    if session.game_status == -1:
        ui.label(f"Failed should have guessed {session.selected_person.name}")
    with ui.grid(columns=5):
        for hint in session.get_hints():
            ui.label(hint)


def guess_refresh(guess, session: GameSession):
    session.guess(guess)
    show_game.refresh()
    show_guesses.refresh()


@ui.refreshable
def show_guesses(session: GameSession):
    with ui.grid(columns=6):
        for guess in session.get_guesses():
            ui.label(guess)


def game_session_card(session: GameSession):
    with ui.card().classes("w-full") as card:
        with ui.element("div").classes("flex flex-row gap-2"):
            ui.select(
                label="Guess",
                with_input=True,
                options=session.candidates,
                on_change=lambda e: guess_refresh(e.value, session),
            )
            ui.button("Skip", on_click=lambda: guess_refresh("SKIP", session=session))
            show_guesses(session=session)

        show_game(session=session)

    return card
