from PIL import Image, ImageDraw
import os
from math import ceil

# Constants
A4_WIDTH, A4_HEIGHT = 3508, 2480  # A4 dimensions in pixels at 300 dpi
IMAGES_PER_ROW = 4
IMAGES_PER_COLUMN = 3
MARGIN = 50  # Margin around each image
BORDER_WIDTH = 5  # Border thickness around each image

def assemble_images(input_folder, output_folder, dpi=300):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Get list of image files in input folder
    image_files = [f for f in os.listdir(input_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

    if not image_files:
        print("No images found in the input folder.")
        return

    # Calculate available slot size for each image
    slot_width = (A4_WIDTH - (IMAGES_PER_ROW + 1) * MARGIN) // IMAGES_PER_ROW
    slot_height = (A4_HEIGHT - (IMAGES_PER_COLUMN + 1) * MARGIN) // IMAGES_PER_COLUMN

    # Process images in chunks of 12 (IMAGES_PER_ROW * IMAGES_PER_COLUMN)
    for i in range(0, len(image_files), IMAGES_PER_ROW * IMAGES_PER_COLUMN):
        images_chunk = image_files[i:i + IMAGES_PER_ROW * IMAGES_PER_COLUMN]

        # Create a new A4 canvas
        canvas = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")
        draw = ImageDraw.Draw(canvas)

        # Place images on the canvas
        for idx, image_file in enumerate(images_chunk):
            row = idx // IMAGES_PER_ROW
            col = idx % IMAGES_PER_ROW

            # Load image
            image_path = os.path.join(input_folder, image_file)
            img = Image.open(image_path)

            # Maintain aspect ratio while resizing
            img_ratio = img.width / img.height
            slot_ratio = slot_width / slot_height

            if img_ratio > slot_ratio:
                # Image is wider relative to the slot
                new_width = slot_width
                new_height = int(new_width / img_ratio)
            else:
                # Image is taller relative to the slot
                new_height = slot_height
                new_width = int(new_height * img_ratio)

            img = img.resize((new_width, new_height), Image.ANTIALIAS)

            # Calculate position to center the image in its slot
            x = MARGIN + col * (slot_width + MARGIN) + (slot_width - new_width) // 2
            y = MARGIN + row * (slot_height + MARGIN) + (slot_height - new_height) // 2

            # Paste image on canvas
            canvas.paste(img, (x, y))
            
            # Draw border around the image
            draw.rectangle(
                [x - BORDER_WIDTH, y - BORDER_WIDTH, x + new_width + BORDER_WIDTH, y + new_height + BORDER_WIDTH],
                outline="black",
                width=BORDER_WIDTH
            )

        # Save the assembled A4 page
        output_path = os.path.join(output_folder, f"page_{i // (IMAGES_PER_ROW * IMAGES_PER_COLUMN) + 1}.png")
        canvas.save(output_path, dpi=(dpi, dpi))

    print(f"Assembled pages saved to {output_folder}.")

# Example usage
input_folder = "/Users/computera/Documents/files/Documents1/py/cardGeneration/md_time_cards/output_folder"
output_folder = os.path.expanduser("/Users/computera/Documents/files/Documents1/py/cardGeneration/md_time_cards/a4_to_print")  # Save in user's home directory
assemble_images(input_folder, output_folder)
