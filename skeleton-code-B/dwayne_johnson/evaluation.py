import dwayne_johnson.constant as constant


def evaluate_board(our_tokens, opponent_tokens, our_throws, opponent_throws):
    """
    Evaluates the position of the board
    Args:
        our_tokens: a dictionary containing our tokens
        opponent_tokens: a dictionary containing the opponent's tokens
        our_throws: the number of throws we have remaining
        opponent_throws: the number of throws the opponent has remaining

    Returns: a single number evaluation of the current game state

    """
    # Number of tokens each player has
    board_eval = count_tokens(our_tokens) - count_tokens(opponent_tokens)
    # Number of tokens left to throw
    throw_eval = opponent_throws - our_throws
    # What types of tokens each player has
    token_eval = token_counts(our_tokens, opponent_tokens)
    # How close tokens are to being taken
    distance_eval = token_distances(our_tokens, opponent_tokens)
    # Invincible Tokens
    invincible_eval = invincible_tokens(our_tokens, opponent_tokens)
    return board_eval * constant.BOARD_WEIGHT + throw_eval * constant.THROW_WEIGHT + \
        token_eval * constant.TOKEN_WEIGHT + distance_eval * constant.DISTANCE_WEIGHT + \
        invincible_eval * constant.INVINCIBLE_WEIGHT


def distance_between(token1, token2):
    """
    Adapted from code obtained from https://www.redblobgames.com/grids/hexagons/
    Args:
        token1: the first token to find distance between
        token2: the second token to find distance between

    Returns: the distance between the two tokens

    """
    cube1 = axial_to_cube(token1)
    cube2 = axial_to_cube(token2)
    return (abs(cube1[0] - cube2[0]) + abs(cube1[1] - cube2[1]) + abs(cube1[2] - cube2[2])) / 2


def axial_to_cube(token):
    """
    Adapted from code obtained from https://www.redblobgames.com/grids/hexagons/
    Args:
        token: the token in axial coordinates form

    Returns: the token in cube coordinates form

    """
    x = token[1]
    z = token[0]
    y = -x - z
    return [x, y, z]


def count_tokens(tokens):
    """
    Counts the number of tokens a player has
    Args:
        tokens: a dictionary containing a player's tokens

    Returns: the number of tokens the player has

    """
    number = 0
    for token in tokens.keys():
        number += len(tokens[token])
    return number


def get_ratio(number1, number2):
    """
    Gets a ratio between two numbers
    Args:
        number1: the numerator
        number2: the denominator

    Returns: A decimal representation of a ratio between two numbers

    """
    if number2 == 0:
        return 0
    else:
        return number1 / number2


def token_counts(our_tokens, opponent_tokens):
    """
    Evaluates the number of each type of token for each player
    Args:
        our_tokens: a dictionary containing our tokens
        opponent_tokens: a dictionary containing the opponent's tokens

    Returns: An single number evaluation of the token types the players currently have

    """
    token_eval = 0
    token_eval += get_ratio(len(our_tokens["r"]), len(opponent_tokens["s"]))
    token_eval += get_ratio(len(our_tokens["p"]), len(opponent_tokens["r"]))
    token_eval += get_ratio(len(our_tokens["s"]), len(opponent_tokens["p"]))

    token_eval -= get_ratio(len(opponent_tokens["r"]), len(our_tokens["s"]))
    token_eval -= get_ratio(len(opponent_tokens["p"]), len(our_tokens["r"]))
    token_eval -= get_ratio(len(opponent_tokens["s"]), len(our_tokens["p"]))

    return token_eval


def token_distances(our_tokens, opponent_tokens):
    """
    Evaluates the distance between tokens on the board
    Args:
        our_tokens: a dictionary containing our tokens
        opponent_tokens: a dictionary containing the opponent's tokens

    Returns: a single number evaluation of the distances between tokens

    """
    distance_eval = 0

    for ally in our_tokens["r"]:
        for opponent in opponent_tokens["s"]:
            distance_eval += constant.MAX_DISTANCE - distance_between(ally, opponent)
        for opponent in opponent_tokens["p"]:
            distance_eval -= constant.MAX_DISTANCE - distance_between(ally, opponent)

    for ally in our_tokens["p"]:
        for opponent in opponent_tokens["r"]:
            distance_eval += constant.MAX_DISTANCE - distance_between(ally, opponent)
        for opponent in opponent_tokens["s"]:
            distance_eval -= constant.MAX_DISTANCE - distance_between(ally, opponent)

    for ally in our_tokens["s"]:
        for opponent in opponent_tokens["p"]:
            distance_eval += constant.MAX_DISTANCE - distance_between(ally, opponent)
        for opponent in opponent_tokens["r"]:
            distance_eval -= constant.MAX_DISTANCE - distance_between(ally, opponent)

    return distance_eval


def invincible_tokens(player_tokens, opponent_tokens):
    """
    An evaluation of the opponent's invincible tokens
    Args:
        player_tokens: a dictionary containing our tokens
        opponent_tokens: a dictionary containing the opponent's tokens

    Returns: -1 if the opponent currently has any invincible tokens and 0 otherwise

    """
    if opponent_tokens["r"] and not player_tokens["p"]:
        return -1
    elif opponent_tokens["p"] and not player_tokens["s"]:
        return -1
    elif opponent_tokens["s"] and not player_tokens["r"]:
        return -1
    return 0
