# Web Scraper for Card Data

This folder contains Python scripts to scrape card data from [https://chrisgeene.nl/cards/](https://chrisgeene.nl/cards/). The data is scraped with the permission of the website owner. The scraped data describes professional tasks for ICT and digital media education.

## File Descriptions

- `webScraper.py`: This script sends a request to the target URL, parses the HTML content using BeautifulSoup, and extracts structured data from elements with the class `post-module`. The extracted data (category, title, sub-title, description, and other attributes) is saved in `output.json`.

- `webScraperAndTranslate.py`: This script performs the same scraping process as `webScraper.py` but adds a translation step. It uses the `googletrans` library to translate the scraped text from Dutch to English. The translated data is saved in `translatedOutput.json`.

- `output.json`: A JSON file containing the raw, untranslated data scraped from the website.

- `translatedOutput.json`: A JSON file containing the scraped data after being translated into English.

## How to Use

### Prerequisites

You need to have Python installed, along with the required libraries. You can install them using pip:

```bash
pip install requests beautifulsoup4 googletrans==4.0.0-rc1
```

### Running the Scripts

1.  **To Scrape the Data (without translation):**
    Execute the `webScraper.py` script.
    ```bash
    python cardGeneration/webScraper/webScraper.py
    ```
    This will create or update the `output.json` file in the same directory.

2.  **To Scrape and Translate the Data:**
    Execute the `webScraperAndTranslate.py` script.
    ```bash
    python cardGeneration/webScraper/webScraperAndTranslate.py
    ```
    This will create or update the `translatedOutput.json` file with the English translation of the scraped data.

**Note:** The paths in the scripts might need to be adjusted if you run them from a different directory context. The original scripts assume they are run from the workspace root.
