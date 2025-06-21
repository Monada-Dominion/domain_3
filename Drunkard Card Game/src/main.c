#include </opt/homebrew/Cellar/sdl2/2.32.8/include/SDL2/SDL.h>
#include </opt/homebrew/Cellar/sdl2_ttf/2.24.0/include/SDL2/SDL_ttf.h>
#include </opt/homebrew/Cellar/sdl2_image/2.8.8/include/SDL2/SDL_image.h>
#include <stdio.h>
#include "game.h"

#define WINDOW_WIDTH 1200
#define WINDOW_HEIGHT 800
#define FONT_PATH "fonts/PressStart2P-Regular.ttf"
#define CARD_WIDTH 100
#define CARD_HEIGHT 145

SDL_Texture* card_textures[73]; // 1-indexed for 72 cards
SDL_Texture* card_back_texture = NULL;

void load_card_textures(SDL_Renderer* renderer) {
    // Load card back
    char path[100];
    sprintf(path, "output_folder/card_back.png");
    SDL_Surface* surface = IMG_Load(path);
    if (!surface) {
        printf("Unable to load card back image! SDL_image Error: %s\n", IMG_GetError());
    } else {
        card_back_texture = SDL_CreateTextureFromSurface(renderer, surface);
        if (!card_back_texture) {
            printf("Unable to create texture from card_back.png! SDL Error: %s\n", SDL_GetError());
        }
        SDL_FreeSurface(surface);
    }

    for (int i = 1; i <= 72; i++) {
        sprintf(path, "output_folder/card_%d.png", i);
        SDL_Surface* surface = IMG_Load(path);
        if (!surface) {
            printf("Unable to load image %s! SDL_image Error: %s\n", path, IMG_GetError());
            card_textures[i] = NULL;
        } else {
            card_textures[i] = SDL_CreateTextureFromSurface(renderer, surface);
            if (!card_textures[i]) {
                printf("Unable to create texture from %s! SDL Error: %s\n", path, SDL_GetError());
            }
            SDL_FreeSurface(surface);
        }
    }
}

void destroy_card_textures() {
    if (card_back_texture) {
        SDL_DestroyTexture(card_back_texture);
    }
    for (int i = 1; i <= 72; i++) {
        if (card_textures[i]) {
            SDL_DestroyTexture(card_textures[i]);
        }
    }
}

void render_text(SDL_Renderer* renderer, const char* text, int x, int y, TTF_Font* font, SDL_Color color) {
    if (!font) {
        printf("Font not loaded!\n");
        return;
    }
    SDL_Surface* surface = TTF_RenderText_Solid(font, text, color);
    if (!surface) {
        printf("Unable to render text surface! SDL_ttf Error: %s\n", TTF_GetError());
        return;
    }
    SDL_Texture* texture = SDL_CreateTextureFromSurface(renderer, surface);
    if (!texture) {
        printf("Unable to create texture from rendered text! SDL Error: %s\n", SDL_GetError());
    } else {
        SDL_Rect destRect = { x, y, surface->w, surface->h };
        SDL_RenderCopy(renderer, texture, NULL, &destRect);
        SDL_DestroyTexture(texture);
    }
    SDL_FreeSurface(surface);
}

