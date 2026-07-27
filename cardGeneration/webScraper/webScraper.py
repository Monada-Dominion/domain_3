import requests
from bs4 import BeautifulSoup
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

# Save data as JSON
with open('/webScraper/output.json', 'w', encoding='utf-8') as json_file:
    json.dump(data_list, json_file, ensure_ascii=False, indent=2)

print("Data has been saved to 'output.json'")
