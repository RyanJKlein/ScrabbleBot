import sys
import os
sys.path.append(os.getcwd())

import Board
import Game
import SimulateGame
from pathlib import Path

TEST_BOARD = False
TEST_GAME = False
TEST_SIM = True

if TEST_SIM:
    #SimulateGame.play_game(SimulateGame.lazy_brute_bot, SimulateGame.lazy_brute_bot)
    #SimulateGame.play_game(SimulateGame.lazy_brute_bot_smarter, SimulateGame.lazy_brute_bot_smarter)
    SimulateGame.play_game(SimulateGame.lazy_brute_bot_smarter, SimulateGame.lazy_brute_bot_smarter)

if TEST_GAME:
    game = Game.ScrabbleGame()
    game.add_player("Ryan")
    game.set_tiles("Ryan", ['A', 'B', 'E', 'F', 'P', 'E', 'D'])
    game.add_player("Kathy")
    game.set_tiles("Kathy", ['Q', 'U', 'I', 'T', 'P', 'E', 'D'])

    game.take_turn("Ryan", "DAB", (7, 7), True)
    game.set_tiles("Ryan", ['Y', 'A', 'E', 'F', 'P', 'E', 'G'])

if TEST_BOARD:
    board = Board.ScrabbleBoard(load=True)
    points = board.play_word('STREAM', (7, 7), False)
    print(points)

    board = Board.ScrabbleBoard(board_file='../ResultsArchive/board2.txt')
    points = board.play_word('STREAM', (7, 7), True)
    print(points)
    points = board.play_word('MAKE', (7, 12), False)
    print(points)
    points = board.play_word('MA', (8, 11), True)
    print(points)
    try:
        points = board.play_word('MATHPPPPPPPPPP', (8, 13), False)
    except:
        print("Hit error")
    points = board.play_word('MATH', (8, 13), False)
    print(points)
# Add to env variables:
# PYDEVD_USE_CYTHON = NO