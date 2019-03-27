#################################################################################
# Contributors - Breandán Kerin, Sinead Dickson, Alanna O'Grady, Daniel Lavelle #
#               Artificial Intelligence Assignment 2                            #
#################################################################################

import sys
import time

num_checks = 0


def print_board(board, n):
    for i in range(n):
        for j in range(n):
            print(board[i][j], end='')
        print()  # to get new line for board


def consistency_check_backtrack(board, row, col, n):
    # check for other queen in same row
    for i in range(col):
        if board[row][i] == 1:
            return False

    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False

        # Check lower diagonal on left side
    for i, j in zip(range(row, n, 1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False

    return True


#
# Goal - add a queen to any square in the leftmost column such that it is not attacked by any other queen
#
def back_tracking(board, col, n):
    # finished - all queens have been added in safe place
    if col == n:
        return True

    # not finished - try placing queen in each row in leftmost column
    for row in range(n):

        if consistency_check_backtrack(board, row, col, n):
            # is safe move - add
            board[row][col] = 1
            # printSolution(board, N)

            # place other queens to see if this position is safe
            if back_tracking(board, col + 1, n):
                return True

            # doesn't lead to solution - backtrack, remove queen from cell
            board[row][col] = 0

    # if the queen can not be placed in any row in
    # this column col  then return false
    return False


# A Optimized function to check if a queen can  be placed on board[row][col]
def is_safe_bnb(row, col, slash_code, backslash_code, row_lookup, slash_code_lookup, backslash_code_lookup):
    val1 = slash_code[row][col]
    val2 = backslash_code[row][col]

    global num_checks
    num_checks += 1

    if slash_code_lookup[val1] or backslash_code_lookup[val2] or row_lookup[row]:
        return False
    return True


# A recursive utility function to solve N Queen problem
def bnb_solve_n_q(board, col, slash_code, backslash_code, row_lookup, slash_code_lookup, backslash_code_lookup, n):
    # base case: If all queens are placed then return true
    if col >= n:
        return True

    # Consider this column and try placing this queen in all rows one by one
    for i in range(n):
        # Check if queen can be placed on board[i][col]
        if is_safe_bnb(i, col, slash_code, backslash_code, row_lookup,
                       slash_code_lookup, backslash_code_lookup):

            # Place this queen in board[i][col]
            board[i][col] = 1
            row_lookup[i] = True
            val1 = slash_code[i][col]
            val2 = backslash_code[i][col]
            slash_code_lookup[val1] = True
            backslash_code_lookup[val2] = True

            # recur to place rest of the queens
            if bnb_solve_n_q(board, col + 1, slash_code, backslash_code, row_lookup,
                             slash_code_lookup, backslash_code_lookup, n):
                return True

            # If placing queen in board[i][col] doesn't lead to a solution, then backtrack
            # Remove queen from board[i][col]
            board[i][col] = 0
            row_lookup[i] = False
            val1 = slash_code[i][col]
            val2 = backslash_code[i][col]
            slash_code_lookup[val1] = False
            backslash_code_lookup[val2] = False

    # If queen can not be place in any row in this column col then return false
    return False


def n_queens_branch_and_bound(n):
    print("Branch and Bound")
    board = create_board(n)

    # helper matrices
    slash_code = create_board(n)
    backslash_code = create_board(n)

    # arrays to tell us which rows are occupied
    row_lookup = [False] * n

    # keep two arrays to tell us which diagonals are occupied
    slash_code_lookup = [False] * (2 * n - 1)
    backslash_code_lookup = [False] * (2 * n - 1)

    # initialise helper matrices
    for r in range(n):
        for c in range(n):
            slash_code[r][c] = r + c
            backslash_code[r][c] = r - c + (n - 1)

    if not bnb_solve_n_q(board, 0, slash_code, backslash_code,
                         row_lookup, slash_code_lookup, backslash_code_lookup, n):
        print("solution doesn't exist")
        return False
    print_board(board, n)
    return True


def create_board(num_queens):
    board = []
    for i in range(0, num_queens):
        board.append([0] * num_queens)
    return board


def n_queens_backtracking(number_queens):
    print("backtrack")
    board = create_board(number_queens)
    if not back_tracking(board, 0, number_queens):
        print("Solution does not exist")
        return False
    print_board(board, number_queens)
    return True


if __name__ == '__main__':
    problem = sys.argv[1]
    n = int(sys.argv[2])

    if problem == "backtrack":
        start_time = time.time()
        n_queens_backtracking(n)
        print("BackTracking Time Taken" + str(time.time() - start_time))
        print("Number of checks in BNB: " + str(num_checks))

    elif problem == "bnb":
        start_time = time.time()
        n_queens_branch_and_bound(n)

        print("Branch and Bound Time Taken: %s" % (str(time.time() - start_time)))
        print("Number of checks in BNB: " + str(num_checks))

    elif problem == "arcConsistency":
        print("this is dans area")
