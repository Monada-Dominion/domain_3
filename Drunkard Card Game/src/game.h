#ifndef GAME_H
#define GAME_H

#include "deck.h"

typedef struct {
    Card* hand[6];
    int hand_size;
    Card* discard_pile[52];
    int discard_count;
} Player;

typedef struct {
    Deck* deck;
    Card* center_card1;
    Card* center_card2;
    Player player1;
    Player player2;
} Game;

Game* create_game();
void start_game(Game* game);
void player_move(Game* game, int player_id, int card_index);
void compare_cards(Game* game);
void destroy_game(Game* game);
void replenish_hand(Player* player, Deck* deck);
void reset_game(Game* game);

#endif
