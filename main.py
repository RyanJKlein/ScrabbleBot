import Board

board = Board.ScrabbleBoard()
points = board.add_to_board('STREAM', (7, 7), True)
print(points)
points = board.add_to_board('MAKE', (12, 7), False)
print(points)
# Add to env variables:
# PYDEVD_USE_CYTHON = NO