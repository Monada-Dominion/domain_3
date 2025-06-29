#include <stdlib.h>
#include <stdio.h>
#include "game.h"

Game* create_game() {
    Game* game = (Game*)malloc(sizeof(Game));
    game->deck = create_deck();
    game->center_card1 = NULL;
    game->center_card2 = NULL;
    game->player1.hand_size = 0;
    game->player1.discard_count = 0;
    game->player2.hand_size = 0;
    game->player2.discard_count = 0;
    return game;
}

void start_game(Game* game) {
    shuffle_deck(game->deck);
    for (int i = 0; i < 6; i++) {
        game->player1.hand[i] = draw_card(game->deck);
        game->player1.hand_size++;
        game->player2.hand[i] = draw_card(game->deck);
        game->player2.hand_size++;
    }
    printf("Players have been dealt cards: Player 1 has %d cards, Player 2 has %d cards.\n", game->player1.hand_size, game->player2.hand_size);
}

void player_move(Game* game, int player_id, int card_index) {
    Card* selected_card;
    Player* player;

    if (player_id == 1) {
        player = &game->player1;
    } else {
        player = &game->player2;
    }

    if (card_index < 0 || card_index >= player->hand_size) return;

    selected_card = player->hand[card_index];
    
    // Shift cards to fill the gap
    for (int i = card_index; i < player->hand_size - 1; i++) {
        player->hand[i] = player->hand[i + 1];
    }
    player->hand[player->hand_size - 1] = NULL;
    player->hand_size--;

    if (player_id == 1) {
        game->center_card1 = selected_card;
    } else {
        game->center_card2 = selected_card;
    }

    printf("Player %d played card: %d\n", player_id, selected_card->number);
}

void replenish_hand(Player* player, Deck* deck) {
    while (player->hand_size < 6 && deck->size > 0) {
        player->hand[player->hand_size++] = draw_card(deck);
    }
}

void compare_cards(Game* game) {
    if (game->center_card1 == NULL || game->center_card2 == NULL) return;

    if (game->center_card1->number > game->center_card2->number) {
        // Player 1 wins the round
        game->player1.discard_pile[game->player1.discard_count++] = game->center_card1;
        game->player1.discard_pile[game->player1.discard_count++] = game->center_card2;
        printf("Player 1 wins the round.\n");
    } else if (game->center_card1->number < game->center_card2->number) {
        // Player 2 wins the round
        game->player2.discard_pile[game->player2.discard_count++] = game->center_card1;
        game->player2.discard_pile[game->player2.discard_count++] = game->center_card2;
        printf("Player 2 wins the round.\n");
    } else {
        // It's a tie, return cards to each player's discard pile
        game->player1.discard_pile[game->player1.discard_count++] = game->center_card1;
        game->player2.discard_pile[game->player2.discard_count++] = game->center_card2;
        printf("The round is a tie. Cards returned.\n");
    }

    // Clear center cards after comparison
    game->center_card1 = NULL;
    game->center_card2 = NULL;
}

void reset_game(Game* game) {
    // Clear hands and discard piles
    for (int i = 0; i < game->player1.hand_size; i++) game->player1.hand[i] = NULL;
    for (int i = 0; i < game->player2.hand_size; i++) game->player2.hand[i] = NULL;
    for (int i = 0; i < game->player1.discard_count; i++) game->player1.discard_pile[i] = NULL;
    for (int i = 0; i < game->player2.discard_count; i++) game->player2.discard_pile[i] = NULL;
    
    game->player1.hand_size = 0;
    game->player1.discard_count = 0;
    game->player2.hand_size = 0;
    game->player2.discard_count = 0;
    
    // Reset deck
    destroy_deck(game->deck);
    game->deck = create_deck();
    
    // Restart game
    start_game(game);
}

void destroy_game(Game* game) {
    destroy_deck(game->deck);
    free(game);
    printf("Game destroyed.\n");
}
