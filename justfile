# Starts the website
run:
    uv run -m pantheondle.main

# Process the data
data input:
    uv run -m pantheondle.scripts.prepare_data {{input}} data
