# Mystical Journey (MJ)

This directory contains files for generation of a 72 card deck from A. Krasnomakov's Surreal Story: About the Spider and the time. 

This deck is an essential element for a transforamtional game with alternative worlds and meta world of the tetrad of books by A. Krasnomakov. 

the first book of the triad is available in this repo as .md file. Use it wisely. 

With the script 72 text cards are generated and can allow players to make moves in any version of MJ GAME: 
- mystical triangle 
- mystical enneagram 
- mystical duodecade with four alternative realms and the meta land (turn based table top version)
- mystical duodecade with four alternative realms and the meta land (chat based online)
- mystical duodecade with four alternative realms and the meta land (real world version)
---

##  Scripts and Their Functions

### Card Generation

-   `get_72_mj_cards.py`: This script reads the text from `about_the_spider_and_the_time.md`, a large text file, and extracts 72 random sentences to create a deck of "cards," which are saved in `cards.md`.

### Mapping


-   `maps.py`: Generates an interactive HTML map (`divided_map.html`) using the Folium library. The map is centered on a user-provided or random set of coordinates and is divided into 12 radial sections.
-   `maps_to_point_no_data.py`: Similar to `maps.py`, but likely focuses on pointing to specific locations without additional data overlays.
-   `maps_to_point_with_data.py`: An advanced version of the mapping script that likely overlays data points onto the map.
-   `maps_with_data.py`: Another variation of the mapping script that integrates data with the map visualization.

### Data Fetching

-   `fetch_live_data.py`: Fetches a Google Street View image for a specified latitude and longitude using the Google Maps Street View API. **Note:** This script requires a valid Google Cloud API key to function.

## Files

-   `about_the_spider_and_the_time.md`: A large text file that serves as the source material for card generation.
-   `cards.md`: The output file containing the generated cards.
-   `divided_map.html`: The output file for the interactive map.

## 📄 License

This project is licensed under the [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/) license.

You may share this work **with credit**, **non-commercially**, and **without modification**.
