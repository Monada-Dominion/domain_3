from PIL import Image, ImageDraw
import os

# Constants
A4_WIDTH, A4_HEIGHT = 3508, 2480  # A4 dimensions in pixels at 300 dpi
CARDS_PER_ROW = 5  # Number of cards per row
CARDS_PER_COLUMN = 3  # Number of cards per column
EDGE_MARGIN = 50  # 5mm margin in pixels at 300 dpi
BORDER_WIDTH = 1  # Border thickness around each card

def assemble_images(input_folder, output_folder, dpi=300):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Get list of image files in input folder
    image_files = [f for f in os.listdir(input_folder) if f.startswith('card_') and f.endswith(('.png', '.jpg', '.jpeg'))]
    image_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))  # Sort by card number

    if not image_files:
        print("No images found in the input folder.")
        return

    # Calculate usable space for cards (subtract margins from the total page size)
    usable_width = A4_WIDTH - 2 * EDGE_MARGIN
    usable_height = A4_HEIGHT - 2 * EDGE_MARGIN

    # Calculate card size while preserving aspect ratio
    aspect_ratio = 0.736  # Aspect ratio of the cards
    card_width = usable_width / CARDS_PER_ROW
    card_height = usable_height / CARDS_PER_COLUMN

    if card_width / card_height > aspect_ratio:
        card_width = card_height * aspect_ratio
    else:
        card_height = card_width / aspect_ratio

    # Process images in chunks of CARDS_PER_PAGE
    cards_per_page = CARDS_PER_ROW * CARDS_PER_COLUMN
    for i in range(0, len(image_files), cards_per_page):
        images_chunk = image_files[i:i + cards_per_page]

        # Create a new A4 canvas
        canvas = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")
        draw = ImageDraw.Draw(canvas)

        # Place images on the canvas
        for idx, image_file in enumerate(images_chunk):
            row = idx // CARDS_PER_ROW
            col = idx % CARDS_PER_ROW

            # Calculate position to place the card (0 margin between cards)
            x = EDGE_MARGIN + col * card_width
            y = EDGE_MARGIN + row * card_height

            # Load image
            image_path = os.path.join(input_folder, image_file)
            img = Image.open(image_path)

            # Resize image to maintain aspect ratio
            img = img.resize((int(card_width), int(card_height)), Image.ANTIALIAS)

            # Paste image on canvas
            canvas.paste(img, (int(x), int(y)))
            
            # Draw border around the image
            draw.rectangle(
                [x - BORDER_WIDTH, y - BORDER_WIDTH, x + card_width + BORDER_WIDTH, y + card_height + BORDER_WIDTH],
                outline="black",
                width=BORDER_WIDTH
            )

        # Save the assembled A4 page
        output_path = os.path.join(output_folder, f"page_{i // cards_per_page + 1}.png")
        canvas.save(output_path, dpi=(dpi, dpi))

    print(f"Assembled pages saved to {output_folder}.")

# Example usage
input_folder = "/Users/computera/Documents/files/Documents1/py/cardGeneration/md_time_cards/output_folder"
output_folder = os.path.expanduser("/Users/computera/Documents/files/Documents1/py/cardGeneration/md_time_cards/a4_to_print")  # Save in user's home directory
assemble_images(input_folder, output_folder)
