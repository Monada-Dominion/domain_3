# Card Generation Scripts

This folder contains a set of Python scripts for generating a deck of 72 custom cards, assembling them onto A4 pages for printing, and creating matching card backs.

## File Descriptions

- `glitcher.py`: Applies a glitch effect to an image. It can be used to create a unique, distorted image from a base picture, such as the `md_seal.png`.
- `card_gen.py`: A simple script to generate a single card with a central image and corner symbols. It's a good starting point for understanding the basic card structure.
- `deck_gen.py`: Generates a full deck of 72 cards based on a specific set of rules for combining symbols from the `12_shapes` folder. The output is saved in the `output_folder`.
- `card_back_assembler.py`: Takes an image (e.g., `md_seal.png` or a glitched version) and arranges it in a grid on A4 pages to be printed as card backs. It mirrors alternate columns to ensure correct alignment for double-sided printing.
- `a4_assembler.py`: Assembles the generated card faces from `output_folder` onto A4 pages, arranging them in a 4x3 grid.
- `a4_assembler_optimised.py`: An optimized version of `a4_assembler.py` that arranges cards in a 5x3 grid, making better use of the A4 page space.

## Folders

- `12_shapes/`: Contains the 12 symbol images used for the cards.
- `output_folder/`: The default location where `deck_gen.py` saves the 72 individual card images.
- `a4_to_print/`: The default location where the `a4_assembler` and `card_back_assembler` scripts save the final A4 pages ready for printing.

## Image Files

- `md_seal.png`: A seal image used as the base for the card backs.
- `glitched_image.png`: An example of an image created by `glitcher.py`.

## How to Use

1.  **Generate the Card Deck:**
    Run `deck_gen.py` to create the 72 card faces.
    ```bash
    python cardGeneration/md_time_cards/deck_gen.py
    ```
    The generated cards will be saved in the `output_folder`.

2.  **Assemble Card Faces for Printing:**
    Run `a4_assembler_optimised.py` to arrange the card faces onto A4 pages.
    ```bash
    python cardGeneration/md_time_cards/a4_assembler_optimised.py
    ```
    The output pages will be saved in `a4_to_print/`.

3.  **Create Card Backs:**
    You can use the `md_seal.png` directly or create a glitched version first.
    To create a glitched version, modify and run `glitcher.py`.

    Then, run `card_back_assembler.py` to create the A4 pages for the card backs. Make sure the `total_pages` variable in the script matches the number of pages generated for the card faces.
    ```bash
    python cardGeneration/md_time_cards/card_back_assembler.py
    ```
    The card back pages will also be saved in `a4_to_print/`.

4.  **Print:**
    Print the pages from `a4_to_print/`. The card faces and backs are designed for double-sided printing. The mirroring in `card_back_assembler.py` should ensure they align correctly. 