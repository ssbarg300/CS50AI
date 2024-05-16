"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    
    xc = 0
    oc = 0
    for i in range(3):
        for y in range(3):
            if board[i][y] == X:
                xc += 1
            elif board[i][y] == O:
                oc += 1
    if xc > oc:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    if terminal(board):
        return possible_actions
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    dboard = copy.deepcopy(board)
    # check if action is illegal
    if dboard[action[0]][action[1]] != EMPTY:
        raise Exception("illegal move")
    if (action[0] < 0 or action[0] > 2) or (action[1] < 0 or action[1] > 2):
        raise Exception("out of bounds move")
    dboard[action[0]][action[1]] = player(board)
    return dboard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
   
    # Check rows and columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
            return board[0][i]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    for x in range(3):
        for j in range(3):
            if board[x][j] == EMPTY:
                return False
            
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # base case
    if terminal(board) == True:
        return None
    # recursive Exploration
    # maximising player.
    if player(board) == X:
        # initialise the best value to negative infinity(because then any value would be greater therefor better.)
        best_value = float('-inf')
        # initialise best_action to None this is the action we will return after we find where is the best action
        best_action = None
        # iterate through all the possible actions in the current board.
        for a in actions(board):
            #
            value = min_value(result(board, a))
            if value > best_value:
                best_value = value
                best_action = a
        return best_action

    if player(board) == O:
        best_value = float('inf')
        best_action = None
        for a in actions(board):
            value = max_value(result(board, a))
            if value < best_value:
                best_value = value
                best_action = a
        return best_action


def min_value(board):
    # base case
    if terminal(board):
        return utility(board)
    # set v to infinity so everything is lower.
    v = float('inf')
    for action in actions(board):
        # here we assume O plays optimally so we will choose the minimum value of the max_value(results(s,a))
        v = min(v, max_value(result(board, action)))
    return v


def max_value(board):
    # base case.
    if terminal(board):
        return utility(board)
    # we set v to the - infinity so anything is greater
    v = float('-inf')
    for action in actions(board):
        # O also assumes X plays optimally so we will choose the maximum value of min_value(result(s,a))
        v = max(v, min_value(result(board, action)))
    # then we return the value
    return v