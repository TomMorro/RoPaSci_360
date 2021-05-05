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
        update = board.perform_move(player_action, opponent_action, self.ourTokens, self.opponentTokens,
                                    self.ourThrows, self.opponentThrows)
        self.ourTokens = update[0]
        self.opponentTokens = update[1]
        self.ourThrows = update[2]
        self.opponentThrows = update[3]
