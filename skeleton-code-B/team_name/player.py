
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
            self.ourTokens[token_type].append(coordinates)
        else:
            before = player_action[1]
            after = player_action[2]


            token = self.locations[before]
            self.locations.pop(before)
            self.locations[after] = token

        # Handle opponent action
        if opponent_action[0] == "THROW":
            token_type = opponent_action[1]
            coordinates = opponent_action[2]
            self.opponentTokens[token_type].append(coordinates)
        else:
            before = opponent_action[1]
            after = opponent_action[2]
            token = self.locations[before]
            self.locations.pop(before)
            self.locations[after] = token
