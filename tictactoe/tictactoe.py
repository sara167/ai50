"""
Tic Tac Toe Player
"""
import copy
import math

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
    empty_blocks = empty_blocks_count(board)

    player_str = "X" if empty_blocks == len(board) * len(board[0]) else "X" if empty_blocks % 2 != 0 else "O"
    return player_str


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_set = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                actions_set.append((i, j))
    return actions_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if board[action[0]][action[1]] != EMPTY:
        raise NameError('This action cannot be done')

    board_copy = copy.deepcopy(board)
    board_copy[action[0]][action[1]] = player(board)
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # checking each row
    for i in range(len(board)):
        if not has_empty_block(board[i]):
            row_as_string = "".join(board[i])
            if row_as_string.count("X") == 3:
                return "X"
            elif row_as_string.count("O") == 3:
                return "O"

    # checking each column
    for j in range(len(board[0])):
        col_as_string = ""
        for k in range(len(board)):
            if board[k][j] != EMPTY:
                col_as_string+= str(board[k][j])
                print(col_as_string)
        if col_as_string.count("X") == 3:
            return "X"
        elif col_as_string.count("O") == 3:
            return "O"

    # checking diagonal 1
    dia1 = [board[0][0], board[1][1], board[2][2]]
    dia1_as_string = ""
    if not has_empty_block(dia1):
        dia1_as_string = "".join(dia1)
    if dia1_as_string.count("X") == 3:
        return "X"
    if dia1_as_string.count("O") == 3:
        return "O"

    # checking diagonal 1
    dia2 = [board[0][2], board[1][1], board[2][0]]
    dia2_as_string = ""
    if not has_empty_block(dia2):
        dia2_as_string = "".join(dia2)
    if dia2_as_string.count("X") == 3:
        return "X"
    if dia2_as_string.count("O") == 3:
        return "O"

    return None


def empty_blocks_count(board):
    empty_blocks = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                empty_blocks += 1
    return empty_blocks


def has_empty_block(row):
    for i in range(len(row)):
        if row[i] == EMPTY:
            return True
    return False


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    elif empty_blocks_count(board) == 0:
        return True

    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    game_winner = winner(board)
    if "X" == game_winner:
        return 1
    elif "O" == game_winner:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == "X":
        action, v= MAX_value(board)
        return action
    else:
        action, v = MIN_value(board)
        return action


def MAX_value(board):
    if terminal(board):
        return None, utility(board)
    max_action, max_value = None, -100000000000
    for action in actions(board):
        empty, v= MIN_value(result(board, action))
        if v>max_value:
            max_value=v
            max_action=action
    return max_action, max_value


def MIN_value(board):
    if terminal(board):
        return None, utility(board)
    min_action, min_value = None, 100000000000
    for action in actions(board):
        empty, v= MAX_value(result(board, action))
        if v<min_value:
            min_value=v
            min_action=action
    return min_action, min_value
