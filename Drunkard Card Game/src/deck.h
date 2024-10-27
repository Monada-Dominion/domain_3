#ifndef DECK_H
#define DECK_H

#include "card.h"

typedef struct {
    Card** cards; // Array of pointers to Card
    int size;     // Number of cards in the deck
} Deck;

Deck* create_deck();
void shuffle_deck(Deck* deck);
Card* draw_card(Deck* deck);
void destroy_deck(Deck* deck);

#endif // DECK_H

