# Finds a token given its location
def find_token(location, player):
    # Look in Rocks
    for cell in player["R"]:
        if cell == location:
            return "R"
    # Look in Scissors
    for cell in player["S"]:
        if cell == location:
            return "S"
    # Look in Papers
    for cell in player["P"]:
        if cell == location:
            return "P"

    return 0


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


class Player:

    def __init__(self, player):
        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.

        The parameter player is the string "upper" (if the instance will
        play as Upper), or the string "lower" (if the instance will play
        as Lower).
        """
        # put your code here
        if player == "upper":
            self.isUpper = True
        else:
            self.isUpper = False

        self.ourTokens = {'r': [], 's': [], 'p': []}
        self.opponentTokens = {'r': [], 's': [], 'p': []}

    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """
        # put your code here

    def update(self, opponent_action, player_action):
        """
        Called at the end of each turn to inform this player of both
        players' chosen actions. Update your internal representation
        of the game state.
        The parameter opponent_action is the opponent's chosen action,
        and player_action is this instance's latest chosen action.
        """
        # Handle player actions
        if player_action[0] == "THROW":
            token_type = player_action[1]
            coordinates = player_action[2]
            self.upperTokens[token_type].append(coordinates)
            find_eats(token_type, coordinates, self.lowerTokens)
        else:
            before = player_action[1]
            after = player_action[2]
            token_type = find_token(before, self.upperTokens)
            self.upperTokens[token_type].remove(before)
            self.upperTokens[token_type].append(after)
            find_eats(token_type, after, self.lowerTokens)

        # Handle opponent action
        if opponent_action[0] == "THROW":
            token_type = opponent_action[1]
            coordinates = opponent_action[2]
            self.upperTokens[token_type].append(coordinates)
            find_eats(token_type, coordinates, self.upperTokens)
        else:
            before = opponent_action[1]
            after = opponent_action[2]
            token_type = find_token(before, self.upperTokens)
            self.lowerTokens[token_type].remove(before)
            self.lowerTokens[token_type].append(after)
            find_eats(token_type, coordinates, self.upperTokens)

        # Eating recognition as well
