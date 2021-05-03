import player
import evaluation


def simulate_move(our_action, opponents_action):
    our_tokens = Player.ourTokens
    opponents_tokens = Player.opponentTokens
    our_throws = Player.ourThrows
    opponents_throws = Player.opponentThrows
    if player_action[0] == "THROW":
        token_type = player_action[1]
        coordinates = player_action[2]
        our_tokens[token_type].append(coordinates)
        our_throws += 1
        find_eats(token_type, coordinates, opponents_tokens)
    else:
        before = player_action[1]
        after = player_action[2]
        token_type = find_token(before, self.ourTokens)
        our_tokens[token_type].remove(before)
        our_tokens[token_type].append(after)
        find_eats(token_type, after, opponents_tokens)

        # Handle opponent action
    if opponent_action[0] == "THROW":
        token_type = opponent_action[1]
        coordinates = opponent_action[2]
        opponents_tokens[token_type].append(coordinates)
        opponents_throws += 1
        find_eats(token_type, coordinates, our_tokens)
    else:
        before = opponent_action[1]
        after = opponent_action[2]
        token_type = find_token(before, ourTokens)
        opponents_tokens[token_type].remove(before)
        opponents_tokens[token_type].append(after)
        find_eats(token_type, after, our_tokens)

    return our_token, opponents_tokens, our_throws, opponents_throws


# Determine if there were any tokens eat as a result a move
def find_eats(token_type, location, player_eat):
    # Rock eats Scissors
    if token_type == "R":
        for cell in player_eat["S"]:
            if cell == location:
                player_eat["S"].remove(cell)

    # Scissors eats Paper
    if token_type == "S":
        for cell in player_eat["P"]:
            if cell == location:
                player_eat["P"].remove(cell)

    # Paper eats Rock
    if token_type == "P":
        for cell in player_eat["R"]:
            if cell == location:
                player_eat["R"].remove(cell)