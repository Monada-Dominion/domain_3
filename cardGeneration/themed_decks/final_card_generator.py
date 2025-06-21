#this script takes images, names and descriptions and creates 72 cards 
#quality is optimized with font size 32px 
#it creates 72 colors based on color spectrum, unique color for each card 
#Card consists of header, image section, name, description, background and black border
#thus, the script generates 72 unique cards using these elements
#names, descriptions and images can be substituted.


from PIL import Image, ImageDraw, ImageFont
import os

class FinalCardGenerator:
    def __init__(self):
        self.card_width = 708
        self.card_height = 1062
        self.border_color = "black"
        self.header_color = "black"
        self.max_font_size = 48
        self.num_colors = 72  # Define the number of colors here
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.font_path = os.path.join(script_dir, "fonts", "PressStart2P-Regular.ttf")

    def create_rounded_mask(self, size, radius):
        mask = Image.new('L', size)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([(0, 0), size], fill=255, radius=radius)
        return mask

    def wrap_text(self, text, font, max_width):
        lines = []
        line = []
        words = text.split()

        for word in words:
            test_line = line + [word] if line else [word]
            test_size = self.get_text_size(' '.join(test_line), font)

            if test_size[0] <= max_width:
                line.append(word)
            else:
                lines.append(' '.join(line))
                line = [word]

        if line:
            lines.append(' '.join(line))

        return '\n'.join(lines)

    def get_text_size(self, text, font):
        dummy_img = Image.new('RGB', (1, 1))
        dummy_draw = ImageDraw.Draw(dummy_img)
        bbox = dummy_draw.textbbox((0, 0), text, font=font)
        return (bbox[2] - bbox[0], bbox[3] - bbox[1])

    def generate_card(self, name, description, image_path, output_path):
        try:
            # Create the card template
            template = Image.new("RGB", (self.card_width, self.card_height), "white")
            draw = ImageDraw.Draw(template)

            # Determine the background color based on the card index
            card_index = int(output_path.split("_")[-1].split(".")[0])
            background_color = self.get_background_color(card_index)

            # Create a border for the card
            border_width = 5
            for x in range(border_width):
                draw.rounded_rectangle(
                    [(x, x), (self.card_width - x - 1, self.card_height - x - 1)],
                    outline=self.border_color,
                    radius=20,
                    fill=background_color  # Set the background color
                )

            # Draw the header
            header_text = "Logic Cards"
            header_font_size = 32
            # Use a try-except block to handle missing font file
            try:
                header_font = ImageFont.truetype(self.font_path, size = header_font_size)
            except IOError:
                print(f"Font file not found at {self.font_path}. Using default font.")
                header_font = ImageFont.load_default()

            header_text_bbox = draw.textbbox((0, 0), header_text, font=header_font)
            header_text_width = header_text_bbox[2] - header_text_bbox[0]
            header_text_height = header_text_bbox[3] - header_text_bbox[1]
            header_x = (self.card_width - header_text_width) // 2
            header_y = 10
            draw.rectangle(
                [(0, 0), (self.card_width, header_y + header_text_height + 10)],
                fill=self.header_color
            )
            draw.text((header_x, header_y), header_text, fill="white", font=header_font)

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
            image.thumbnail((image_width, image_height), Image.Resampling.LANCZOS)
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

            # Draw the name and description within a text box
            text_y = image_y + image_height + 10
            max_text_width = self.card_width - 20
            name_font_size = 32
            description_font_size = 32
            
            try:
                name_font = ImageFont.truetype(self.font_path, size=name_font_size)
                description_font = ImageFont.truetype(self.font_path, size=description_font_size)
            except IOError:
                print(f"Font file not found at {self.font_path}. Using default font.")
                name_font = ImageFont.load_default()
                description_font = ImageFont.load_default()


            name = self.wrap_text(name, name_font, max_text_width)
            description = self.wrap_text(description, description_font, max_text_width)

            draw.text((10, text_y), name, fill="black", font=name_font)
            text_y += self.get_text_size(name, name_font)[1] + 20
            draw.text((10, text_y), description, fill="black", font=description_font)

            # Save the card
            template.save(output_path, dpi=(300, 300), quality=100)

        except Exception as e:
            print(f"Error generating card {output_path}: {e}")

    def get_background_color(self, card_index):
        colors = []
        num_colors = 72  # Total number of different colors for the cards

        for i in range(num_colors):
            hue = int((348 / num_colors) * i)
            rgb_color = self.hsv_to_rgb(hue / 360, 1, 1)
            scaled_color = tuple(int(255 * component) for component in rgb_color)
            colors.append(scaled_color)

        color_index = (card_index - 1) % num_colors
        return colors[color_index]

    def hsv_to_rgb(self, h, s, v):
        h_i = int(h * 6)
        f = h * 6 - h_i
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)

        if h_i == 0:
            return v, t, p
        if h_i == 1:
            return q, v, p
        if h_i == 2:
            return p, v, t
        if h_i == 3:
            return p, q, v
        if h_i == 4:
            return t, p, v
        return v, p, q

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Create a 'fonts' directory if it doesn't exist relative to the script.
    # The user should place the 'PressStart2P-Regular.ttf' file in this directory.
    fonts_dir = os.path.join(script_dir, "fonts")
    if not os.path.exists(fonts_dir):
        os.makedirs(fonts_dir)
        
    card_generator = FinalCardGenerator()
    output_folder = os.path.join(script_dir, "final_cards")

    # Using universal paths relative to the script's location
    names_file = os.path.join(script_dir, "namesAndDescriptions", "logicGatesNames.txt")
    descriptions_file = os.path.join(script_dir, "namesAndDescriptions", "logicGatesDescriptions.txt")
    images_folder = os.path.join(script_dir, "sourceImages", "standardisedLGatesImages")

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        with open(names_file, "r") as file:
            names = file.read().splitlines()

        with open(descriptions_file, "r") as file:
            descriptions = file.read().splitlines()

        image_files = [file for file in os.listdir(images_folder) if file.endswith((".png", ".jpeg", ".jpg"))]
        
        # Check if all required files and folders are present
        if not all([names, descriptions, image_files]):
            print("Error: Ensure names, descriptions, and image files are available.")
        else:
            for image_filename in image_files:
                try:
                    card_index = int(image_filename.split("_")[-1].split(".")[0])
                    if 1 <= card_index <= len(names):
                        name = names[card_index - 1]
                        description = descriptions[card_index - 1]
                        image_path = os.path.join(images_folder, image_filename)
                        output_path = os.path.join(output_folder, image_filename)
                        card_generator.generate_card(name, description, image_path, output_path)
                except (ValueError, IndexError) as e:
                    print(f"Skipping file {image_filename} due to error: {e}")

    except FileNotFoundError as e:
        print(f"Error: {e}. Please make sure the required data files and image folder exist.") 