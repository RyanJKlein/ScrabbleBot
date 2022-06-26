import random

BOARD_SIDE_LEN = 15
LETTER_POINTS = {
    'A': 1,
    'B': 3,
    'C': 3,
    'D': 2,
    'E': 1,
    'F': 4,
    'G': 2,
    'H': 4,
    'I': 1,
    'J': 8,
    'K': 5,
    'L': 1,
    'M': 3,
    'N': 1,
    'O': 1,
    'P': 3,
    'Q': 10,
    'R': 1,
    'S': 1,
    'T': 1,
    'U': 1,
    'V': 4,
    'W': 4,
    'X': 8,
    'Y': 4,
    'Z': 10,
    '*': 0
}

BOARD_SCORES = [
    ['TW', 'NS', 'NS', 'DL', 'NS', 'NS', 'NS', 'TW', 'NS', 'NS', 'NS', 'DL', 'NS', 'NS', 'TW'],
    ['NS', 'DW', 'NS', 'NS', 'NS', 'TL', 'NS', 'NS', 'NS', 'TL', 'NS', 'NS', 'NS', 'DW', 'NS'],
    ['NS', 'NS', 'DW', 'NS', 'NS', 'NS', 'DL', 'NS', 'DL', 'NS', 'NS', 'NS', 'DW', 'NS', 'NS'],
    ['DL', 'NS', 'NS', 'DW', 'NS', 'NS', 'NS', 'DL', 'NS', 'NS', 'NS', 'DW', 'NS', 'NS', 'DL'],
    ['NS', 'NS', 'NS', 'NS', 'DW', 'NS', 'NS', 'NS', 'NS', 'NS', 'DW', 'NS', 'NS', 'NS', 'NS'],
    ['NS', 'TL', 'NS', 'NS', 'NS', 'TL', 'NS', 'NS', 'NS', 'TL', 'NS', 'NS', 'NS', 'TL', 'NS'],
    ['NS', 'NS', 'DL', 'NS', 'NS', 'NS', 'DL', 'NS', 'DL', 'NS', 'NS', 'NS', 'DL', 'NS', 'NS'],
    ['TL', 'NS', 'NS', 'DL', 'NS', 'NS', 'NS', 'DW', 'NS', 'NS', 'NS', 'DL', 'NS', 'NS', 'TW'],
    ['NS', 'NS', 'DL', 'NS', 'NS', 'NS', 'DL', 'NS', 'DL', 'NS', 'NS', 'NS', 'DL', 'NS', 'NS'],
    ['NS', 'TL', 'NS', 'NS', 'NS', 'TL', 'NS', 'NS', 'NS', 'TL', 'NS', 'NS', 'NS', 'TL', 'NS'],
    ['NS', 'NS', 'NS', 'NS', 'DW', 'NS', 'NS', 'NS', 'NS', 'NS', 'DW', 'NS', 'NS', 'NS', 'NS'],
    ['DL', 'NS', 'NS', 'DW', 'NS', 'NS', 'NS', 'DL', 'NS', 'NS', 'NS', 'DW', 'NS', 'NS', 'DL'],
    ['NS', 'NS', 'DW', 'NS', 'NS', 'NS', 'DL', 'NS', 'DL', 'NS', 'NS', 'NS', 'DW', 'NS', 'NS'],
    ['NS', 'DW', 'NS', 'NS', 'NS', 'TL', 'NS', 'NS', 'NS', 'TL', 'NS', 'NS', 'NS', 'DW', 'NS'],
    ['TW', 'NS', 'NS', 'DL', 'NS', 'NS', 'NS', 'TW', 'NS', 'NS', 'NS', 'DL', 'NS', 'NS', 'TW']
]



def next_spot(cord, horizontal):
    if horizontal:
        return cord[0]+1, cord[1]
    else:
        return cord[0], cord[1]+1


def last_spot(cord, horizontal):
    if horizontal:
        return cord[0]-1, cord[1]
    else:
        return cord[0], cord[1]-1


