"""
Solver for single-stage, zero-sum matrix-form games using scipy default
linear programming routines.

Original by Matthew Farrugia-Roberts, 2021

Adapted for use by William Chio and Thomas Morrison

"""

import numpy as np
import scipy.optimize as opt


def solve_game(matrix, maximiser=True, row_player=True):
    """
    Given a utility matrix V for a zero-sum game, compute a mixed-strategy
    security strategy/Nash equilibrium solution along with the bound on the
    expected value of the game to the player.
    By default, assume the player is the MAXIMISER and chooses the ROW of V,
    and the opponent is the MINIMISER choosing the COLUMN. Use the flags to
    change this behaviour.

    Parameters
    ----------
    * matrix: (n, m)-array or array-like; utility/payoff matrix;
    * maximiser: bool (default True); compute strategy for the maximiser.
        Set False to play as the minimiser.
    * row_player: bool (default True); compute strategy for the row-chooser.
        Set False to play as the column-chooser.

    Returns
    -------
    * s: (n,)-array; probability vector; an equilibrium mixed strategy over
        the rows (or columns) ensuring expected value v.
    * v: float; mixed security level / guaranteed minimum (or maximum)
        expected value of the equilibrium mixed strategy.

    Exceptions
    ----------
    * OptimisationError: If the optimisation reports failure. The message
        from the optimiser will accompany this exception.
    """
    matrix = np.asarray(matrix)
    # lprog will solve for the column-maximiser
    if row_player:
        matrix = matrix.T
    if not maximiser:
        matrix = -matrix
    m, n = matrix.shape
    # ensure positive
    c = -matrix.min(initial=0) + 1
    v_pos = matrix + c
    # solve linear program
    res = opt.linprog(
        np.ones(n),
        A_ub=-v_pos,
        b_ub=-np.ones(m),
        options={'tol': 1e-8},
    )
    if res.status:
        raise OptimisationError(res.message)
    # compute strategy and value
    v = 1 / res.x.sum()
    s = res.x * v
    v = v - c  # re-scale
    if not maximiser:
        v = -v
    return s, v


class OptimisationError(Exception):
    """For if the optimiser reports failure."""
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return "Optimisation Error: {0}".format(self.message)
        else:
            return "Optimisation Error"
