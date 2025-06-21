#this small script creates image placeholders of random color
#generates a list of 72 cards

from PIL import Image
import random

# Function to generate a random color
#def random_color():
#    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def random_color():
    return (255, 255, 255)

# Generate 72 images
for i in range(1, 73):
    # Create a new image with random color
    img = Image.new('RGB', (320, 150), random_color())
    
    # Save the image
    img.save(f'image_{i}.png')

print("All images have been generated and saved.")
