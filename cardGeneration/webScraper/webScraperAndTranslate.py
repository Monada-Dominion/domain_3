import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import json

url = "https://chrisgeene.nl/cards/"  # Replace with the actual URL of the webpage

# Fetch the HTML content of the webpage
response = requests.get(url)
html_code = response.content

soup = BeautifulSoup(html_code, 'html.parser')

# Find all the card elements
cards = soup.find_all('div', class_='post-module')

data_list = []

# Loop through each card and extract information
for card in cards:
    data = {
        'category': card.find('div', class_='category').text.strip(),
        'title': card.find('h1', class_='title').text.strip(),
        'sub_title': card.find('h2', class_='sub_title').text.strip(),
        'description': card.find('p', class_='description').text.strip(),
        'selfstandigheid': card.find('span', class_='comments').find('strong', string='Zelfstandigheid').find_next('br').next_sibling.strip(),
        'gedrag': card.find('span', class_='comments').find('strong', string='Gedrag').find_next('br').next_sibling.strip(),
        'context': card.find('span', class_='comments').find('strong', string='Context').find_next('br').next_sibling.strip(),
    }

    data_list.append(data)

# Translate Dutch to English
translator = Translator()
translated_data_list = []

for data in data_list:
    translated_data = {}
    for key, value in data.items():
        try:
            # Check if the value is not None before translating
            if value is not None:
                translated_text = translator.translate(value, src='nl', dest='en').text
            else:
                translated_text = ''
        except Exception as e:
            print(f"Error translating '{value}': {e}")
            translated_text = ''

        translated_data[key] = translated_text

    translated_data_list.append(translated_data)

# Save translated data as JSON
with open('output_translated.json', 'w', encoding='utf-8') as json_file:
    json.dump(translated_data_list, json_file, ensure_ascii=False, indent=2)

print("Translated data has been saved to 'output_translated.json'")
