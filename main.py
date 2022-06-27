import Board

board = Board.ScrabbleBoard(load=True)
points = board.play_word('STREAM', (7, 7), False)
print(points)

board = Board.ScrabbleBoard(board_file='board2.txt')
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