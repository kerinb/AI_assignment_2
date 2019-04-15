#################################################################################
# Contributors - Breandán Kerin, Sinead Dickson, Alanna O'Grady, Daniel Lavelle #
#               Artificial Intelligence Assignment 2                            #
#################################################################################

import time
import matplotlib.pyplot as plt
from copy import deepcopy
import random
import numpy as np

num_checks = 0


def print_board(board, n):
    for i in range(n):
        for j in range(n):
            print(board[i][j], end='')
        print()  # to get new line for board


def consistency_check_backtrack(board, row, col, n):
    # check for other queen in same row
    global num_checks
    num_checks += 1

    for i in range(col):
        num_checks += 1
        if board[row][i] == 1:
            return False

    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        num_checks += 1
        if board[i][j] == 1:
            return False

        # Check lower diagonal on left side
    for i, j in zip(range(row, n, 1), range(col, -1, -1)):
        num_checks += 1
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
def is_safe_bnb(row, col, forward_slash_helper, back_slash_helper, row_lookup_helper, forward_slash_lookup_helper, back_slash_lookup_helper):
    val1 = forward_slash_helper[row][col]
    val2 = back_slash_helper[row][col]

    global num_checks
    num_checks += 1

    if forward_slash_lookup_helper[val1] or back_slash_lookup_helper[val2] or row_lookup_helper[row]:
        return False
    return True


# A recursive utility function to solve N Queen problem
def bnb_solve_n_q(board, col, forward_slash_helper, back_slash_helper, row_lookup_helper, forward_slash_lookup_helper, back_slash_lookup_helper, n):
    # base case: If all queens are placed then return true
    if col >= n:
        return True

    # Consider this column and try placing this queen in all rows one by one
    for i in range(n):
        # Check if queen can be placed on board[i][col]
        if is_safe_bnb(i, col, forward_slash_helper, back_slash_helper, row_lookup_helper,
                       forward_slash_lookup_helper, back_slash_lookup_helper):

            # Place this queen in board[i][col]
            board[i][col] = 1
            row_lookup_helper[i] = True
            val1 = forward_slash_helper[i][col]
            val2 = back_slash_helper[i][col]
            forward_slash_lookup_helper[val1] = True
            back_slash_lookup_helper[val2] = True

            # recur to place rest of the queens
            if bnb_solve_n_q(board, col + 1, forward_slash_helper, back_slash_helper, row_lookup_helper,
                             forward_slash_lookup_helper, back_slash_lookup_helper, n):
                return True

            # If placing queen in board[i][col] doesn't lead to a solution, then backtrack
            # Remove queen from board[i][col]
            board[i][col] = 0
            row_lookup_helper[i] = False
            val1 = forward_slash_helper[i][col]
            val2 = back_slash_helper[i][col]
            forward_slash_lookup_helper[val1] = False
            back_slash_lookup_helper[val2] = False

    # If queen can not be place in any row in this column col then return false
    return False


def n_queens_branch_and_bound(n):
    print("Branch and Bound")
    board = create_board(n)

    # helper matrices
    forward_slash_helper = create_board(n)
    back_slash_helper = create_board(n)

    # arrays to tell us which rows are occupied
    row_helper = [False] * n

    # keep two arrays to tell us which diagonals are occupied
    forward_slash_lookup_helper = [False] * (2 * n - 1)
    back_slash_lookup_helper = [False] * (2 * n - 1)

    # initialise helper matrices
    for r in range(n):
        for c in range(n):
            forward_slash_helper[r][c] = r + c
            back_slash_helper[r][c] = r - c + (n - 1)

    if not bnb_solve_n_q(board, 0, forward_slash_helper, back_slash_helper,
                         row_helper, forward_slash_lookup_helper, back_slash_lookup_helper, n):
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
    start = time.time()
    print("backtrack")
    board = create_board(number_queens)
    if not back_tracking(board, 0, number_queens):
        print("Solution does not exist")
        end = time.time()
        execution_time = end - start
        print(execution_time)
        return execution_time
    print_board(board, number_queens)
    end = time.time()
    execution_time = end - start
    print(execution_time)
    return execution_time

##~~~~~~~~~~~~~~~~ HILL CLIMBING ~~~~~~~~~~~~~~

def generate_random_board(n):
    """
    Returns a vector of positions where queen is for
    each column
    """
    q = []
    b = create_board(n)
    for col in range(n):  
        r = random.randint(0, n-1)
        q.append(r)
        b[r][col] = 1
    return b, q
def do_avoid_eachother(i, j, q):
    """
    Assumes i != j, and j > i
    """
    global num_checks
    num_checks+=1
    if q[i] == q[j]:
        return 0
    elif abs(j-i) == abs(q[j] - q[i]):
        return 0
    else:
        
        return 1
