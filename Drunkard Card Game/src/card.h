#ifndef CARD_H
#define CARD_H

typedef struct {
    int number; // Unique number from 1 to 72
} Card;

Card* create_card(int number);
void destroy_card(Card* card);

#endif // CARD_H

