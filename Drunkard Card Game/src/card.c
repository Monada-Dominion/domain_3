#include <stdlib.h>
#include <stdio.h>
#include "card.h"

Card* create_card(int number) {
    Card* card = (Card*)malloc(sizeof(Card));
    card->number = number;
    printf("Card created: %d\n", number);
    return card;
}

void destroy_card(Card* card) {
    free(card);
    printf("Card destroyed.\n");
}