def calc_word_score(letters_dict):
    # Calculate the score of the placed tiles
    multiple = 1
    un_gained = 0
    for letter in letters_dict:
        letter_value = LETTER_POINTS[letter['LETTER']]
        spot = BOARD_SCORES[letter['POSITION'][0]][letter['POSITION'][1]]
        played = letter['PLAYED']
        if spot == 'TW' and played:
            multiple *= 3
            un_gained += letter_value
        elif spot == 'DW' and played:
            multiple *= 2
            un_gained += letter_value
        elif spot == 'TL' and played:
            un_gained += letter_value * 3
        elif spot == 'DL' and played:
            un_gained += letter_value * 2
        else:
            un_gained += letter_value
    return un_gained * multiple


class ScrabbleBoard:
    def __init__(self, log_file='scrabble_log.txt'):
        # Initialize board
        one_row = [None for x in range(BOARD_SIDE_LEN)]
        self.letter_placements = [one_row for x in range(BOARD_SIDE_LEN)]
        # FIXME name uniquely so we don't overwrite
        self.board_file = open(log_file, 'w')

    def __spot_empty(self, cord):
        if cord[0] < 0 or cord[0] > 14 or cord[1] < 0 or cord[1] > 14:
            return True
        else:
            return self.letter_placements[cord[0]][cord[1]] is None

    def __get_letter(self, cord):
        return self.letter_placements[cord[0]][cord[1]]

    def __get_played_words(self, word, position: tuple, horizontal):
        '''
        :param word: the primary word made in the turn, included non-placed tiles
        :param position: start position of the made word
        :param horizontal: True: word played horizontally; False: word played verical
        :return:
        '''
        if position[0] < 0 or position[0] > 14 or position[1] < 0 or position[1] > 14:
            raise IndexError('Placement is off the board!')
        words_made = []
        base_made = []
        cord = position
        idx = 0
        while (not self.__spot_empty(cord)) or idx < len(word):
            # Letter was already on the board
            if not self.__spot_empty(cord):
                played = False
            else:
                played = True
                # RECURSIVE STEP - find other words made if adjacent tiles are non-empty
                # Go to the top of the word
                cord_candidate = cord
                while not self.__spot_empty(cord_candidate):
                    cord_candidate = last_spot(cord_candidate, not horizontal)
                cord_candidate = next_spot(cord_candidate, not horizontal) # Move back to start of word
                # Go down until we reach an empty spot
                new_word_made = []
                while not self.__spot_empty(cord_candidate):
                    letter = self.__get_letter(cord_candidate)
                    letter_to_add = {
                        'LETTER': letter if letter else word[x], # Add letter on board if there, if not add played letter
                        'PLAYED': False if letter else True,
                        'POSITION': cord_candidate
                    }
                    new_word_made.append(letter_to_add)
                    cord_candidate = next_spot(cord_candidate, not horizontal)
                # Check if an actual word was made
                if len(new_word_made) > 1:
                    words_made.append(new_word_made)

            letter_to_add = {
                'LETTER': word[idx],
                'PLAYED': played,
                'POSITION': cord,
            }
            base_made.append(letter_to_add)
            cord = next_spot(cord, horizontal)
            idx += 1
        words_made.append(base_made)
        return words_made

    # Word dictionary format:
    # played_word = [
    #     {
    #         'LETTER': 'S',
    #         'PLAYED': True,
    #         'POSITION': (0, 0),
    #     },
    #     {
    #         'LETTER': 'R',
    #         'PLAYED': True,
    #         'POSITION': (1, 0),
    #     }]

    def add_to_board(self, word, position: tuple, horizontal):
        """

        :param word: word to play
        :param position: tuple of x,y coordinate to play turn; (0, 0) is upper left
        :param horizontal: True for horizontal
        :return: tuple (points scored, new letters)
        """
        # Verify board spot is not taken, and figure out special spots
        words_made = self.__get_played_words(word, position, horizontal)
        points = 0
        for word in words_made:
            points += calc_word_score(word)
        self.__save_board()
        return points

    def __save_board(self):
        """
        Saves the board to the log file
        :return:
        """
        as_str = ""
        for row in self.letter_placements:
            for letter in row:
                if not letter:
                    as_str += "_" + ","
                else:
                    as_str += letter + ","
            as_str = as_str[:-1] + '\n'
        self.board_file.write(as_str)

    def __del__(self):
        self.board_file.close()






