import board


def simulate_move(our_action, opponents_action, our_tokens, opponents_tokens, our_throws, opponents_throws):
    if our_action[0] == "THROW":
        token_type = our_action[1]
        coordinates = our_action[2]
        our_tokens[token_type].append(coordinates)
        our_throws += 1
        board.find_eats(token_type, coordinates, our_tokens, opponents_tokens)
    else:
        before = our_action[1]
        after = our_action[2]
        token_type = board.find_token(before, our_tokens)
        our_tokens[token_type].remove(before)
        our_tokens[token_type].append(after)
        board.find_eats(token_type, after, our_tokens, opponents_tokens)

    # Handle opponent action
    if opponents_action[0] == "THROW":
        token_type = opponents_action[1]
        coordinates = opponents_action[2]
        opponents_tokens[token_type].append(coordinates)
        opponents_throws += 1
        board.find_eats(token_type, coordinates, our_tokens, opponents_tokens)
    else:
        before = opponents_action[1]
        after = opponents_action[2]
        token_type = board.find_token(before, our_tokens)
        opponents_tokens[token_type].remove(before)
        opponents_tokens[token_type].append(after)
        board.find_eats(token_type, after, our_tokens, opponents_tokens)

    return our_tokens, opponents_tokens, our_throws, opponents_throws