#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include "deck.h"

Deck* create_deck() {
    Deck* deck = (Deck*)malloc(sizeof(Deck));
    deck->size = 72;
    deck->cards = (Card**)malloc(deck->size * sizeof(Card*));

    for (int i = 0; i < deck->size; i++) {
        deck->cards[i] = create_card(i + 1);
    }
    printf("Deck created with %d cards.\n", deck->size);
    return deck;
}

void shuffle_deck(Deck* deck) {
    srand(time(NULL));
    for (int i = 0; i < deck->size; i++) {
        int j = rand() % deck->size;
        Card* temp = deck->cards[i];
        deck->cards[i] = deck->cards[j];
        deck->cards[j] = temp;
    }
    printf("Deck shuffled.\n");
}

Card* draw_card(Deck* deck) {
    if (deck->size > 0) {
        Card* card = deck->cards[--deck->size];
        printf("Card drawn: %d\n", card->number);
        return card;
    }
    return NULL; // No cards left
}

void destroy_deck(Deck* deck) {
    for (int i = 0; i < deck->size; i++) {
        destroy_card(deck->cards[i]);
    }
    free(deck->cards);
    free(deck);
    printf("Deck destroyed.\n");
}

