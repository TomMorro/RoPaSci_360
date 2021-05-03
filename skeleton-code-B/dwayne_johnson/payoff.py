import evaluation
import simulate


# Create a Payoff Matrix
def create_payoff_matrix(our_tokens, opponents_tokens, our_throws, opponents_throws, is_upper):
    payoff = []  # Overall payoff matrix

    # generate possible moves for each player
    our_moves = generate_moves(our_tokens, our_throws, is_upper)
    opponents_moves = generate_moves(opponents_tokens, opponents_throws, not is_upper)

    # generate the util
    for opponents_move in opponents_moves:
        row = []
        for our_move in our_moves:
            new_board = simulate.simulate_move(our_move, opponents_move)
            value = evaluation.evaluate_board(new_board[0], new_board[1], new_board[2], new_board[3])
            row.append(value)
        payoff.append(row)


def find_slide_moves(origin):
    """
    Finds the possible slide moves
    Args:
        origin: the token to slide

    Returns: a list of possible coordinates to slide to

    """
    r = origin[0]
    q = origin[1]

    surroundings = find_surroundings(r, q)

    new_surroundings = []
    for cell in surroundings:
        if check_on_board(cell):
            new_surroundings.append(cell)

    return new_surroundings


def find_swing_moves(origin, other_tokens):
    """
    Finds the possible swing moves
    Args:
        origin: the token to swing
        other_tokens: the other tokens controlled by that player

    Returns: a list of possible coordinates to swing to

    """
    r = origin[0]
    q = origin[1]

    surroundings = find_surroundings(r, q)

    swing_cells = []
    for cell in surroundings:
        if cell in other_tokens['R'] or cell in other_tokens['P'] or cell in other_tokens['S']:
            x = cell[0]
            y = cell[1]
            swing_surrounds = find_surroundings(x, y)
            for token in swing_surrounds:
                if check_on_board(token) and token not in surroundings and token not in swing_cells and token != origin:
                    swing_cells.append(token)

    return swing_cells


def check_on_board(cell):
    """
    Checks that a given cell coordinate is on the board
    Args:
        cell: the given cell

    Returns: whether the cell is in a legal position on the board

    """
    if cell[0] > 4 or cell[0] < -4 or cell[1] > 4 or cell[1] < -4:
        return False
    if cell[0] + cell[1] > 4 or cell[0] + cell[1] < -4:
        return False

    return True


# Generates the set of all possible moves for a player
def generate_moves(tokens, throws, is_upper):
    possible_moves = []
    # Add all possible swings and slides
    for token_type in tokens.keys():
        for token in tokens[token_type]:
            slides = find_slide_moves(token)
            for move in slides:
                possible_moves.append(("SLIDE", token, move))

            swings = find_swing_moves(token, tokens)
            for move in swings:
                possible_moves.append(("SWING", token, move))

    throw_locations = find_throwable_cells(throws, is_upper)
    for cell in throw_locations:
        for i in range(0, 2):
            if i == 0:
                possible_moves.append(("THROW", "P", cell))
            elif i == 1:
                possible_moves.append(("THROW", "R", cell))  # Fix notation once figured out a representation
            else:
                possible_moves.append(("THROW", "S", cell))

    return possible_moves


# Finds the cells capable of being thrown to
def find_throwable_cells(throws, is_upper):
    """
    Finds the cells able to be thrown to for a player
    Args:
        throws: the number of throws the player has done
        is_upper: whether the player is upper or lower

    Returns: a list of cells that can be thrown to

    """
    i = 4
    throwable_cells = []
    while i + throws >= 4 and throws < 9:
        if i >= 0:
            j = -4
        else:
            j = -4 - i
        while j + i <= 4 and j <= 4:
            if is_upper:
                cell = (i, j)
            else:
                cell = (-i, -j)
            throwable_cells.append(cell)
            j += 1
        i -= 1
    return throwable_cells


def find_surroundings(r, q):
    """
    Finds the surrounding cells of given coordinates
    Args:
        r: the hexagonal row
        q: the hexagonal column

    Returns: the surroundings of a cell

    """
    return [(r + 1, q), (r - 1, q), (r, q + 1), (r, q - 1), (r + 1, q - 1), (r - 1, q + 1)]
