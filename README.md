# 🃏 Domain 3: The Triangle - Cards

<p align="center">
  <img src="https://img.shields.io/github/last-commit/monada-dominion/domain_3?style=for-the-badge" alt="GitHub last commit">
  <img src="https://img.shields.io/github/repo-size/monada-dominion/domain_3?style=for-the-badge" alt="GitHub repo size">
</p>

<p align="center">
  <em>A diverse collection of projects centered around card generation.</em>
</p>

---

Welcome to Domain 3, a card deck domain. It's a diverse collection of projects centered around card generation, simulations, and data visualization. This repository contains everything from a playable C-based card game to Python scripts for web scraping and generating unique, themed card decks.

## 🗺️ Initial domains of Monada Dominion

It is a progressive journey structured into several domains. While you can explore some parts out of order, the intended path is designed for a gradual unfolding of understanding.

*   **🌀 Domain 1: The Dot - Mindfulness** (<a href="https://github.com/Monada-Dominion/domain_1">Link</a>)
    *   Essential preparation for the entire MD system - Shin-Lap mindfulness program.

*   **🧘‍♂️ Domain 2: The Line - Meditation** (<a href="https://github.com/Monada-Dominion/domain_2">Link</a>)
    *   Can be explored without preparation, but the need for theory from Domain 1 will emerge as you progress.

*   **🃏 Domain 3: The Triangle - Cards** (You are here)
    *   This is a card deck domain. It will not fully reveal itself without completing Domains 1 and 2. However, it's always possible to create something new.

*   **🔒 Domain 4: The quadrangle - Algorithms**
    *   Not visible or available without the knowledge from all three preceding domains.

> Further steps are obscured but can be opened on demand. All currently available domains: (<a href="https://github.com/Monada-Dominion/domain_3">Link</a>)

---

## 🚀 Projects in this Domain

### 🃏 `Drunkard Card Game/`
A fully playable graphical card game built from the ground up in C using the SDL2 library for rendering, fonts, and images.

-   **To Use:** Navigate to the directory, compile with `make`, and run `./card_game`.

### 🖨️ `cardGeneration/`
A suite of Python scripts for creating card decks. It includes web scrapers to gather content and powerful tools for generating card images and assembling them into themed decks.

-   **To Use:** Explore the various Python scripts to generate your own cards. See the `README.md` inside for more details.

### 🔮 `docs/` (Mystical Journey GitHub Pages Web App)
An interactive web application hosted on GitHub Pages for playing the **Mystical Journey (MJ)** transformational card game based on A. Krasnomakov's *About the Spider and the Time*.

-   **Features:**
    - Player Goal Stating (Energy / Matter / Time)
    - 1 to 6 players support (3–4 recommended, solo mode included)
    - 72 Card Deck & live book sentence generator
    - Card Interpretation recording & 3-card victory condition
    - Full Game History export (Markdown & JSON)
    - Real-World 12-Sector Map generator (Leaflet.js)
-   **Source Material:** [Krasnomakov Bureau – Literature](https://krasnomakov-bureau-info.github.io/literature/books/)
-   **GitHub Pages Deployment:** Configure repository Settings -> Pages -> Source: `Deploy from a branch`, Branch: `main`, Folder: `/docs`.

### 🗺️ `mj/`
A collection of Python scripts for geographical data processing and creative content generation. It features scripts that create interactive maps with Folium, fetch live data from the Google Street View API, and generate "cards" from a text corpus.

-   **To Use:** Run the various Python scripts to generate maps or card data. Note that `fetch_live_data.py` requires a Google Cloud API key.

### 📝 `words_n_dots/`
A simple and fun command-line word guessing game implemented in Python. It simulates a card game where each "card" is a word to be guessed.

-   **To Use:** Run `python words_n_dots/wnd.py` in your terminal to play.

### 📄 `printable_deck/`
This directory contains ready-to-print PDF files of the generated card decks, perfect for creating physical copies of your creations.

-   **To Use:** Open the PDF files and print them to create your own physical card decks.

---
## 🛠️ Technologies & Frameworks

![C](https://img.shields.io/badge/C-A8B9CC?style=for-the-badge&logo=c&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SDL2](https://img.shields.io/badge/SDL2-1E8449?style=for-the-badge&logo=sdl&logoColor=white)
![Folium](https://img.shields.io/badge/Folium-2E86C1?style=for-the-badge&logo=python&logoColor=white)

---

## 🙌 Contributing

Found a typo or have a suggestion? Contributions are welcome! Please feel free to open an issue or submit a pull request to improve the materials.

## 📄 License

Monada Dominion Non-Commercial No-Derivatives Source License (MD-NC-ND) v1.1

This project is open-source. See the [LICENSE](LICENSE) file for more details.
