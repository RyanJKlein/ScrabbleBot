from Source import Board, Game
import itertools
import Input.ScrabbleConstants as Scrabble
import os
word_dictionary = []

def lazy_brute_bot(tiles, board: Board.ScrabbleBoard):
    """
    Picks the first valid 5 letter word it finds with the first 5 letters. Disregards blanks.
    Does not allow overlap.
    :param tiles: players tiles
    :param board: current game board
    :return: word, position, horizontal
    """
    perm_val = len(tiles) if len(tiles) < 5 else 5

    all_perms = []
    done = False
    while not done:
        combos = list(itertools.combinations(tiles, perm_val))
        for combo in combos:
            all_perms.extend([''.join(p) for p in itertools.permutations(combo)])
        perm_val -= 1
        if perm_val < 2:
            done = True

    for perm in all_perms:
        if valid_word(perm):
            if board.empty():
                word = perm
                position = (7, 7)
                horizontal = True
                return word, position, horizontal
            else:
                # Try every position on the word, horizontal
                for horizontal in (False, True):
                    xrange = range(Scrabble.BOARD_SIDE_LEN) if horizontal else range(Scrabble.BOARD_SIDE_LEN - len(perm))
                    yrange = range(Scrabble.BOARD_SIDE_LEN) if not horizontal else range(Scrabble.BOARD_SIDE_LEN - len(perm))
                    for x in xrange:
                        for y in yrange:
                            matches_made = board.get_candidate_words(perm, (x, y), horizontal)
                            if valid_words(matches_made) and not board.word_overlaps(perm, (x, y), horizontal):
                                word = perm
                                position = (x, y)
                                return word, position, horizontal
                # No horizontal words worked, try vertical
    # Dirty, clean up
    return None, None, None


# Blanks are lowercase
ALL_ENGLISH_LETTERS = [chr(x) for x in range(97, 97+26)]
COMMON_ENGLISH_LETTERS = ['e', 'r', 's', 't']
def lazy_brute_bot_smarter(tiles, board: Board.ScrabbleBoard, blanks=COMMON_ENGLISH_LETTERS, check_segments=True):
    """
    Only uses 5 letters at a time, but will use blanks
    :param tiles: players tiles
    :param board: current game board
    :return: word, position, horizontal
    """
    perm_val = len(tiles) if len(tiles) < 5 else 5

    all_perms = []
    done = False
    # start_make_combos = time.time()
    while not done:
        combos = list(itertools.combinations(tiles, perm_val))
        for combo in combos:
            all_perms.extend([''.join(p) for p in itertools.permutations(combo)])
        perm_val -= 1
        if perm_val < 2:
            done = True
    # duration = time.time() - start_make_combos
    # print(f"Time to make combos: {duration} seconds")

    for perm_raw in all_perms:
        blanked_perms = []
        if "*" in perm_raw:
            for char_idx in range(len(perm_raw)):
                if perm_raw[char_idx] == '*':
                    for letter in blanks:
                        new_perm = perm_raw[:char_idx]
                        new_perm += letter
                        new_perm += perm_raw[char_idx+1:]
                        blanked_perms.append(new_perm)
        else:
            blanked_perms.append(perm_raw)
        for perm in blanked_perms:
            if valid_word(perm.upper()) or (check_segments and valid_word_segment(perm.upper())):
                if board.empty():
                    word = perm
                    position = (7, 7)
                    horizontal = True
                    return word, position, horizontal
                else:
                    for horizontal in (False, True):
                        xrange = range(Scrabble.BOARD_SIDE_LEN) if horizontal else range(Scrabble.BOARD_SIDE_LEN - len(perm))
                        yrange = range(Scrabble.BOARD_SIDE_LEN) if not horizontal else range(
                            Scrabble.BOARD_SIDE_LEN - len(perm))
                        for x in xrange:
                            for y in yrange:
                                if board.connects((x, y), len(perm), horizontal):
                                    matches_made = board.get_candidate_words(perm, (x, y), horizontal)
                                    if valid_words(matches_made) and not board.word_overlaps(perm, (x, y), horizontal):
                                        word = perm
                                        position = (x, y)
                                        return word, position, horizontal
    # Dirty, clean up
    return None, None, None


def bot_three(tiles, board: Board.ScrabbleBoard, blanks=COMMON_ENGLISH_LETTERS):
    """
    Searches for
    :param tiles: players tiles
    :param board: current game board
    :return: word, position, horizontal
    """
    perm_val = len(tiles) if len(tiles) < 5 else 5



def valid_word(word):
    return word in word_dictionary

# FIXME - implement
def valid_word_segment(word):
    for item in word_dictionary:
        if word in item:
            return True
    return False

def valid_words(word_list):
    if len(word_list) < 2:
        return False
    else:
        for word in word_list:
            if not valid_word(word.upper()):
                return False
    return True

def play_game(player1_bot, player2_bot, dictionary_path=None):
    global word_dictionary
    if not dictionary_path:
        current_folder = os.path.basename(os.getcwd())
        if current_folder == 'Source':
            os.chdir('..')
        dictionary_path = os.path.join(os.getcwd(), 'Input', 'scrabble_dictionary.txt')
    game = Game.ScrabbleGame(log_file_name="game_simulation.txt", sdata_name='game_simulation_data.txt',
                             sim_bag=True)
    game.add_player('Player1')
    game.add_player('Player2')

    with open(dictionary_path, 'r') as file_dict:
        word_dictionary = []
        lines = file_dict.readlines()
        for line in lines:
            word_dictionary.append(line.strip())
    print("Loaded dictionary")

    player_up = 'Player1'
    consec_trades = 0
    while len(game.get_tiles('Player1')) > 0 and len(game.get_tiles('Player2')) > 0 and consec_trades < 6:
        bot = player1_bot if player_up == 'Player1' else player2_bot
        word, position, horizontal = bot(game.get_tiles(player_up), game.board)
        if word:
            print(f'{player_up} played {word} for ', end='')
            points = game.take_turn(player_up, word, position, horizontal)
            print(f'{points} points')
            consec_trades = 0
        else:
            orig_tiles = game.get_tiles(player_up)
            game.trade_all_tiles(player_up)
            print(f'{player_up} trades in all letters; traded letters: {orig_tiles}')
            consec_trades += 1
        if '*' in game.get_tiles(player_up):
            print(f'{player_up} has a blank')
        player_up = 'Player1' if player_up == 'Player2' else 'Player2'
    # GAME OVER
    print("Game complete!")



