# 🃏 Themed Card Deck Generator 🃏

Welcome to the Themed Card Deck Generator! This folder contains a set of Python scripts to automatically generate decks of 72 unique, themed cards.

## ✨ Features

- **Automated Card Generation**: Create a full deck of 72 cards from text files and images.
- **Unique Designs**: Each card in the deck has a unique background color, generated from a vibrant color spectrum.
- **Customizable Content**: Easily change card names, descriptions, and images.
- **Themed Decks**: Scripts can be adapted to create decks with different themes and headers for card groups.
- **High-Quality Output**: Generates high-resolution cards (300 DPI) ready for printing.
- **8-bit Font**: Uses 'Press Start 2P' font for a retro gaming look.

## 🐍 Python Scripts

This directory contains the following Python scripts:

### 📄 `final_card_generator.py`

This is the main script for generating a standard 72-card deck.

- **What it does**: It takes a list of names, a list of descriptions, and a folder of images to create 72 cards. Each card has a standard header ("Logic Cards"), an image, name, description, and a unique background color.
- **Usage**: This is the recommended script for general-purpose card deck generation.

### 📑 `cardGenerationUniqueHeaders.py`

This is a modified version of the main script, designed for creating decks where cards are grouped into themes.

- **What it does**: It works similarly to the main script, but it assigns a unique header to each group of 6 cards. This is useful for creating decks with sub-categories.
- **Note**: This script contains hardcoded paths and is provided as an example of further customization.

### 🖼️ `generateImage72Placeholders.py`

A small utility script to help you get started if you don't have images yet.

- **What it does**: It generates 72 blank white placeholder images with the correct naming convention (`image_1.png`, `image_2.png`, etc.). You can use these to set up your deck structure before you have the final artwork.

## 🚀 How to Use

1.  **Prepare your assets**:
    -   **Names & Descriptions**: You will need two text files, one for names and one for descriptions. Each file should contain 72 lines. These should be placed in the folder `namesAndDescriptions`. The script `final_card_generator.py` expects `logicGatesNames.txt` and `logicGatesDescriptions.txt`.
    -   **Images**: You need 72 images, named `image_1.png`, `image_2.png`, ..., `image_72.png`. Place them in the `sourceImages/standardisedLGatesImages/` folder.
    -   **Font**: Make sure you have the `PressStart2P-Regular.ttf` font file inside the `fonts/` directory.

2.  **Run the script**:
    ```bash
    python final_card_generator.py
    ```

3.  **Get your cards**:
    -   The generated cards will be saved in the `final_cards/` folder.

## 🃏 Ready Decks Examples

For a sneak peek at what you can create, check out the `ready_decks_examples/` directory. You'll find examples of fully generated decks there.

## 🎨 Customization

- **Content**: To create your own deck, simply replace the contents of the names and descriptions files, and provide your own images.
- **Headers**: To change the main header, edit the `header_text` variable in `final_card_generator.py`. For themed headers, you can adapt the logic from `cardGenerationUniqueHeaders.py`.
- **Colors**: The background colors are generated automatically. You can tweak the `get_background_color` function if you want to change the color generation logic.

Happy card crafting! 🎉
