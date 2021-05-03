import board


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

        self.ourTokens = {'R': [], 'S': [], 'P': []}
        self.opponentTokens = {'R': [], 'S': [], 'P': []}
        self.ourThrows = 0
        self.opponentThrows = 0

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
            self.ourTokens[token_type].append(coordinates)
            self.ourThrows += 1
            board.find_eats(token_type, coordinates, self.ourTokens, self.opponentTokens)
        else:
            before = player_action[1]
            after = player_action[2]
            token_type = board.find_token(before, self.ourTokens)
            self.ourTokens[token_type].remove(before)
            self.ourTokens[token_type].append(after)
            board.find_eats(token_type, after, self.ourTokens, self.opponentTokens)

        # Handle opponent action
        if opponent_action[0] == "THROW":
            token_type = opponent_action[1]
            coordinates = opponent_action[2]
            self.opponentTokens[token_type].append(coordinates)
            self.opponentThrows += 1
            board.find_eats(token_type, coordinates, self.ourTokens, self.opponentTokens)
        else:
            before = opponent_action[1]
            after = opponent_action[2]
            token_type = board.find_token(before, self.ourTokens)
            self.opponentTokens[token_type].remove(before)
            self.opponentTokens[token_type].append(after)
            board.find_eats(token_type, after, self.ourTokens, self.opponentTokens)

        # Eating recognition as well
