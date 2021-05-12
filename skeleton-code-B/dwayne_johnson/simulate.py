import copy
import random
import dwayne_johnson.evaluation as evaluation
import dwayne_johnson.board as board
import dwayne_johnson.gametheory as game_theory
import dwayne_johnson.constant as const


def simulate_move_tree(our_tokens, opponents_tokens, our_throws, opponents_throws, is_upper, current_depth, limit):
    """
    Recursively simulate moves into the future in order to select an appropriate move
    Args:
        our_tokens: a dictionary containing our tokens
        opponents_tokens: a dictionary containing the opponent's tokens
        our_throws: the number of throws we have remaining
        opponents_throws: the number of throws the opponent has remaining
        is_upper: whether our player is upper
        current_depth: the current depth of the search
        limit: the depth limit of the search

    Returns: At the top level, a move and at lower levels, the guaranteed maximum expected value of the equilibrium
    mixed strategy

    """
    # On first call, we are simply generating all our immediate moves
    if current_depth == 0:
        payoff = []  # Overall payoff matrix

        # generate possible moves for each player
        our_moves = generate_moves(our_tokens, opponents_tokens, our_throws, is_upper, is_player=True)
        opponents_moves = generate_moves(opponents_tokens, our_tokens, opponents_throws, not is_upper, is_player=False)

        our_moves = prune_moves(our_moves, opponents_moves, our_tokens, opponents_tokens, our_throws, opponents_throws)
        opponents_moves = prune_moves(opponents_moves, our_moves, opponents_tokens, our_tokens, opponents_throws,
                                      our_throws)

        # If too many moves to consider, don't look into future
        if len(our_moves) * len(opponents_moves) > const.TOP_LEVEL_LIMIT:
            current_depth = limit - 1

        # generate the util
        for our_move in our_moves:
            row = []
            for opponents_move in opponents_moves:
                new_board = board.perform_move(our_move, opponents_move, copy.deepcopy(our_tokens),
                                               copy.deepcopy(opponents_tokens), our_throws, opponents_throws)
                value = recursive_move_tree(new_board[0], new_board[1], new_board[2], new_board[3], is_upper,
                                            current_depth + 1, limit)
                row.append(value)
            payoff.append(row)

        if not opponents_moves:
            move = random.choices(our_moves)
        else:
            possible_moves = game_theory.solve_game(payoff)[0]
            move = random.choices(our_moves, weights=possible_moves)

        return move

    # On subsequent calls we are returning the maximums of each subgame being solved


def recursive_move_tree(our_tokens, opponents_tokens, our_throws, opponents_throws, is_upper, current_depth, limit):
    if 0 < current_depth < limit:
        tree = []  # Overall payoff matrix

        # generate possible moves for each player
        our_moves = generate_moves(our_tokens, opponents_tokens, our_throws, is_upper, is_player=True)
        opponents_moves = generate_moves(opponents_tokens, our_tokens, opponents_throws, not is_upper, is_player=False)

        our_moves = prune_moves(our_moves, opponents_moves, our_tokens, opponents_tokens, our_throws, opponents_throws)
        opponents_moves = prune_moves(opponents_moves, our_moves, opponents_tokens, our_tokens, opponents_throws,
                                      our_throws)
        
        if len(our_moves) * len(opponents_moves) > const.RECURSIVE_LIMIT:
            return evaluation.evaluate_board(our_tokens, opponents_tokens, our_throws, opponents_throws)

        # generate the util
        for our_move in our_moves:
            row = []
            for opponents_move in opponents_moves:
                new_board = board.perform_move(our_move, opponents_move, copy.deepcopy(our_tokens),
                                               copy.deepcopy(opponents_tokens), our_throws, opponents_throws)
                value = recursive_move_tree(new_board[0], new_board[1], new_board[2], new_board[3], is_upper,
                                            current_depth + 1, limit)
                row.append(value)
            tree.append(row)

        # if one of the players have no moves, just return the eval of the current board as the max
        if not our_moves or not opponents_moves:
            maximum = evaluation.evaluate_board(our_tokens, opponents_tokens, our_throws, opponents_throws)
        else:
            maximum = (game_theory.solve_game(tree))[1]
        return maximum

    # At a leaf so simply return eval of board
    elif current_depth == limit:
        return evaluation.evaluate_board(our_tokens, opponents_tokens, our_throws, opponents_throws)


def prune_moves(player_moves, opponent_moves, player_tokens, opponent_tokens, player_throws, opponent_throws):
    pruned_moves = []

    for player_move in player_moves:
        row = []
        for opponent_move in opponent_moves:
            new_board = board.perform_move(player_move, opponent_move, copy.deepcopy(player_tokens),
                                           copy.deepcopy(opponent_tokens), player_throws, opponent_throws)
            value = evaluation.evaluate_board(new_board[0], new_board[1], new_board[2], new_board[3])
            row.append(value)
        pair_value = (player_move, row)
        pruned_moves = prune_rows(pair_value, pruned_moves)

    player_moves.clear()
    for move in pruned_moves:
        player_moves.append(move[0])

    return player_moves


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
        if cell in other_tokens["r"] or cell in other_tokens["p"] or cell in other_tokens["s"]:
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
    if cell[0] > const.BOARD_BOUNDARY or cell[0] < -const.BOARD_BOUNDARY or cell[1] > const.BOARD_BOUNDARY \
            or cell[1] < -const.BOARD_BOUNDARY:
        return False
    if cell[0] + cell[1] > const.BOARD_BOUNDARY or cell[0] + cell[1] < -const.BOARD_BOUNDARY:
        return False

    return True


