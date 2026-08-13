from nicegui import ui

from pantheondle.model.game import GameSession


async def map_component(session: GameSession):

    p = session.selected_person
    center = (
        (p.birth_place.lat + p.death_place.lat) / 2,
        (p.birth_place.lon + p.death_place.lon) / 2,
    )

    m = ui.leaflet(center=center).classes("h-100")
    m.clear_layers()
    _ = m.tile_layer(
        url_template="https://tiles.stadiamaps.com/tiles/stamen_watercolor/{z}/{x}/{y}.{ext}",
        options={
            "maxZoom": 16,
            "minZoom": 1,
            "attribution": '&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://www.stamen.com/" target="_blank">Stamen Design</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            "ext": "jpg",
        },
    )

    await m.initialized()
    m.run_map_method(
        "fitBounds",
        [
            [p.birth_place.lat, p.birth_place.lon],
            [p.death_place.lat, p.death_place.lon],
        ],
    )

    # TODO: Replace by marker (birth and death icon?) it seems more readable
    m.generic_layer(
        name="circle",
        args=[
            (p.birth_place.lat, p.birth_place.lon),
            {"color": "green", "radius": "5000"},
        ],
    )
    m.generic_layer(
        name="circle",
        args=[
            (p.death_place.lat, p.death_place.lon),
            {"color": "red", "radius": "5000"},
        ],
    )
