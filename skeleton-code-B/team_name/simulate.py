import dwayne_johnson.board as board


def simulate_move(our_action, opponents_action, our_tokens, opponents_tokens, our_throws, opponents_throws):
    # Handle player actions
    if our_action[0] == "THROW":
        our_token_type = our_action[1]
        our_new_location = our_action[2]
        our_tokens[our_token_type].append(our_new_location)
        our_throws += 1
    else:
        before = our_action[1]
        our_new_location = our_action[2]
        our_token_type = board.find_token(before, our_tokens)
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
        opponent_token_type = board.find_token(before, opponents_tokens)
        opponents_tokens[opponent_token_type].remove(before)
        opponents_tokens[opponent_token_type].append(opponent_new_location)

    board.find_eats(our_token_type, opponent_token_type, our_new_location, opponent_new_location, our_tokens,
                    opponents_tokens)
