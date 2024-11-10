CC = gcc
CFLAGS = -Wall -g
BIN_DIR = ../bin
SRC_DIR = ../src_lama
ALG_DIR = $(SRC_DIR)/algorithm
FUN_DIR = $(ALG_DIR)/function

all: $(BIN_DIR)/main
	$(BIN_DIR)/main

$(BIN_DIR)/main: $(FUN_DIR)/magic_cube.c $(FUN_DIR)/array.c $(ALG_DIR)/random_restart_hill_climbing.c $(ALG_DIR)/simulated_annealing.c $(ALG_DIR)/genetic_algorithm.c $(SRC_DIR)/main.c
	$(CC) $(CFLAGS) -o $@ $^

clean:
	rm -f $(BIN_DIR)/main
	rm -rf $(BIN_DIR)/main.dSYM
	clear