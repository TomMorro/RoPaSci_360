def evaluate_board(our_tokens, opponent_tokens, our_throws, opponent_throws):
    # Things to evaluate
    # Number of tokens each player has
    a = count_tokens(our_tokens) - count_tokens(opponent_tokens)
    # Number of tokens left to throw
    b = opponent_throws - our_throws
    # What types of tokens each player has
    c = 0
    c += get_ratio(len(our_tokens["R"]), len(opponent_tokens["S"]))
    c += get_ratio(len(our_tokens["P"]), len(opponent_tokens["R"]))
    c += get_ratio(len(our_tokens["S"]), len(opponent_tokens["P"]))

    c -= get_ratio(len(opponent_tokens["R"]), len(our_tokens["S"]))
    c -= get_ratio(len(opponent_tokens["P"]), len(our_tokens["R"]))
    c -= get_ratio(len(opponent_tokens["S"]), len(our_tokens["P"]))
    # How close tokens are to being taken
    print(a, b, c)


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
