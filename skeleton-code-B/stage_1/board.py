def perform_move(our_action, opponents_action, our_tokens, opponents_tokens, our_throws, opponents_throws):
    """
    Performs a given move for a turn
    Args:
        our_action: the action chosen by our player
        opponents_action: teh action chosen by the opponent
        our_tokens: a dictionary containing our tokens
        opponents_tokens: a dictionary containing the opponent's tokens
        our_throws: how many throws we have made
        opponents_throws: how many throws the opponent has made

    Returns: an updated list of our tokens, our opponent's tokens and the number of throws from each player

    """
    # Handle player actions
    if our_action[0] == "THROW":
        our_token_type = our_action[1]
        our_new_location = our_action[2]
        our_tokens[our_token_type].append(our_new_location)
        our_throws += 1
    else:
        before = our_action[1]
        our_new_location = our_action[2]
        our_token_type = find_token(before, our_tokens)
        our_tokens[our_token_type].remove(before)
        our_tokens[our_token_type].append(our_new_location)

    # Handle opponent action
    if opponents_action[0] == "THROW":
        opponent_token_type = opponents_action[1]
        opponent_new_location = opponents_action[2]
        opponents_tokens[opponent_token_type].append(opponent_new_location)
        opponents_throws += 1
    else:
        before = opponents_action[1]
        opponent_new_location = opponents_action[2]
        opponent_token_type = find_token(before, opponents_tokens)
        opponents_tokens[opponent_token_type].remove(before)
        opponents_tokens[opponent_token_type].append(opponent_new_location)

    find_eats(our_token_type, opponent_token_type, our_new_location, opponent_new_location, our_tokens,
              opponents_tokens)

    return our_tokens, opponents_tokens, our_throws, opponents_throws


def find_token(location, player):
    """
    Finds what type of token a player has on a particular cell
    Args:
        location: the location of the cell
        player: the list of tokens of the player to be searched

    Returns: the token type or 0 if none found

    """
    # Look in Rocks
    for cell in player["r"]:
        if cell == location:
            return "r"
    # Look in Scissors
    for cell in player["s"]:
        if cell == location:
            return "s"
    # Look in Papers
    for cell in player["p"]:
        if cell == location:
            return "p"

    return 0


def find_eats(our_token_type, opponent_token_type, our_new_location, opponent_new_location, our_tokens,
              opponents_tokens):
    """
    Determines if there were any tokens eaten as a result of a single simultaneous move
    Args:
        our_token_type: the type of token we are performing an action with
        opponent_token_type: the type of token the opponent is performing an action with
        our_new_location: the new location of our token
        opponent_new_location: the new location of the opponent's token
        our_tokens: a dictionary containing our tokens
        opponents_tokens: a dictionary containing the opponent's tokens

    """
    for i in range(0, 2):
        if i == 0:
            token_type = our_token_type
            location = our_new_location
            tokens = our_tokens
        else:
            token_type = opponent_token_type
            location = opponent_new_location
            tokens = opponents_tokens

        # Ensures that the token we are dealing with hasn't already been eaten by previous check
        if location in tokens[token_type]:
            # Rock eats Scissors
            if token_type == "r":
                eat_token_type("s", location, our_tokens, opponents_tokens)
                # Rock eaten by Paper
                if location in our_tokens["p"] or location in opponents_tokens["p"]:
                    tokens[token_type].remove(location)

            # Scissors eats Paper
            elif token_type == "s":
                eat_token_type("p", location, our_tokens, opponents_tokens)
                # Scissors eaten by Rock
                if location in our_tokens["r"] or location in opponents_tokens["r"]:
                    tokens[token_type].remove(location)

            # Paper eats Rock
            elif token_type == "p":
                eat_token_type("r", location, our_tokens, opponents_tokens)
                # Paper eaten by Scissors
                if location in our_tokens["s"] or location in opponents_tokens["s"]:
                    tokens[token_type].remove(location)


def eat_token_type(token_type, location, our_tokens, opponents_tokens):
    """
    Removes all instances of a token on a cell
    Args:
        token_type: the type of token
        location: the location of the token
        our_tokens: a dictionary containing our tokens
        opponents_tokens: a dictionary containing the opponent's tokens

    """
    our_tokens[token_type] = [cell for cell in our_tokens[token_type] if cell != location]
    opponents_tokens[token_type] = [cell for cell in opponents_tokens[token_type] if cell != location]
