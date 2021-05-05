import dwayne_johnson.constant as constant


def evaluate_board(our_tokens, opponent_tokens, our_throws, opponent_throws):
    # Number of tokens each player has
    board_eval = count_tokens(our_tokens) - count_tokens(opponent_tokens)
    # Number of tokens left to throw
    throw_eval = opponent_throws - our_throws
    # What types of tokens each player has
    token_eval = token_counts(our_tokens, opponent_tokens)
    # How close tokens are to being taken
    distance_eval = token_distances(our_tokens, opponent_tokens)
    return board_eval * constant.BOARD_WEIGHT + throw_eval * constant.THROW_WEIGHT + \
        token_eval * constant.TOKEN_WEIGHT + distance_eval * constant.DISTANCE_WEIGHT


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
    number = 0
    for token in tokens.keys():
        number += len(tokens[token])
    return number


def get_ratio(number1, number2):
    if number2 == 0:
        return 0
    else:
        return number1 / number2


def token_counts(our_tokens, opponent_tokens):
    token_eval = 0
    token_eval += get_ratio(len(our_tokens["r"]), len(opponent_tokens["s"]))
    token_eval += get_ratio(len(our_tokens["p"]), len(opponent_tokens["r"]))
    token_eval += get_ratio(len(our_tokens["s"]), len(opponent_tokens["p"]))

    token_eval -= get_ratio(len(opponent_tokens["r"]), len(our_tokens["s"]))
    token_eval -= get_ratio(len(opponent_tokens["p"]), len(our_tokens["r"]))
    token_eval -= get_ratio(len(opponent_tokens["s"]), len(our_tokens["p"]))

    return token_eval


def token_distances(our_tokens, opponent_tokens):
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
