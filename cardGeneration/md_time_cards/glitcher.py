from PIL import Image, ImageDraw, ImageFilter, ImageChops
import random
import os

def glitch_image(input_image_path, output_image_path, **params):
    """
    Apply glitch effects to an image based on controllable parameters.

    Parameters:
    - input_image_path: Path to the input image.
    - output_image_path: Path to save the glitched image.
    - params: Dictionary of glitch parameters:
        - slice_count: Number of slices (higher = more glitch lines).
        - max_offset: Maximum horizontal pixel offset for slices.
        - color_shift: Maximum color channel shift.
        - noise_level: Amount of noise applied to the image.
        - blur_radius: Radius for blurring effect (0 = no blur).
    """
    # Load the image
    img = Image.open(input_image_path)
    img = img.convert("RGB")  # Ensure RGB mode
    width, height = img.size

    # Read parameters with defaults
    slice_count = params.get('slice_count', 10)
    max_offset = params.get('max_offset', 20)
    color_shift = params.get('color_shift', 10)
    noise_level = params.get('noise_level', 30)
    blur_radius = params.get('blur_radius', 0)

    # Create a blank image for the output
    glitched_img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(glitched_img)

    # Apply slice-based glitch
    for i in range(slice_count):
        # Randomly select slice height
        slice_height = random.randint(5, height // slice_count)

        # Randomly select a y-coordinate for the slice
        y = random.randint(0, height - slice_height)

        # Crop the slice from the original image
        slice_box = (0, y, width, y + slice_height)
        slice_img = img.crop(slice_box)

        # Apply a random horizontal offset to the slice
        offset = random.randint(-max_offset, max_offset)
        glitched_img.paste(slice_img, (offset, y))

    # Apply color channel shifts
    r, g, b = glitched_img.split()
    r = ImageChops.offset(r, random.randint(-color_shift, color_shift), 0)
    g = ImageChops.offset(g, 0, random.randint(-color_shift, color_shift))
    b = ImageChops.offset(b, random.randint(-color_shift, color_shift), 0)
    glitched_img = Image.merge("RGB", (r, g, b))

    # Apply blur
    if blur_radius > 0:
        glitched_img = glitched_img.filter(ImageFilter.GaussianBlur(blur_radius))

    # Save the final glitched image
    glitched_img.save(output_image_path)
    print(f"Glitched image saved to {output_image_path}")


# Example usage
input_image_path = "/Users/computera/Documents/files/Documents1/py/cardGeneration/md_time_cards/a4_to_print/backside_page_3.png"  # Replace with the backside card area
output_image_path = "glitched_image.png"  # Path to save the glitched image

# Control parameters
glitch_params = {
    "slice_count": 30,  # Number of slices (more slices = more glitch lines)
    "max_offset": 0,   # Maximum horizontal pixel offset for slices
    "color_shift": 5,  # Maximum pixel offset for RGB color shifts
    "noise_level": 100,   # Amount of noise applied to the image (set to 0 as it's not used here)
    "blur_radius": 3    # Blur radius for a smoothed glitch effect
}

# Apply glitch effect
glitch_image(input_image_path, output_image_path, **glitch_params)
