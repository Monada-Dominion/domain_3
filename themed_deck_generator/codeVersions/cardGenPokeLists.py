#go over lists and generate cards 

from PIL import Image, ImageDraw, ImageFont
import os

# Constants
card_width = 300
card_height = 420
border_color = "black"
header_color = "lightblue"
font_size = 12

# Paths to data files and image folder
names_file = "names.txt"
descriptions_file = "descriptions.txt"
images_folder = "images"
output_folder = "pokemon_cards"

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Read names and descriptions from txt files
with open(names_file, "r") as file:
    names = file.read().splitlines()

with open(descriptions_file, "r") as file:
    descriptions = file.read().splitlines()

# Iterate through the images folder and generate cards
for i, image_filename in enumerate(os.listdir(images_folder)):
    # Check if it's a valid image file
    if image_filename.endswith(".png") or image_filename.endswith(".jpg"):
        # Create the card template
        template = Image.new("RGB", (card_width, card_height), "white")
        draw = ImageDraw.Draw(template)

        # Create a border for the card
        border_width = 5
        for x in range(border_width):
            draw.rectangle(
                [(x, x), (card_width - x - 1, card_height - x - 1)],
                outline=border_color
            )

        # Draw the header
        header_text = "Logic Gates"
        
        header_font = ImageFont.load_default()
        header_text_width, header_text_height = draw.textsize(header_text, font=header_font)
        header_x = (card_width - header_text_width) // 2
        header_y = 10
        draw.rectangle(
            [(0, 0), (card_width, header_y + header_text_height + 10)],
            fill=header_color
        )
        draw.text((header_x, header_y), header_text, fill="black", font=header_font)

        # Get name and description from lists
        name = names[i]
        description = descriptions[i]

        # Set font and size for name and description
        font = ImageFont.load_default()

        # Draw name and description on the card
        draw.text((10, header_y + header_text_height + 20), f"Name: {name}", fill="black", font=font)
        draw.text((10, header_y + header_text_height + 100), f"Description: {description}", fill="black", font=font)

        # Load the image
        image_path = os.path.join(images_folder, image_filename)
        image = Image.open(image_path)

        # Placeholder for the image
        image_placeholder = Image.new("RGB", (card_width - 20, 200), "lightgray")

        # Paste the image on the card
        template.paste(image_placeholder, (10, header_y + header_text_height + 240))
        template.paste(image, (20, header_y + header_text_height + 250))

        # Save the generated card
        output_filename = f"pokemon_card_{i + 1}.png"
        output_path = os.path.join(output_folder, output_filename)
        template.save(output_path)
