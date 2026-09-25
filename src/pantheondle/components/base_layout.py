from types import FunctionType

from nicegui import ui


async def base_layout(content_fn: FunctionType) -> None:
    # Fixed Header
    with ui.header().classes("bg-primary p-2"):
        ui.label("Pantheondle").classes("text-xl text-white font-bold")

    # Main content container (takes up remaining height)
    with ui.column().classes("w-full max-w-4xl mx-auto p-4 flex-grow"):
        await content_fn()

    # Sticky/Fixed Footer
    with ui.footer().classes("bg-gray-200 text-black p-2"):
        ui.label("Based on pantheon.world (Yu, A. Z., et al. (2016). Pantheon 1.0, a manually verified dataset of globally famous biographies. Scientific Data 2:150075. doi: 10.1038/sdata.2015.75)")
