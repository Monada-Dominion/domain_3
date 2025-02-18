from PIL import Image, ImageDraw, ImageFont
import os

# Single name, image, and description
name = "Your Name"
description = "Your Description"
image_path = "/Users/krasnomakov/Documents1/py/cardGeneration/kisspng-xnor-gate-xor-gate-nand-gate-logic-gate-quantum-logic-gate-5b2f965672a0e3.0342038215298453344695.png"  # Replace this with the actual path to your image

# Output folder
output_folder = "output"

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Load the image
image = Image.open(image_path)

# Set font and size
font = ImageFont.load_default()

# Iterate to generate cards
for i in range(72):  # Assuming you want 72 cards
    # Create a drawing context
    draw = ImageDraw.Draw(image)

    # Draw name and description on the image
    draw.text((50, 50), f"Name: {name}", fill="white", font=font)
    draw.text((50, 100), f"Description: {description}", fill="white", font=font)

    # Save the generated card
    output_filename = f"card_{i + 1}.png"
    output_path = os.path.join(output_folder, output_filename)
    image.save(output_path)

# Optionally, you can resize the image if needed
# new_size = (width, height)
# resized_image = image.resize(new_size)
# resized_image.save(output_path)