def objective_function(q):
    """
    Measure how many pairs of queens do not get in each other's way
    param: board a 2 d list indicating where queens are
    param: q : a list indictating where the queens for each column are
    n: n for n queens
    """
    result = 0
    n = len(q)
    for i in range(n):
        for j in range(i+1, n):
            # check if queen i and j are giving each other grief
            avoid_eachother = do_avoid_eachother(i,j,q)
            result += avoid_eachother
            
    return result



def compute_optimum_avoiding_pairs(n):
    """
    Compute the optimum number of queens
    that could avoid each other for n queens
    problem, given by sigma(n)
    """
    count = 0
    for i in range(n):
        count+=i
    return count

def hill_climbing_algorithm(starting_q):
    """
    Compute hill climbing algorithm for input
    list of queen positions
    """
    start = time.time()
    n = len(starting_q)
    optimum = compute_optimum_avoiding_pairs(n)
    best_score = objective_function(starting_q) 
    q = starting_q
    while(best_score < optimum):
        better_score_found = False
        for i in range(n):
            # Cycle through all queens
            temp_q = deepcopy(q)
            for j in range(n):
                if j != q[i]:
                    temp_q[i] = j
                    score = objective_function(temp_q)
                    if score > best_score:
                        q = temp_q
                        best_score = score
                        better_score_found = True
                        break
                
                
        if not better_score_found:
            q = randomise_board(q)
            best_score = objective_function(q)
    end = time.time()
    ##print("Hill Climbing board results:") 
    ##print_board_q(q)
    return end-start

def randomise_board(q):
    """
    Randomise board given input is a list of
    queen positions
    """
    n = len(q)
    for i in range(n):
        q[i] = random.randint(0, n-1)
    return q
def print_board_q(q):
    """
    Print function specific to the list data structure used in 
    hill climbing
    """
    n = len(q)
    b = create_board(n)
    for i in range(n):
        b[q[i]][i] = 1
    print_board(b, n)
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    backtracking_execution_times = []
    backtracking_num_checks = []
    bnb_execution_times = []
    bnb_num_checks = []
    hill_climbing_execution_times = []
    hill_climbing_num_checks = []
    queens_test_range = range(4, 24, 4)
    HILL_CLIMBING_SAMPLE_SIZE = 20 ## In order to account for randomisation
    # backtracking
    for i in queens_test_range:
        print(i)
        #backtracking
        backtracking_execution_times.append(n_queens_backtracking(i))
        print("BackTracking Time Taken: " + str(n_queens_backtracking(i)))
        print("Number of checks in Backtracking: " + str(num_checks))
        backtracking_num_checks.append(num_checks)
        num_checks = 0  # reinitialise to 0 for next algorithm
        #bnb
        start_time = time.time()
        n_queens_branch_and_bound(i)
        bnb_execution_times.append(time.time() - start_time)
        print("Branch and Bound Time Taken: %s" % (str(time.time() - start_time)))
        print("Number of checks in BNB: " + str(num_checks))
        bnb_num_checks.append(num_checks)
        num_checks = 0  # reinitialise to 0 for next algorithm

        ##hill climbing
        temp_times = []
        temp_checks = []
        for _ in range(HILL_CLIMBING_SAMPLE_SIZE):
            _, q = generate_random_board(i)
            t = hill_climbing_algorithm(q)
            temp_times.append(t)
            temp_checks.append(num_checks)
            num_checks = 0
        hill_climbing_execution_times.append(np.median(temp_times))
        hill_climbing_num_checks.append(np.median(temp_checks))
        print("Hill Climbing Time Taken: %s" % (np.median(temp_times)))
        print("Number of checks in Hill Climbing: " + str(np.median(temp_checks)))
        

    # execution time plot
    plt.plot(queens_test_range, backtracking_execution_times)
    plt.plot(queens_test_range, bnb_execution_times)
    plt.plot(queens_test_range, hill_climbing_execution_times)
    plt.title("Execution Times")
    plt.xlabel("Number of Queens")
    plt.ylabel("Time [s]")
    plt.legend(['Backtracking', "Branch and Bound", "Hill Climbing"], loc='upper left')
    plt.savefig('execution_times.png')
    plt.clf()

    # number of checks plot
    plt.plot(queens_test_range, backtracking_num_checks)
    plt.plot(queens_test_range, bnb_num_checks)
    plt.plot(queens_test_range, hill_climbing_num_checks)
    plt.title("Number of Checks")
    plt.xlabel("Number of Queens")
    plt.ylabel("Time [s]")
    plt.legend(['Backtracking', "Branch and Bound", "Hill Climbing"], loc='upper left')
    plt.savefig('number_checks.png')
