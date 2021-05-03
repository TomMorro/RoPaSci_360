import evaluation


# Create a Payoff Matrix
def create_payoff_matrix(our_tokens, opponents_tokens, our_throws, opponents_throws):
    payoff = {}  # Overall payoff matrix
    our_moves = []  # Collection of all our possible moves
    opponents_moves = []  # Collection of all opponent possible moves

    # generate possible moves for each player
    our_moves = generate_moves(our_tokens, our_throws)
    opponents_moves = generate_moves(opponents_tokens, opponents_throws)

    for our_move in our_moves:
        for opponents_move in opponents_moves:
            move_combo = (our_move, opponents_move)
            new_board = simulate_move(our_move, opponents_move)
            payoff[move_combo] = evaluation.evaluate_board(new_board[0], new_board[1], new_board[2], new_board[3])


# Finds all potential valid slide moves for a token
def find_slide_moves(cell):
    r = cell[0]
    q = cell[1]

    surroundings = [(r + 1, q), (r - 1, q), (r, q + 1), (r, q - 1), (r + 1, q - 1), (r - 1, q + 1)]

    new_surroundings = []
    for cell in surroundings:
        if check_on_board(cell):
            new_surroundings.append(cell)

    return new_surroundings


# Finds all potential valid swing moves for a token
def find_swing_moves(cell):
    return 0


# Check that a given cell coordinate is actually on the board
def check_on_board(cell):
    """
    Checks if a certain cell is on the board, returning whether it is or not
    """
    if cell[0] > 4 or cell[0] < -4 or cell[1] > 4 or cell[1] < -4:
        return False
    if cell[0] + cell[1] > 4 or cell[0] + cell[1] < -4:
        return False

        return True


# Generates the set of all possible moves for a player
def generate_moves(tokens, throws):
    possible_moves = []
    # Add all possible swings and slides
    for token_type in tokens.keys():
        for token in token_type:
            slides = find_slide_moves(token)
            for move in slides:
                possible_moves.append((token, move))

            swings = find_swing_moves(token)
            for move in swings:
                possible_moves.append((token, move))

    # Add all possible throws
    throw_locations = find_throwable_cells(our_throws)
    for cell in throw_locations:
        for i in range(0,2):
            if i == 0:
                possible_moves.append(paper, cell)
            elif i == 1:
                possible_moves.append(rock, cell) # Fix notation once figured out a representation
            else:
                possible_moves.append(scissors, cell)

    return possible_moves


# Finds the cells capable of being thrown to
def find_throwable_cells(throws):
    return 0