import logging

from nicegui import ui

from components.map_component import map_component
from components.session_component import game_session_card
from src.game import Difficulty, Game

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

game = Game("./data/person_2025_update.csv")


@ui.page("/")
async def page():
    with ui.element("nav").classes("bg-primary w-full p-2"):
        ui.label("Pantheondle").classes("text-xl text-white text-bold")

    session = game.start(Difficulty.EASY)

    with ui.element("div").classes("flex flex-column gap-2 w-full"):
        await map_component(session=session)
        game_session_card(session=session)


ui.run()
