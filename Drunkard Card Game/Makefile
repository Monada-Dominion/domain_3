CC = gcc
CFLAGS = -I/opt/homebrew/include/SDL2 -D_REENTRANT
LDFLAGS = -L/opt/homebrew/lib -lSDL2

SRC = src/main.c src/card.c src/deck.c src/game.c
OBJ = $(SRC:.c=.o)

all: card_game

card_game: $(OBJ)
	$(CC) -o $@ $^ $(LDFLAGS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJ) card_game

