from PIL import Image, ImageDraw, ImageFont
import os

class CardGenerator:
    def __init__(self):
        self.card_width = 300
        self.card_height = 420
        self.border_color = "grey"
        self.header_color = "grey"
        self.font_size = 12

    def create_rounded_mask(self, size, radius):
        mask = Image.new('L', size)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([(0, 0), size], fill=255, radius=radius)
        return mask

    def generate_card(self, name, description, image_path, output_path):
        # Create the card template
        template = Image.new("RGB", (self.card_width, self.card_height), "white")
        draw = ImageDraw.Draw(template)

        # Create a border for the card
        border_width = 5
        for x in range(border_width):
            draw.rounded_rectangle(
                [(x, x), (self.card_width - x - 1, self.card_height - x - 1)],
                outline=self.border_color,
                radius=20  # Adjust the roundness of the corners
            )

        # Draw the header
        header_text = "Logic Gate Card"
        header_font = ImageFont.load_default()
        header_text_width, header_text_height = draw.textsize(header_text, font=header_font)
        header_x = (self.card_width - header_text_width) // 2
        header_y = 10
        draw.rectangle(
            [(0, 0), (self.card_width, header_y + header_text_height + 10)],
            fill=self.header_color
        )
        draw.text((header_x, header_y), header_text, fill="black", font=header_font)

        # Load the image
        image = Image.open(image_path)

        # Placeholder for the image
        image_width = self.card_width - 2 * border_width
        image_height = self.card_height // 2 - header_y - header_text_height - 20
        image_x = border_width
        image_y = header_y + header_text_height + 20

        # Create a white background for the image placeholder
        image_bg = Image.new("RGB", (image_width, image_height), "white")

        # Resize and crop the image to fit the placeholder
        image.thumbnail((image_width, image_height))
        image = image.crop((0, 0, image_width, image_height))

        # If the image has transparency, convert it to RGB and composite it over the white background
        if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
            image = Image.alpha_composite(image_bg.convert('RGBA'), image.convert('RGBA')).convert("RGB")

        # Create a mask for the image and apply it to create rounded corners
        image_mask = self.create_rounded_mask((image_width, image_height), 20)
        rounded_image = Image.new('RGB', (image_width, image_height))
        rounded_image.paste(image, mask=image_mask)

        # Paste the image onto the card
        template.paste(rounded_image, (image_x, image_y))

        # Draw the name and description
        text_y = image_y + image_height + 10
        draw.text((10, text_y), name, fill="black", font=header_font)
        draw.text((10, text_y + 20), description, fill="black", font=header_font)

        # Save the card
        template.save(output_path)

if __name__ == "__main__":
    card_generator = CardGenerator()
    output_folder = "generated_cards"

    # Paths to data files and image folder
    names_file = "names.txt"
    descriptions_file = "descriptions.txt"
    images_folder = "images"

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(names_file, "r") as file:
        names = file.read().splitlines()

    with open(descriptions_file, "r") as file:
        descriptions = file.read().splitlines()

    # Iterate through the images folder and generate cards
    for i, image_filename in enumerate(os.listdir(images_folder)):
        if image_filename.endswith(".png") or image_filename.endswith(".jpg"):
            name = names[i % len(names)]
            description = descriptions[i % len(descriptions)]
            image_path = os.path.join(images_folder, image_filename)
            output_path = os.path.join(output_folder, f"logicGate_card_{i + 1}.png")
            card_generator.generate_card(name, description, image_path, output_path)
