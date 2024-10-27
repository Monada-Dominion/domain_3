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
    if (player_id == 1) {
        selected_card = game->player1.hand[card_index];
        game->player1.hand[card_index] = NULL; // Remove from hand
        game->center_card1 = selected_card; // Move to center
    } else {
        selected_card = game->player2.hand[card_index];
        game->player2.hand[card_index] = NULL; // Remove from hand
        game->center_card2 = selected_card; // Move to center
    }
    printf("Player %d played card: %d\n", player_id, selected_card->number);
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
        // It's a tie, handle accordingly (e.g., both cards discarded)
        printf("The round is a tie.\n");
    }

    // Clear center cards after comparison
    game->center_card1 = NULL;
    game->center_card2 = NULL;
}

void destroy_game(Game* game) {
    destroy_deck(game->deck);
    free(game);
    printf("Game destroyed.\n");
}
