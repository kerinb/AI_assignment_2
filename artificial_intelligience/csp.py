

def printBoard(board, N):
    for i in range(N):
        for j in range(N):
            print(board[i][j], end='')
        print() #to get new line for board

def consistencyCheck(board, row, col, N):
    # check for other queen in same row
    for i in range(col):
        if board[row][i] == 1:
            return False

    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False

        # Check lower diagonal on left side
    for i, j in zip(range(row, N, 1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False

    return True

#
# Goal - add a queen to any square in the leftmost column such that it is not attacked by any other queen
#
def back_tracking(board, col, N):
    # finished - all queens have been added in safe place
    if col == N:
        return True

    # not finished - try placing queen in each row in leftmost column
    for row in range(N):

        if consistencyCheck(board, row, col, N):
            # is safe move - add
            board[row][col] = 1
            # printSolution(board, N)

            # place other queens to see if this position is safe
            if back_tracking(board, col + 1, N) == True:
                return True

            # doesn't lead to solution - backtrack, remove queen from cell
            board[row][col] = 0

    # if the queen can not be placed in any row in
    # this column col  then return false
    return False

def createBoard(numQueens):
    board = []
    for i in range(0, numQueens):
        board.append([0] * numQueens)
    return board

def n_queens_backtracking(numberQueens):
    board = createBoard(numberQueens)
    if back_tracking(board, 0, numberQueens) == False:
        print ("Solution does not exist")
        return False
    printBoard(board, numberQueens)
    return True

if __name__ == '__main__':
    n_queens_backtracking(16)