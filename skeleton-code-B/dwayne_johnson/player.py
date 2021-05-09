import dwayne_johnson.board as board
import dwayne_johnson.gametheory as gametheory
import dwayne_johnson.payoff as payoff
import dwayne_johnson.simulate as simulate
import dwayne_johnson.constant as constant
import random


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

        self.ourTokens = {"r": [], "s": [], 'p': []}
        self.opponentTokens = {"r": [], "s": [], 'p': []}
        self.ourThrows = 0
        self.opponentThrows = 0

    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """
        #payoff_matrix = payoff.create_payoff_matrix(self.ourTokens, self.opponentTokens, self.ourThrows,
        #                                           self.opponentThrows, self.isUpper)
        payoff_matrix = simulate.simulate_move_tree(self.ourTokens, self.opponentTokens, self.ourThrows,
                                                    self.opponentThrows, self.isUpper, 0, constant.SIMULATE_DEPTH)

        matrix = payoff_matrix[0]
        ours = payoff_matrix[1]
        possible_moves = gametheory.solve_game(matrix)[0]
        move = random.choices(ours, weights=possible_moves)
        return move[0]

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
