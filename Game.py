import Board
import random

LETTER_FREQUENCIES = {
    'A': 9,
    'B': 2,
    'C': 2,
    'D': 4,
    'E': 12,
    'F': 2,
    'G': 3,
    'H': 2,
    'I': 9,
    'J': 1,
    'K': 1,
    'L': 4,
    'M': 2,
    'N': 6,
    'O': 8,
    'P': 2,
    'Q': 1,
    'R': 6,
    'S': 4,
    'T': 6,
    'U': 4,
    'V': 2,
    'W': 2,
    'X': 1,
    'Y': 2,
    'Z': 1,
    '*': 2
}

class ScrabbleGame:
    def __init__(self, log_file_name="scrabble_game.txt", sdata_name="game_data.txt", sim_bag=False):
        if sim_bag:
        # Create bag as a list in random order
            self.bag = []
            for letter in LETTER_FREQUENCIES:
                to_add = [letter for x in range(LETTER_FREQUENCIES[letter])]
                self.bag.extend(to_add)
            random.shuffle(self.bag)
        # Other init
        self.players = {}
        self.board = Board.ScrabbleBoard(log_file_name[:-4] + "_board.txt")
        self.sim_bag = sim_bag
        self.log_file = open(log_file_name, 'w+')

    def add_player(self, name, tiles=None):
        self.players[name] = {}
        self.players[name]['POINTS'] = 0
        if self.sim_bag:
            self.players[name]['TILES'] = self.bag[:7]
            self.bag = self.bag[7:]
        else:
            self.players[name]['TILES'] = tiles
        # Print to log

    def take_turn(self, name, word, position: tuple, horizontal):
        points = self.board.play_word(word, position, horizontal)
        self.players[name]['POINTS'] += points
        if self.sim_bag:
            for char in word:
                if char.isupper():
                    self.players[name]['TILES'].remove(char)
                else:
                    self.players[name]['TILES'].remove('*')
            game_over = False
            if len(self.bag) < len(word):
                self.players[name]['TILES'].extend(self.bag)
                self.bag = []
            elif len(self.get_tiles(name)) > 0:
                self.players[name]['TILES'].extend(self.bag[:len(word)])
                self.bag = self.bag[len(word):]
            else:
                game_over = True
        self.__update_log(f'{name} plays {word} at {position} for {points} points\n')
        if self.sim_bag and game_over:
            self.__update_log(f'**********************************************\n')
            self.__update_log(f'\nGAME OVER. FINAL SCORE:\n')
            for player in self.players:
                name = self.players[player]['NAME']
                points = self.players[player]['POINTS']
                self.__update_log(f'{name}: {points}\n')
            self.__update_log(f'**********************************************\n')

        self.__log_score()
        return points

    def set_tiles(self, name, tiles):
        self.players[name]['TILES'] = tiles

    def get_tiles(self, name):
        return self.players[name]['TILES']

    def __update_log(self, message):
        self.log_file.write(message)

    def __log_score(self):
        for player in self.players:
            self.__update_log(f'{player}: {self.players[player]["POINTS"]}\t')
        self.__update_log("\n")

    def trade_all_tiles(self, name):
        old_tiles = self.players[name]['TILES']
        if len(self.bag) > 0:
            if len(self.bag) < 7:
                traded_tiles = old_tiles[:len(self.bag)]
                self.players[name]['TILES'] = self.players[name]['TILES'][:len(self.bag)]
                self.players[name]['TILES'].extend(self.bag)
                self.bag = traded_tiles
            else:
                self.players[name]['TILES'] = self.bag[:7]
                self.bag = self.bag[7:]
                self.bag.extend(old_tiles)

    def __del__(self):
        self.log_file.close()
