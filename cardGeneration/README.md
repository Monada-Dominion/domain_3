# Card Generation Project

This project is a collection of tools and assets for generating themed decks of cards. It includes web scrapers to gather data, scripts to generate card images, and pre-made decks.

---

## 📁 Directory Structure

### `md_time_cards/`

This directory contains the core tools for generating a deck of 72 "Time Cards".

-   **Python Scripts:**
    -   `card_gen.py`: Generates individual card images.
    -   `deck_gen.py`: Assembles a full deck of cards.
    -   `a4_assembler.py` & `a4_assembler_optimised.py`: Arranges cards onto an A4-sized sheet for printing.
    -   `card_back_assembler.py`: Creates the back of the cards.
    -   `glitcher.py`: A script to apply a "glitch" effect to images.
-   **Assets and Output:**
    -   `output_folder/`: The default location for generated card images.
    -   `a4_to_print/`: The default location for generated A4 print sheets.

### `themed_decks/`

This directory is for creating specialized, themed decks.

-   **Python Scripts:**
    -   `final_card_generator.py` & `cardGenerationUniqueHeaders.py`: Scripts for generating cards with unique themes and headers.
-   **Assets and Output:**
    -   `sourceImages/`, `fonts/`, `namesAndDescriptions/`: Contain the assets needed to create the themed decks.
    -   `ready_decks_examples/`: Contains examples of fully generated themed decks.
    -   `final_cards/`: The output directory for the generated themed cards.

### `webScraper/`

This directory contains Python scripts for scraping card data from [https://chrisgeene.nl/cards/](https://chrisgeene.nl/cards/).

-   `webScraper.py`: Scrapes the data and saves it to `output.json`.
-   `webScraperAndTranslate.py`: Scrapes the data, translates it from Dutch to English, and saves it to `translatedOutput.json`.
-   `output.json`: The raw, untranslated scraped data.
-   `translatedOutput.json`: The English translation of the scraped data.

## 🍷 A Final Note

And don't forget that you are a human - get some real VINO.