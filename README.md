# 🔺 Monada Dominion: Domain 3 🃏

Welcome to Domain 3, a diverse collection of projects centered around card generation, simulations, and data visualization. This repository contains everything from a playable C-based card game to Python scripts for web scraping and generating unique, themed card decks.

[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-nd/4.0/)

---

## 🛠️ Technologies & Frameworks

![C](https://img.shields.io/badge/C-A8B9CC?style=for-the-badge&logo=c&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SDL2](https://img.shields.io/badge/SDL2-1E8449?style=for-the-badge&logo=sdl&logoColor=white)
![Folium](https://img.shields.io/badge/Folium-2E86C1?style=for-the-badge&logo=python&logoColor=white)

---

## 📁 Project Directory

### 🃏 `Drunkard Card Game/`
A fully playable graphical card game built from the ground up in C using the SDL2 library for rendering, fonts, and images.

-   **To Use:** Navigate to the directory, compile with `make`, and run `./card_game`.

### 🖨️ `cardGeneration/`
A suite of Python scripts for creating card decks. It includes web scrapers to gather content and powerful tools for generating card images and assembling them into themed decks.

-   **To Use:** Explore the various Python scripts to generate your own cards. See the `README.md` inside for more details.

### 🗺️ `mj/`
A collection of Python scripts for geographical data processing and creative content generation. It features scripts that create interactive maps with Folium, fetch live data from the Google Street View API, and generate "cards" from a text corpus.

-   **To Use:** Run the various Python scripts to generate maps or card data. Note that `fetch_live_data.py` requires a Google Cloud API key.

### 📝 `words_n_dots/`
A simple and fun command-line word guessing game implemented in Python. It simulates a card game where each "card" is a word to be guessed.

-   **To Use:** Run `python words_n_dots/wnd.py` in your terminal to play.

### 📄 `printable_deck/`
This directory contains ready-to-print PDF files of the generated card decks, perfect for creating physical copies of your creations.

-   **To Use:** Open the PDF files and print them to create your own physical card decks.
