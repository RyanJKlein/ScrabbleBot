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
        if cord[1] + 1 >= BOARD_SIDE_LEN:
            return None
        else:
            return cord[0], cord[1]+1
    else:
        if cord[0] + 1 >= BOARD_SIDE_LEN:
            return None
        else:
            return cord[0]+1, cord[1]


def last_spot(cord, horizontal):
    if horizontal:
        if cord[1] - 1 < 0:
            return None
        else:
            return cord[0], cord[1]-1
    else:
        if cord[0] - 1 < 0:
            return None
        else:
            return cord[0]-1, cord[1]


def calc_word_score(letters_dict):
    # Calculate the score of the placed tiles
    multiple = 1
    un_gained = 0
    for letter_dict in letters_dict:
        letter = letter_dict['LETTER']
        if not letter == letter.upper():
            letter = '*'
        letter_value = LETTER_POINTS[letter]
        spot = BOARD_SCORES[letter_dict['POSITION'][0]][letter_dict['POSITION'][1]]
        played = letter_dict['PLAYED']
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
    def __init__(self, board_file='scrabble_board.txt', load=False):
        self.letter_placements = []
        self.file_name = board_file
        # If not loading from file, create new board
        if not load:
            for row in range(BOARD_SIDE_LEN):
                self.letter_placements.append([])
                for col in range(BOARD_SIDE_LEN):
                    self.letter_placements[row].append('_')
        else:
            with open(board_file, 'r') as in_file:
                lines = in_file.readlines()
                for line in lines:
                        self.letter_placements.append(line.strip().split(','))
            self.__save_board()

    def __spot_empty(self, cord):
        if not cord:
            return False
        if cord[0] < 0 or cord[0] > 14 or cord[1] < 0 or cord[1] > 14:
            return True
        else:
            return self.letter_placements[cord[0]][cord[1]] == '_'

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
        played_idx = 0
        word = self.get_prefixed_word(word, position, horizontal)
        while (not self.__spot_empty(cord)) or played_idx < len(word):
            # Letter was already on the board
            if not self.__spot_empty(cord):
                played = False
            else:
                played = True
                # Get other words made
                # Go to the top of the word
                cord_candidate = cord
                first_tile = True
                while first_tile or (cord_candidate and not self.__spot_empty(cord_candidate)):
                    last_valid_cord = cord_candidate
                    cord_candidate = last_spot(cord_candidate, not horizontal)
                    first_tile = False
                cord_candidate = last_valid_cord
                # Go down until we reach an empty spot
                new_word_made = []
                while cord_candidate and (not self.__spot_empty(cord_candidate) or cord_candidate == cord):
                    if cord_candidate == cord:
                        letter = word[played_idx]
                    else:
                        letter = self.__get_letter(cord_candidate)
                    letter_to_add = {
                        'LETTER': letter, # Add letter on board if there, if not add played letter
                        'PLAYED': True if cord_candidate == cord else False,
                        'POSITION': cord_candidate
                    }
                    new_word_made.append(letter_to_add)
                    cord_candidate = next_spot(cord_candidate, not horizontal)
                    last = cord_candidate
                # Check if an actual word was made
                if len(new_word_made) > 1:
                    words_made.append(new_word_made)
                played_idx += 1

            letter_to_add = {
                # Minus 1 since we inc'd in loop
                'LETTER': word[played_idx-1] if played else self.__get_letter(cord),
                'PLAYED': played,
                'POSITION': cord,
            }
            base_made.append(letter_to_add)
            cord = next_spot(cord, horizontal)
            if not cord:
                break
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

    def play_word(self, word, position: tuple, horizontal):
        """

        :param word: word to play
        :param position: tuple of x,y coordinate to play turn; (0, 0) is upper left
        :param horizontal: True for horizontal
        :return: tuple (points scored, new letters)
        """
        # Retrieve words made in this turn
        words_made = self.__get_played_words(word, position, horizontal)
        # Calculate points for turn
        points = 0
        for word in words_made:
            points += calc_word_score(word)
        # Add word to board - only do "base" word since that must include all tiles placed
        for letter_data in words_made[-1]:
            cord = letter_data['POSITION']
            letter = letter_data['LETTER']
            if self.__spot_empty(cord):
                self.place_tile(letter, cord)
        # Write board to file
        self.__save_board()
        return points

    def __save_board(self):
        """
        Saves the board to the log file
        :return:
        """
        # Close then re-open file in 'w' to clear it
        self.board_file = open(self.file_name, 'w')
        as_str = ""
        for row in self.letter_placements:
            for letter in row:
                if not letter:
                    as_str += "_" + ","
                else:
                    as_str += letter + ","
            as_str = as_str[:-1] + '\n'
        self.board_file.write(as_str)
        self.board_file.close()

    def place_tile(self, letter, cord):
        x = cord[0]
        y = cord[1]
        self.letter_placements[x][y] = letter

    def empty(self):
        return self.__get_letter((7,7)) == '_'

    def get_candidate_words(self, word, position, horizontal):
        words_list = self.__get_played_words(word, position, horizontal)
        words_made = []
        for word_data in words_list:
            candidate_word = ""
            for letter_data in word_data:
                candidate_word += letter_data['LETTER']
            words_made.append(candidate_word)
        return words_made

    def word_overlaps(self, word, position, horizontal):
        cord = position
        for letter in word:
            if not self.__spot_empty(cord):
                return True
            cord = next_spot(cord, horizontal)
        return False

    def __del__(self):
        print("Game over")

    def get_prefixed_word(self, word, position, horizontal):
        cord = last_spot(position, horizontal)
        while cord and not self.__spot_empty(cord):
            word = self.__get_letter(cord) + word
            cord = last_spot(cord, horizontal)
        return word






