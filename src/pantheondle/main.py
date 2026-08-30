import logging

from nicegui import ui

from pantheondle.components.base_layout import base_layout
from pantheondle.components.map_component import map_component
from pantheondle.components.session_component import game_session_card
from pantheondle.model.game import Difficulty, PersonRepository, get_repository

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@ui.page("/")
async def welcome_page() -> None:
    async def content() -> None:
        with ui.element("div").classes("flex gap-4"):
            ui.label("Select your difficulty").classes("text-lg font-medium")

            for difficulty in Difficulty:
                with (
                    ui.card()
                    .classes(
                        "cursor-pointer hover:bg-slate-200 ease-in-out duration-200 "
                        + "hover:scale-110"
                    )
                    .on("click", lambda d=difficulty: ui.navigate.to(f"/game/{d.name}"))
                ):
                    ui.label(str(difficulty.name))

    await base_layout(content)


@ui.page("/game/{difficulty}")
async def game_page(difficulty: str) -> None:
    async def content() -> None:

        difficulty_enum = Difficulty.parse(difficulty)
        if difficulty_enum is None:
            ui.navigate.to("/")
            return
        game = get_repository()

        session = game.new_game(difficulty_enum)

        ui.label(f"Playing a game of difficulty: {difficulty}")
        with ui.element("div").classes("flex flex-column gap-2 w-full"):
            await map_component(session=session)
            game_session_card(session=session)

    await base_layout(content)


def main() -> None:
    ui.run()


if __name__ in {"__main__", "__mp_main__"}:
    main()
