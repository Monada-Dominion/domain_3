#this script takes images and standardises them with adding a white background 
#saves in a new folder

from PIL import Image, ImageOps
import os

# Specify the input and output directories
input_dir = '/Users/krasnomakov/Documents1/py/cardGeneration/asmlUniversalImages'
output_dir = '/Users/krasnomakov/Documents1/py/cardGeneration/standardisedImagesASMLUniversal'

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Define the target size for the output images
output_size = (696, 469)

# List all files in the input directory
image_files = [f for f in os.listdir(input_dir) if f.endswith('.jpg') or f.endswith('.png')]

# Iterate through each image file and process it
for image_file in image_files:
    # Open the image with alpha channel (transparency support)
    img = Image.open(os.path.join(input_dir, image_file)).convert("RGBA")

    # Create a new image with a white background of the target size
    white_bg = Image.new('RGBA', output_size, (255, 255, 255, 255))

    # Resize the original image to fit within the target size
    img.thumbnail(output_size, Image.ANTIALIAS)

    # Calculate the position to center the resized image on the white background
    x = (output_size[0] - img.width) // 2
    y = (output_size[1] - img.height) // 2

    # Paste the resized image onto the white background
    white_bg.paste(img, (x, y), img)

    # Save the resulting image in the output directory with the same name
    output_path = os.path.join(output_dir, image_file)
    white_bg.save(output_path)

print("Image processing complete. Images saved to the output folder.")
