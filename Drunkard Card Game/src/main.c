#include </opt/homebrew/Cellar/sdl2/2.30.5/include/SDL2/SDL.h>
#include <stdio.h>
#include "game.h"

#define WINDOW_WIDTH 800
#define WINDOW_HEIGHT 600

void render_game(Game* game, SDL_Renderer* renderer) {
    // Clear the screen
    SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255); // White color
    SDL_RenderClear(renderer);

    // Render the deck (top)
    SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255); // Black color
    SDL_Rect deckRect = { (WINDOW_WIDTH - 100) / 2, 20, 100, 30 };
    SDL_RenderFillRect(renderer, &deckRect);

    // Render player 1's cards (left)
    for (int i = 0; i < game->player1.hand_size; i++) {
        SDL_Rect cardRect = { 50, 100 + i * 40, 100, 30 };
        SDL_RenderFillRect(renderer, &cardRect);
    }

    // Render player 2's cards (right)
    for (int i = 0; i < game->player2.hand_size; i++) {
        SDL_Rect cardRect = { WINDOW_WIDTH - 150, 100 + i * 40, 100, 30 };
        SDL_RenderFillRect(renderer, &cardRect);
    }

    // Render the active cards in the center
    if (game->center_card1 != NULL) {
        SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255); // Red color for player 1's active card
        SDL_Rect activeCardRect1 = { (WINDOW_WIDTH - 200) / 2, (WINDOW_HEIGHT - 40) / 2, 100, 30 };
        SDL_RenderFillRect(renderer, &activeCardRect1);
    }

    if (game->center_card2 != NULL) {
        SDL_SetRenderDrawColor(renderer, 0, 0, 255, 255); // Blue color for player 2's active card
        SDL_Rect activeCardRect2 = { (WINDOW_WIDTH + 100) / 2, (WINDOW_HEIGHT - 40) / 2, 100, 30 };
        SDL_RenderFillRect(renderer, &activeCardRect2);
    }

    // Present the renderer
    SDL_RenderPresent(renderer);
}

int main(int argc, char* argv[]) {
    // Initialize SDL
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        printf("SDL could not initialize! SDL_Error: %s\n", SDL_GetError());
        return 1;
    }
    printf("SDL initialized successfully.\n");

    // Create a window
    SDL_Window* window = SDL_CreateWindow("Card Game", 
        SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, 
        WINDOW_WIDTH, WINDOW_HEIGHT, SDL_WINDOW_SHOWN);
    
    if (window == NULL) {
        printf("Window could not be created! SDL_Error: %s\n", SDL_GetError());
        SDL_Quit();
        return 1;
    }
    printf("Window created successfully.\n");

    // Create a renderer
    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (renderer == NULL) {
        printf("Renderer could not be created! SDL_Error: %s\n", SDL_GetError());
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }
    printf("Renderer created successfully.\n");

    Game* game = create_game();
    start_game(game);
    printf("Game started. Players have been dealt cards.\n");

    // Main game loop
    int running = 1;
    int player_turn = 1; // 1 for Player 1, 2 for Player 2
    int selected_card_index = -1;
    SDL_Event event;
    while (running) {
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                running = 0;
            } else if (event.type == SDL_MOUSEBUTTONDOWN) {
                int x = event.button.x;
                int y = event.button.y;

                // Check if a card is clicked
                if (player_turn == 1) {
                    for (int i = 0; i < game->player1.hand_size; i++) {
                        SDL_Rect cardRect = { 50, 100 + i * 40, 100, 30 };
                        if (x >= cardRect.x && x <= cardRect.x + cardRect.w && y >= cardRect.y && y <= cardRect.y + cardRect.h) {
                            selected_card_index = i;
                            break;
                        }
                    }
                } else {
                    for (int i = 0; i < game->player2.hand_size; i++) {
                        SDL_Rect cardRect = { WINDOW_WIDTH - 150, 100 + i * 40, 100, 30 };
                        if (x >= cardRect.x && x <= cardRect.x + cardRect.w && y >= cardRect.y && y <= cardRect.y + cardRect.h) {
                            selected_card_index = i;
                            break;
                        }
                    }
                }

                if (selected_card_index != -1) {
                    player_move(game, player_turn, selected_card_index);
                    selected_card_index = -1;

                    if (player_turn == 2) {
                        compare_cards(game);
                    }

                    player_turn = player_turn == 1 ? 2 : 1; // Switch turn
                }
            }
        }

        render_game(game, renderer);
    }

    // Clean up
    destroy_game(game);
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
    printf("Game exited cleanly.\n");
    return 0;
}
