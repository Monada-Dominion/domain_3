# Words 'n Dots

This project is a simple, command-line word guessing game implemented in Python. It's designed to simulate a card game where each "card" is a word, and the number of letters in the word is represented by "dots" (stars).

---

## 🎲 How it Works

The game operates in a loop, simulating a deck of 72 cards:

1.  **Deck Creation:** At the start, the `wnd.py` script reads the `words.txt` file and randomly selects 72 words to create a "deck".
2.  **Card Selection:** In each round, a word is randomly chosen from the deck. The player is told the length of the word.
3.  **Guessing Game:** The player then has to guess the letters of the word. The number of allowed turns is equal to the length of the word.
4.  **Winning/Losing:**
    -   If the player guesses all the letters correctly within the allowed turns, they win the round.
    -   If they run out of turns, they lose.
5.  **Game Progression:** After each round, the card is removed from the deck, and the game continues until all 72 cards have been played.

## 🚀 How to Play

To play the game, simply run the `wnd.py` script from your terminal:

```bash
python words_n_dots/wnd.py
```

Make sure that the `words.txt` file is in the same directory as the script.

--

## 📄 License

This project is licensed under the [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/) license.

You may share this work **with credit**, **non-commercially**, and **without modification**.
