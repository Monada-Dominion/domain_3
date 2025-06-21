# Drunkard Card Game

This project is a C-based prototype for a card game, demonstrating the use of generated card assets. It is built using the SDL2 library for graphics and user input. Buit on mac os, where SDL was installed with brew. For your set up change paths to SDL builds. 

[![Language](https://img.shields.io/badge/Language-C-blue.svg)](https://en.wikipedia.org/wiki/C_(programming_language))

## Card Images

The card images used in this game are sourced from the `../cardGeneration/md_time_cards` directory.

## Building and Running

To compile and run the game, you will need to have the SDL2, SDL2_ttf, and SDL2_image libraries installed. On macOS with Homebrew, you can install them with:

```bash
brew install sdl2 sdl2_ttf sdl2_image
```

Once the dependencies are installed, you can build the game using the provided `Makefile`:

```bash
make
```

To run the game, execute the following command:

```bash
./card_game
``` 