def generate_moves(tokens, opponent_pieces, throws, is_upper, is_player):
    """
    Generates the set of all possible moves for a player
    Args:
        tokens: a dictionary containing the current player's tokens
        opponent_pieces: a dictionary containing the current opponent's tokens
        throws: the number of throws the current player has made
        is_upper: whether the current player is the upper player
        is_player: whether the current player is the player we control

    Returns: A list of possible moves for the current player

    """
    possible_moves = []
    # Add all possible swings and slides
    for token_type in tokens.keys():
        for token in tokens[token_type]:
            slides = find_slide_moves(token)
            for move in slides:
                if is_player:
                    if not board.find_token(move, tokens):
                        possible_moves.append(("SLIDE", token, move))
                else:
                    possible_moves.append(("SLIDE", token, move))

            swings = find_swing_moves(token, tokens)
            for move in swings:
                if is_player:
                    if not board.find_token(move, tokens):
                        possible_moves.append(("SWING", token, move))
                else:
                    possible_moves.append(("SWING", token, move))

    throw_locations = find_throwable_cells(throws, is_upper)
    throw_locations = prune_throws(throw_locations, tokens, throws, opponent_pieces, is_player, is_upper)

    for cell in throw_locations:
        for i in range(0, 3):
            if i == 0:
                possible_moves.append(("THROW", "p", cell))
            elif i == 1:
                possible_moves.append(("THROW", "r", cell))  # Fix notation once figured out a representation
            else:
                possible_moves.append(("THROW", "s", cell))

    return possible_moves


def find_throwable_cells(throws, is_upper):
    """
    Finds the cells able to be thrown to for a player
    Args:
        throws: the number of throws the player has done
        is_upper: whether the player is upper or lower

    Returns: a list of cells that can be thrown to

    """
    i = const.BOARD_BOUNDARY
    throwable_cells = []
    while i + throws >= const.BOARD_BOUNDARY and throws < const.MAX_THROWS:
        if i >= 0:
            j = -const.BOARD_BOUNDARY
        else:
            j = -const.BOARD_BOUNDARY - i
        while j + i <= const.BOARD_BOUNDARY and j <= const.BOARD_BOUNDARY:
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


def prune_throws(throw_locations, current_player, curr_player_throws, other_player, is_player, is_upper):
    """
    Prunes throws in order to increase efficiency
    Args:
        throw_locations: a list of all possible throws
        current_player: a dictionary containing the current player's tokens
        curr_player_throws: the number of throws of the current player
        other_player: a dictionary containing the current opponent's tokens
        is_player: whether the current player is the player we control
        is_upper: whether the current player is upper

    Returns: A pruned list of possible throws

    """
    new_throw_locations = []

    for cell in throw_locations:
        if cell in current_player["r"] and cell in current_player["p"] and cell in current_player["s"]:
            continue
        if not is_player:
            if not board.find_token(cell, other_player):
                continue
        else:
            row_num = cell[0]
            if not is_upper:
                row_num = -row_num
            value = row_num + curr_player_throws
            if value != const.BOARD_BOUNDARY and not board.find_token(cell, other_player):
                continue
        new_throw_locations.append(cell)

    return new_throw_locations


def prune_rows(new_pair, previous_pairs):
    """
    Prune moves based on whether they get dominated
    Args:
        new_pair: the new pair of the move and its' evaluation for every opposing move
        previous_pairs: the previous pairs of moves and evaluations

    Returns: a new list of pairs, where dominated moves have been pruned out

    """
    updated_pairs = []

    if previous_pairs:
        for previous_pair in previous_pairs:
            value = compare_rows(new_pair, previous_pair)
            if value == 1:
                return previous_pairs
            elif value == 0:
                updated_pairs.append(previous_pair)

    updated_pairs.append(new_pair)
    return updated_pairs


def compare_rows(row1, row2):
    """
    Compares two moves
    Args:
        row1: a list containing the first move's evaluations
        row2: a list containing the second move's evaluations

    Returns: 1 if the first move is dominated, -1 if the second move is dominated, 0 if neither are dominated

    """
    row1_dominated = True
    row2_dominated = True

    if len(row1[1]) == 0:
        return 0

    for i in range(0, len(row1[1])):
        if row1[1][i] > row2[1][i]:
            row1_dominated = False
        elif row1[1][i] < row2[1][i]:
            row2_dominated = False
        if not row1_dominated and not row2_dominated:
            break

    if row1_dominated:
        return 1
    if row2_dominated:
        return -1
    return 0
