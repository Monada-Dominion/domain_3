from PIL import Image, ImageDraw, ImageOps

# Define card dimensions (slightly larger than standard cards)
card_width_mm = 70
card_height_mm = 95

# Convert mm to pixels (assuming 300 DPI for high-quality print)
dpi = 300
def mm_to_px(mm):
    return int(mm * dpi / 25.4)

card_width_px = mm_to_px(card_width_mm)
card_height_px = mm_to_px(card_height_mm)

# Create a white background card
card = Image.new('RGB', (card_width_px, card_height_px), 'white')
draw = ImageDraw.Draw(card)

# Draw a 1px black border 4mm from the edge
margin_mm = 4
margin_px = mm_to_px(margin_mm)
border_rect = [
    (margin_px, margin_px),
    (card_width_px - margin_px - 1, card_height_px - margin_px - 1)
]
draw.rectangle(border_rect, outline='black', width=1)

# Load and resize the central symbol image
central_image = Image.open('/Users/computera/Documents/files/Documents1/py/cardGeneration/md_time_cards/12_shapes/6.jpg')  # Update with your image file
central_image = central_image.resize((400, 400), Image.ANTIALIAS)

# Paste the central image in the middle
central_x = (card_width_px - 400) // 2
central_y = (card_height_px - 400) // 2
card.paste(central_image, (central_x, central_y), central_image.convert('RGBA'))

# Load and resize the small symbols
symbol1 = Image.open('/Users/computera/Documents/files/Documents1/py/cardGeneration/md_time_cards/12_shapes/1.jpg')  # Update with your image file
symbol2 = Image.open('/Users/computera/Documents/files/Documents1/py/cardGeneration/md_time_cards/12_shapes/2.jpg')  # Update with your image file

# Resize symbols slightly smaller to accommodate the border
symbol_inner_size = 198  # Inner size after resizing
symbol_border_size = 1   # Border size in pixels
symbol_total_size = symbol_inner_size + 2 * symbol_border_size  # Total size after adding border

symbol1 = symbol1.resize((symbol_inner_size, symbol_inner_size), Image.ANTIALIAS)
symbol2 = symbol2.resize((symbol_inner_size, symbol_inner_size), Image.ANTIALIAS)

# Add a thin 1px black border to the small images
symbol1 = ImageOps.expand(symbol1, border=symbol_border_size, fill='white')
symbol2 = ImageOps.expand(symbol2, border=symbol_border_size, fill='white')

# Paste the small symbols in the upper-left corner
x_top1 = margin_px + 5
y_top = margin_px + 5
x_top2 = x_top1 + symbol_total_size + 5  # 5px spacing between symbols

card.paste(symbol1, (x_top1, y_top), symbol1.convert('RGBA'))
card.paste(symbol2, (x_top2, y_top), symbol2.convert('RGBA'))

# Paste the small symbols in the bottom-right corner, aligning both to the right
x_bottom2 = card_width_px - margin_px - symbol_total_size - 5
y_bottom = card_height_px - margin_px - symbol_total_size - 5
x_bottom1 = x_bottom2 - symbol_total_size - 5  # 5px spacing between symbols

card.paste(symbol2, (x_bottom1, y_bottom), symbol2.convert('RGBA'))  # Second image first
card.paste(symbol1, (x_bottom2, y_bottom), symbol1.convert('RGBA'))  # First image second


# Save the card image
card.save('card_output_fixed_v2.png')
