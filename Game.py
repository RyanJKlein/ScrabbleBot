import Board
import random

LETTER_FREQUENCIES = {
    'A': 12
}

class ScrabbleGame:
    def __init__(self):
        # Create bag as a list in random order
        self.bag = []
        for letter, freq in LETTER_FREQUENCIES:
            to_add = [letter for x in range(freq)]
            self.bag.extend(to_add)
        random.shuffle(self.bag)
        # Other init
        self.players = 0
        self.player_scores = {}
        self.player_tiles = {}

    def add_player(self, name):
        self.player_scores[name] = 0
        self.player_tiles[name] = self.bag[:7]
        self.bag = self.bag[7:]