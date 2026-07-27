from PIL import Image, ImageDraw, ImageOps
import os

# Constants
A4_WIDTH, A4_HEIGHT = 3508, 2480  # A4 dimensions in pixels at 300 dpi
CARDS_PER_ROW = 18  # Number of cards per row
CARDS_PER_COLUMN = 13  # Number of cards per column
EDGE_MARGIN = 50  # 5mm margin around the edges of the page
BORDER_WIDTH = 1  # Border thickness around each card
CARDS_PER_PAGE = CARDS_PER_ROW * CARDS_PER_COLUMN  # Total cards per page


def create_backside(input_image_path, output_folder, total_pages, dpi=300):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Load the input image
    base_image = Image.open(input_image_path)
    base_image = base_image.convert("RGBA")  # Ensure image is in RGBA mode

    # Add a white background if the image has transparency
    white_background = Image.new("RGBA", base_image.size, "WHITE")
    base_image = Image.alpha_composite(white_background, base_image).convert("RGB")

    # Calculate available space for cards
    usable_width = A4_WIDTH - 2 * EDGE_MARGIN
    usable_height = A4_HEIGHT - 2 * EDGE_MARGIN

    # Calculate card size to fit the grid
    card_width = usable_width / CARDS_PER_ROW
    card_height = usable_height / CARDS_PER_COLUMN
    card_size = min(card_width, card_height)  # Ensure square cards

    # Resize the input image to match card size
    resized_image = base_image.resize((int(card_size), int(card_size)), Image.ANTIALIAS)

    # Create the specified number of A4 pages
    for page_number in range(total_pages):
        # Create a new A4 canvas
        canvas = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")
        draw = ImageDraw.Draw(canvas)

        # Arrange images in the grid aligned to the right
        for row in range(CARDS_PER_COLUMN):
            for col in range(CARDS_PER_ROW):
                # Calculate position for each card
                x = A4_WIDTH - EDGE_MARGIN - (CARDS_PER_ROW - col) * card_size
                y = EDGE_MARGIN + row * card_size

                # Flip the image horizontally for every alternate column
                if col % 2 == 1:  # Flip every alternate column for mirroring
                    card_image = ImageOps.mirror(resized_image)
                else:
                    card_image = resized_image

                # Paste the card image onto the canvas
                canvas.paste(card_image, (int(x), int(y)))

                # Draw border around the image
                draw.rectangle(
                    [x - BORDER_WIDTH, y - BORDER_WIDTH, x + card_size + BORDER_WIDTH, y + card_size + BORDER_WIDTH],
                    outline="black",
                    width=BORDER_WIDTH
                )

        # Save the backside A4 page
        output_path = os.path.join(output_folder, f"backside_page_{page_number + 1}.png")
        canvas.save(output_path, dpi=(dpi, dpi))

    print(f"Backside layouts saved to {output_folder}.")


# Example usage
input_image_path = "/Users/computera/Documents/files/Documents1/py/cardGeneration/md_time_cards/md_seal.png"  # Replace with your input image path
output_folder = os.path.expanduser("/Users/computera/Documents/files/Documents1/py/cardGeneration/md_time_cards/a4_to_print")  # Save in your home directory
total_pages = 5  # Total number of A4 pages to create (matching the front side)
create_backside(input_image_path, output_folder, total_pages)
