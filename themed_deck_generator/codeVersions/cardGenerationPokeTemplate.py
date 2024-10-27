from PIL import Image, ImageDraw, ImageFont
import os

# Constants
card_width = 300
card_height = 420
border_color = "black"
header_color = "lightblue"
header_text = "Pokémon Card"
font_size = 12

# Output folder
output_folder = "pokemon_cards"

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

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
font = ImageFont.load_default()
header_font = ImageFont.load_default()
header_text_width, header_text_height = draw.textsize(header_text, font=header_font)
header_x = (card_width - header_text_width) // 2
header_y = 10
draw.rectangle(
    [(0, 0), (card_width, header_y + header_text_height + 10)],
    fill=header_color
)
draw.text((header_x, header_y), header_text, fill="black", font=header_font)

# Placeholder for image and description
image_placeholder = Image.new("RGB", (card_width - 20, 200), "lightgray")
description_placeholder = Image.new("RGB", (card_width - 20, 100), "lightgray")

# Save the template
template.paste(image_placeholder, (10, header_y + header_text_height + 20))
template.paste(description_placeholder, (10, header_y + header_text_height + 240))

# Save the template as a file
template.save(os.path.join(output_folder, "pokemon_card_template.png"))
