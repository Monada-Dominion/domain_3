from PIL import Image, ImageDraw, ImageOps
import os

# Define card dimensions (slightly larger than standard cards)
card_width_mm = 70
card_height_mm = 95

# Convert mm to pixels (assuming 300 DPI for high-quality print)
dpi = 300
def mm_to_px(mm):
    return int(mm * dpi / 25.4)

card_width_px = mm_to_px(card_width_mm)
card_height_px = mm_to_px(card_height_mm)

# Get the current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Paths
symbols_folder = os.path.join(script_dir, '/Users/computera/Documents/files/Documents1/py/cardGeneration/md_time_cards/12_shapes')  # Update if your symbols are in a different location
output_folder = os.path.join(script_dir, '/Users/computera/Documents/files/Documents1/py/cardGeneration/md_time_cards/output_folder')      # Outputs will be saved in an 'output' folder next to your script

# Ensure the output directory exists
os.makedirs(output_folder, exist_ok=True)

# Load all symbols into a list for easy access
symbols = []
for i in range(1, 13):
    symbol_path = os.path.join(symbols_folder, f'{i}.jpg')
    symbol = Image.open(symbol_path)
    symbols.append(symbol)

# Parameters for small symbols
symbol_inner_size = 198  # Inner size after resizing
symbol_border_size = 1   # Border size in pixels
symbol_total_size = symbol_inner_size + 2 * symbol_border_size  # Total size after adding border

# Function to create a card
def create_card(card_number, central_symbol_index, first_small_symbol_index, second_small_symbol_index):
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
    central_image = symbols[central_symbol_index].resize((400, 400), Image.ANTIALIAS)
    
    # Paste the central image in the middle
    central_x = (card_width_px - 400) // 2
    central_y = (card_height_px - 400) // 2
    card.paste(central_image, (central_x, central_y), central_image.convert('RGBA'))
    
    # Resize small symbols
    first_small_symbol = symbols[first_small_symbol_index].resize((symbol_inner_size, symbol_inner_size), Image.ANTIALIAS)
    second_small_symbol = symbols[second_small_symbol_index].resize((symbol_inner_size, symbol_inner_size), Image.ANTIALIAS)
    
    # Add a thin 1px black border to the small images
    first_small_symbol = ImageOps.expand(first_small_symbol, border=symbol_border_size, fill='white')
    second_small_symbol = ImageOps.expand(second_small_symbol, border=symbol_border_size, fill='white')
    
    # Paste the small symbols in the upper-left corner
    x_top1 = margin_px + 5
    y_top = margin_px + 5
    x_top2 = x_top1 + symbol_total_size + 5  # 5px spacing between symbols
    
    card.paste(first_small_symbol, (x_top1, y_top), first_small_symbol.convert('RGBA'))
    card.paste(second_small_symbol, (x_top2, y_top), second_small_symbol.convert('RGBA'))
    
    # Paste the small symbols in the bottom-right corner, aligning both to the right
    x_bottom2 = card_width_px - margin_px - symbol_total_size - 5
    y_bottom = card_height_px - margin_px - symbol_total_size - 5
    x_bottom1 = x_bottom2 - symbol_total_size - 5  # 5px spacing between symbols
    
    # Rotate the small symbols for the bottom positions
    rotated_first_small_symbol = first_small_symbol.rotate(180, expand=True)
    rotated_second_small_symbol = second_small_symbol.rotate(180, expand=True)
    
    # Swap the order of symbols in the bottom-right corner (display second image first)
    card.paste(rotated_second_small_symbol, (x_bottom1, y_bottom), rotated_second_small_symbol.convert('RGBA'))  # Second image first
    card.paste(rotated_first_small_symbol, (x_bottom2, y_bottom), rotated_first_small_symbol.convert('RGBA'))  # First image second
    
    # Save the card image
    output_path = os.path.join(output_folder, f'card_{card_number}.png')
    card.save(output_path)

# Generate cards
card_number = 1
for group_index in range(12):  # 12 groups
    second_small_symbol_index = group_index  # Symbols are 0-indexed in the list (0 to 11)
    
    # Determine the range for first small and central symbols
    if group_index % 2 == 0:
        symbol_range = list(range(0, 6))  # Symbols 1 to 6 (indices 0 to 5)
    else:
        symbol_range = list(range(6, 12))  # Symbols 7 to 12 (indices 6 to 11)
    
    # Special case for final 6 cards
    if group_index == 11:
        second_small_symbol_index = 11  # Second small symbol is 12 (index 11)
        symbol_range = list(range(6, 12))  # Symbols 7 to 12 (indices 6 to 11)
    
    for i in range(6):  # 6 cards per group
        central_symbol_index = symbol_range[i]
        first_small_symbol_index = symbol_range[i]
        
        create_card(
            card_number=card_number,
            central_symbol_index=central_symbol_index,
            first_small_symbol_index=first_small_symbol_index,
            second_small_symbol_index=second_small_symbol_index
        )
        print(f'Generated card {card_number}')
        card_number += 1

print('All cards generated successfully!')
