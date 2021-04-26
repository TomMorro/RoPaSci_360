def evaluate_board(player):
    # Things to evaluate
    # Number of tokens each player has
    ourTokens - theirTokens
    # Number of tokens left to throw
    ourThrowableTokens - theirThrowableTokens;
    # What types of tokens each player has

    # How close tokens are to being taken


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
