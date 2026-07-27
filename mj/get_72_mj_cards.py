import re
import random

def extract_cards(book_text, chapter_delimiter=r'\*\*\*', max_words=500):
    """
    Extract random text pieces from chapters in the book.

    Args:
        book_text (str): The full text of the book.
        chapter_delimiter (str): Regex pattern to identify chapter delimiters.
        max_words (int): Maximum word length for a card.

    Returns:
        list: A list of tuples (card_number, text) with extracted cards.
    """
    # Split book into chapters using the delimiter pattern
    chapters = re.split(chapter_delimiter, book_text)

    cards = []
    card_number = 1

    for chapter in chapters:
        # Extract sentences starting with a capital letter and ending with ., ?, or !
        sentences = re.findall(r'\b[A-Z][^.!?]*[.!?]', chapter)
        
        chapter_cards = []
        while len(chapter_cards) < 2 and sentences:
            # Choose a random sentence
            sentence = random.choice(sentences)
            sentences.remove(sentence)  # Avoid reusing the same sentence
            
            # Ensure the sentence is not too long
            if len(sentence.split()) <= max_words:
                chapter_cards.append((card_number, sentence.strip()))
                card_number += 1

        cards.extend(chapter_cards)

    return cards

# Example usage
if __name__ == "__main__":
    # Load the book text (assuming it's stored in a markdown file)
    with open("about_the_spider_and_the_time.md", "r", encoding="utf-8") as file:
        book_text = file.read()

    # Extract cards using the chapter delimiter `***`
    cards = extract_cards(book_text, chapter_delimiter=r'\*\*\*')

    # Save the cards to a markdown file
    with open("cards.md", "w", encoding="utf-8") as file:
        for card_number, text in cards:
            file.write(f"## Card {card_number}\n{text}\n\n")
