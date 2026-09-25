# Pantheondle

## Context

A very simple "Guess the famous person" based on a data dump from [Pantheon](https://pantheon.world).
It has different level of difficulty, based on cutoff range of the HPI metric, used by Pantheon.
The HPI is:

> HPI is currently made of five components: the “age” of a biography’s character (e.g. Jesus is more than 2,000 years old), number of Wikipedia language editions in which the biography has a presence (L), the concentration of the pageviews received by a biography across languages (L*), the stability of pageviews over time (CV), and the number of non-English pageviews received by that biography. 

## Setup

1. Use `just data [PATH_TO_DATA]` to automatically process the downloaded data from the pantheon csv database.
Tested with `person_2025_update.csv`
2. Use `just run` to run the website locally


## Citation

Yu, A. Z., et al. (2016). Pantheon 1.0, a manually verified dataset of globally famous biographies. Scientific Data 2:150075. doi: 10.1038/sdata.2015.75
