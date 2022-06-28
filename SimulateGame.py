import Game
import Board
import itertools

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


    word = None
    for perm in all_perms:
        if perm in word_dictionary:
            if board.empty():
                word = perm
                position = (7, 7)
                horizontal = True
                return word, position, horizontal
            else:
                # Try every position on the word, horizontal
                for horizontal in (False, True):
                    xrange = range(Board.BOARD_SIDE_LEN) if horizontal else range(Board.BOARD_SIDE_LEN - len(perm))
                    yrange = range(Board.BOARD_SIDE_LEN) if not horizontal else range(Board.BOARD_SIDE_LEN - len(perm))
                    for x in xrange:
                        for y in yrange:
                            matches_made = board.get_candidate_words(perm, (x, y), horizontal)
                            if valid_words(matches_made) and not board.word_overlaps(perm, (x, y), horizontal):
                                word = perm
                                position = (x, y)
                                return word, position, horizontal
                # No horizontal words worked, try vertical
    # Dirty, clean up
    if not word:
        raise ValueError("No valid turn found!")
    return word, position, horizontal

def valid_words(word_list):
    if len(word_list) < 2:
        return False
    else:
        for word in word_list:
            if word not in word_dictionary:
                return False
    return True

def play_game(player1_bot, player2_bot):
    global word_dictionary
    game = Game.ScrabbleGame(log_file_name='game_simulation.txt', sdata_name='game_simulation_data.txt',
                                  sim_bag=True)
    game.add_player('Player1')
    game.add_player('Player2')

    with open('Collins Scrabble Words (2019).txt', 'r') as file_dict:
        word_dictionary = []
        lines = file_dict.readlines()
        for line in lines:
            word_dictionary.append(line.strip())
    print("Loaded dictionary")

    player_up = 'Player1'
    while len(game.get_tiles('Player1')) > 0 and len(game.get_tiles('Player2')) > 0:
        bot = player1_bot if player_up == 'Player1' else player2_bot
        word, position, horizontal = bot(game.get_tiles(player_up), game.board)
        game.take_turn(player_up, word, position, horizontal)
        print(f'{player_up} played {word}')
        player_up = 'Player1' if player_up == 'Player2' else 'Player2'
    # GAME OVER
    print("Game complete!")