void render_game(Game* game, SDL_Renderer* renderer, int player_turn, TTF_Font* font) {
    // Clear the screen
    SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255); // White color
    SDL_RenderClear(renderer);

    // Render Deck
    SDL_Rect deckRect = { (WINDOW_WIDTH - CARD_WIDTH) / 2, 20, CARD_WIDTH, CARD_HEIGHT };
    if (card_back_texture) {
        SDL_RenderCopy(renderer, card_back_texture, NULL, &deckRect);
    } else {
        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
        SDL_RenderFillRect(renderer, &deckRect);
    }
    char deck_count[20];
    sprintf(deck_count, "Deck: %d", game->deck->size);
    render_text(renderer, deck_count, deckRect.x + 10, deckRect.y + 35, font, (SDL_Color){255, 255, 255, 255});

    // Render Player 1's Discard Pile
    char p1_discard_text[25];
    sprintf(p1_discard_text, "P1 Discard: %d", game->player1.discard_count);
    render_text(renderer, p1_discard_text, 50, WINDOW_HEIGHT - 60, font, (SDL_Color){0, 0, 0, 255});

    // Render Player 2's Discard Pile
    char p2_discard_text[25];
    sprintf(p2_discard_text, "P2 Discard: %d", game->player2.discard_count);
    render_text(renderer, p2_discard_text, WINDOW_WIDTH - 400, WINDOW_HEIGHT - 60, font, (SDL_Color){0, 0, 0, 255});

    // Highlight for player 1
    if (player_turn == 1) {
        SDL_SetRenderDrawColor(renderer, 255, 0, 0, 100); // Semi-transparent red
        SDL_Rect highlightRect = { 45, 95, 110, 515 };
        SDL_RenderFillRect(renderer, &highlightRect);
    }

    // Render player 1's cards (left)
    for (int i = 0; i < game->player1.hand_size; i++) {
        if (game->player1.hand[i]) {
            SDL_Rect cardRect = { 50, 100 + i * (CARD_HEIGHT/2), CARD_WIDTH, CARD_HEIGHT };
            if (card_back_texture) {
                SDL_RenderCopy(renderer, card_back_texture, NULL, &cardRect);
            } else {
                SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
                SDL_RenderFillRect(renderer, &cardRect);
            }
        }
    }

    // Highlight for player 2
    if (player_turn == 2) {
        SDL_SetRenderDrawColor(renderer, 0, 0, 255, 100); // Semi-transparent blue
        SDL_Rect highlightRect = { WINDOW_WIDTH - 155, 95, 110, 515 };
        SDL_RenderFillRect(renderer, &highlightRect);
    }

    // Render player 2's cards (right)
    for (int i = 0; i < game->player2.hand_size; i++) {
        if (game->player2.hand[i]) {
            SDL_Rect cardRect = { WINDOW_WIDTH - 150, 100 + i * (CARD_HEIGHT/2), CARD_WIDTH, CARD_HEIGHT };
            if (card_back_texture) {
                SDL_RenderCopy(renderer, card_back_texture, NULL, &cardRect);
            } else {
                SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
                SDL_RenderFillRect(renderer, &cardRect);
            }
        }
    }

    // Render the active cards in the center
    if (game->center_card1 != NULL) {
        SDL_Rect activeCardRect1 = { (WINDOW_WIDTH - CARD_WIDTH * 2 - 50) / 2, (WINDOW_HEIGHT - CARD_HEIGHT) / 2, CARD_WIDTH, CARD_HEIGHT };
        SDL_RenderCopy(renderer, card_textures[game->center_card1->number], NULL, &activeCardRect1);
    }

    if (game->center_card2 != NULL) {
        SDL_Rect activeCardRect2 = { (WINDOW_WIDTH + 50) / 2, (WINDOW_HEIGHT - CARD_HEIGHT) / 2, CARD_WIDTH, CARD_HEIGHT };
        SDL_RenderCopy(renderer, card_textures[game->center_card2->number], NULL, &activeCardRect2);
    }
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

    // Initialize SDL_image
    int imgFlags = IMG_INIT_PNG;
    if (!(IMG_Init(imgFlags) & imgFlags)) {
        printf("SDL_image could not initialize! SDL_image Error: %s\n", IMG_GetError());
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }

    // Initialize SDL_ttf
    if (TTF_Init() == -1) {
        printf("SDL_ttf could not initialize! SDL_ttf Error: %s\n", TTF_GetError());
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }
    
    TTF_Font* font = TTF_OpenFont(FONT_PATH, 24);
    if (font == NULL) {
        printf("Failed to load font! SDL_ttf Error: %s\n", TTF_GetError());
        // We can continue without a font, text rendering will just fail.
    }

    // Create a renderer
    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (renderer == NULL) {
        printf("Renderer could not be created! SDL_Error: %s\n", SDL_GetError());
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }
    printf("Renderer created successfully.\n");

    load_card_textures(renderer);

    Game* game = create_game();
    start_game(game);
    printf("Game started. Players have been dealt cards.\n");

    // Main game loop
    int running = 1;
    int attacking_player = 1;
    int player_turn = 1; // 1 for Player 1, 2 for Player 2
    int selected_card_index = -1;
    SDL_Event event;
    int game_over = 0;
    char winner_text[100] = "";

    while (running) {
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                running = 0;
            } else if (event.type == SDL_MOUSEBUTTONDOWN && !game_over) {
                int x = event.button.x;
                int y = event.button.y;

                // Check if a card is clicked
                if (player_turn == 1) {
                    for (int i = game->player1.hand_size - 1; i >= 0; i--) {
                        SDL_Rect cardRect = { 50, 100 + i * (CARD_HEIGHT/2), CARD_WIDTH, CARD_HEIGHT };
                        if (x >= cardRect.x && x <= cardRect.x + cardRect.w && y >= cardRect.y && y <= cardRect.y + cardRect.h) {
                            // Since cards overlap, we need to make sure we are not clicking a card behind another one.
                            // The backward loop helps, but a pixel-perfect check on an empty area of an overlapping card would require more complex logic.
                            // For now, this is a good approximation.
                            if (i < game->player1.hand_size - 1) {
                                SDL_Rect upperCardRect = { 50, 100 + (i + 1) * (CARD_HEIGHT/2), CARD_WIDTH, CARD_HEIGHT };
                                if (y > upperCardRect.y) continue;
                            }
                            selected_card_index = i;
                            break;
                        }
                    }
                } else {
                    for (int i = game->player2.hand_size - 1; i >= 0; i--) {
                        SDL_Rect cardRect = { WINDOW_WIDTH - 150, 100 + i * (CARD_HEIGHT/2), CARD_WIDTH, CARD_HEIGHT };
                        if (x >= cardRect.x && x <= cardRect.x + cardRect.w && y >= cardRect.y && y <= cardRect.y + cardRect.h) {
                            if (i < game->player2.hand_size - 1) {
                                SDL_Rect upperCardRect = { WINDOW_WIDTH - 150, 100 + (i + 1) * (CARD_HEIGHT/2), CARD_WIDTH, CARD_HEIGHT };
                                if (y > upperCardRect.y) continue;
                            }
                            selected_card_index = i;
                            break;
                        }
                    }
                }

                if (selected_card_index != -1) {
                    player_move(game, player_turn, selected_card_index);
                    
                    if (player_turn == 1) {
                        replenish_hand(&game->player1, game->deck);
                    } else {
                        replenish_hand(&game->player2, game->deck);
                    }

                    if (game->center_card1 != NULL && game->center_card2 != NULL) {
                        compare_cards(game);
                        attacking_player = (attacking_player == 1) ? 2 : 1;
                        player_turn = attacking_player;
                    } else {
                        player_turn = (player_turn == 1) ? 2 : 1; // Switch turn to defender
                    }
                    selected_card_index = -1;
                }
            }
        }

        render_game(game, renderer, player_turn, font);

        // Check for game over condition
        if (!game_over && game->deck->size == 0 && game->player1.hand_size == 0 && game->player2.hand_size == 0) {
            game_over = 1;
            int p1_score = 0;
            for(int i = 0; i < game->player1.discard_count; i++) p1_score += game->player1.discard_pile[i]->number;

            int p2_score = 0;
            for(int i = 0; i < game->player2.discard_count; i++) p2_score += game->player2.discard_pile[i]->number;

            if (p1_score > p2_score) {
                sprintf(winner_text, "Player 1 Wins! %d to %d", p1_score, p2_score);
            } else if (p2_score > p1_score) {
                sprintf(winner_text, "Player 2 Wins! %d to %d", p2_score, p1_score);
            } else {
                sprintf(winner_text, "It's a Tie! %d to %d", p1_score, p2_score);
            }
        }

        if (game_over) {
            SDL_SetRenderDrawColor(renderer, 200, 200, 200, 220);
            SDL_Rect modal = {(WINDOW_WIDTH - 400) / 2, (WINDOW_HEIGHT - 100) / 2, 400, 100};
            SDL_RenderFillRect(renderer, &modal);
            render_text(renderer, winner_text, modal.x + 20, modal.y + 20, font, (SDL_Color){0,0,0,255});
            render_text(renderer, "Game Over. Close the window to exit.", modal.x + 20, modal.y + 60, font, (SDL_Color){0,0,0,255});
        }
        
        SDL_RenderPresent(renderer);
    }

    // Clean up
    destroy_game(game);
    destroy_card_textures();
    TTF_CloseFont(font);
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    IMG_Quit();
    TTF_Quit();
    SDL_Quit();
    printf("Game exited cleanly.\n");
    return 0;
}
